from py4j.java_gateway import JavaGateway
from subprocess import call
from multiprocessing import Process
import os
import sys
import time


def init_jvm():
    # first, start the gateway program
    od_jar_locations = os.path.expanduser("C:\\Program Files\\Ocean Optics\\OmniDriver\\OOI_HOME")
    jars = [os.path.join(od_jar_locations, _file) for _file in os.listdir(od_jar_locations) if _file.endswith(".jar")]

    # this assumes that your .class file has been compiled to the same folder as this script
    java_locations = "C:\\Program Files\\Java\\jre1.8.0_65\\bin\\java.exe"
    file_encoding = "-Dfile.encoding=Cp1252"
    py4j_location = "c:\\Python27\\share\\py4j\\py4j0.9.jar"
    jars.append(py4j_location)
    classpath = os.getcwd().replace("src", "bin")+";"+";".join(jars)
    parts = [java_locations, file_encoding, "-classpath", classpath, "SpectrometerServer"]
    call(parts)


class Spectrometer(JavaGateway):
    def __init__(self):
        super(self.__class__, self).__init__()
        p = Process(target=init_jvm)
        p.start()
        # wait for the process to start
        connection = False
        out_str = ""
        while not connection:
            try:
                api_ver = self.getApiVersion()
                print "connected to OmniDriver Version: " + api_ver
                connection = True
            except:
                out_str += "."
                sys.stdout.write(out_str+'\r')
                sys.stdout.flush()
                time.sleep(0.1)