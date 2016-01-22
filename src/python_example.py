from py4j.java_gateway import JavaGateway
from subprocess import call
from multiprocessing import Process
import os
import sys
import time


def init_jvm():
    # first, start the gateway program
    od_jar_locations = os.path.expanduser("~/OmniDriver/OOI_HOME")
    jars = [os.path.join(od_jar_locations, _file) for _file in os.listdir(od_jar_locations) if _file.endswith(".jar")]

    # this assumes that your .class file has been compiled to the same folder as this script
    java_locations = "/usr/lib/jvm/java-7-openjdk-amd64/bin/java"
    file_encoding = "-Dfile.encoding=UTF-8"
    py4j_location = "/usr/local/share/py4j/py4j0.9.1.jar"
    jars.append(py4j_location)
    classpath = os.getcwd().replace("src", "bin")+":"+":".join(jars)
    call([java_locations, file_encoding, "-classpath", classpath, "SpectrometerServer"])

p = Process(target = init_jvm)


p.start()
gateway = JavaGateway()                   # connect to the JVM
wrapper = gateway.entry_point

# wait for the process to start

connection = False
out_str = ""
while not connection:
    try:
        api_ver = wrapper.getApiVersion()
        print "connected to OmniDriver Version: " + api_ver
        connection = True
    except:
        out_str += "."
        sys.stdout.write(out_str+'\r')
        sys.stdout.flush()
        time.sleep(0.1)
num_open = wrapper.openAllSpectrometers()

spectrometerIndex = 0
channelIndex = 0
integrationTime = 800000
wrapper.setIntegrationTime(spectrometerIndex, channelIndex, integrationTime)

pixels = wrapper.getSpectrum(spectrometerIndex, channelIndex)
p.terminate()


