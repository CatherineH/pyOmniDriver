from py4j.java_gateway import JavaGateway
from subprocess import call
from multiprocessing import Process, Pipe
import os
import sys
import time


def get_classpath():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin'))


def init_jvm(pipe_to_parent=None):
    """
    init_jvm starts the gateway java instance
    :param pipe_to_parent: a pipe to the parent process to send error messages to
    :return:
    """
    try:
        # first, setup and test the file locations - change these to your system

        od_jar_locations = "C:\\Program Files\\Ocean Optics\\OmniDriver\\OOI_HOME"
        java_location = "C:\\Program Files\\Java\\jre1.8.0_65\\bin\\java.exe"
        py4j_location = "c:\\Python27\\share\\py4j\\py4j0.9.jar"

        if not os.path.isdir(od_jar_locations):
            print "OmniDriver directory: "+od_jar_locations+" does not exist"
            raise ValueError("OmniDriver directory: "+od_jar_locations+" does not exist")

        if not os.path.exists(java_location):
            print "Java not found at: "+java_location
            raise ValueError("Java not found at: "+java_location)
        if not os.path.exists(py4j_location):
            print "Py4J not found at: "+py4j_location
            raise ValueError("Py4J not found at: "+py4j_location)

        jars = [os.path.join(od_jar_locations, _file) for _file in os.listdir(od_jar_locations) if _file.endswith(".jar")]

        # this assumes that your .class file has been compiled to the same folder as this script
        file_encoding = "-Dfile.encoding=Cp1252"
        jars.append(py4j_location)

        classpath = get_classpath()+";"+";".join(jars)
        parts = [java_location, file_encoding, "-classpath", classpath, "SpectrometerServer"]
        call(parts)
    except Exception as e:
        print "pyOmniDriver failed: " + str(e)
        if pipe_to_parent is not None:
            pipe_to_parent.send((type(e), e))


class Spectrometer(JavaGateway):
    def __init__(self):
        super(self.__class__, self).__init__()
        to_child, to_self = Pipe()
        p = Process(target=init_jvm, args=(to_self,))
        p.start()
        # check on how the java connection went
        #exc_info = to_child.recv()
        # if the startup did not go well, exit
        '''
        if exc_info[0] == ValueError:
            print "pyOmniDriver failed: "+str(exc_info[1])
            return
        '''
        # wait for the process to start
        connection = False
        out_str = ""
        while not connection:
            try:
                api_ver = self.getApiVersion()
                print "connected to OmniDriver Version: " + api_ver
                connection = True
            except Exception as e:
                out_str += "."
                sys.stdout.write(out_str+'\r')
                sys.stdout.flush()
                print e
                time.sleep(0.1)
