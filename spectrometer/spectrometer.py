from py4j.java_gateway import JavaGateway
from subprocess import call
from multiprocessing import Process, Pipe
import os
import sys
import time


class SpectrometerException(Exception):
    pass


def init_jvm(pipe_to_parent=None):
    """
    init_jvm starts the gateway java instance
    :return:
    """
    OOI_HOME = os.getenv('OOI_HOME', "C:\\Program Files\\Ocean Optics\\OmniDriver")
    JAVA_HOME = os.getenv('JAVA_HOME',"C:\\Program Files\\Java\\jre1.8.0_65")
    PYTHON_HOME = os.getenv('PYTHONHOME','C:\\Python35')
    java_location = os.path.join(JAVA_HOME, "bin\\java.exe")
    py4j_location = os.path.join(PYTHON_HOME, "share\\py4j")

    if not os.path.isdir(OOI_HOME):
        raise ValueError("OmniDriver directory: " + OOI_HOME + " does not exist")

    if not os.path.exists(java_location):
        raise ValueError("Java not found at: "+java_location)
    if not os.path.exists(py4j_location):
        raise ValueError("Py4J not found at: "+py4j_location)

    jars = [os.path.join(OOI_HOME, _file)
            for _file in os.listdir(OOI_HOME)
            if _file.endswith(".jar")]

    # this assumes that your .class file has been compiled to the same
    # folder as this script
    file_encoding = "-Dfile.encoding=Cp1252"
    jars.append([os.path.join(py4j_location, _file)
            for _file in os.listdir(py4j_location)
            if _file.endswith(".jar")][0])
    classpath = os.path.dirname(__file__)+";"+OOI_HOME+";"+";".join(jars)
    ld_library_path = '-Djava.library.path='+OOI_HOME
    parts = [java_location, file_encoding, ld_library_path, "-classpath", classpath,
             "SpectrometerServer"]
    call(parts)


class Spectrometer(JavaGateway):
    def __init__(self):
        super(self.__class__, self).__init__()
        #to_child, to_self = Pipe()
        p = Process(target=init_jvm)
        p.start()

        # wait for the process to start
        connection = False
        out_str = ""
        while not connection:
            try:
                api_ver = self.getApiVersion()
                print("connected to OmniDriver Version: " + api_ver)
                connection = True
            except Exception as e:
                out_str += "."
                sys.stdout.write(out_str+'\r')
                sys.stdout.flush()
                print(e)
                time.sleep(0.1)
