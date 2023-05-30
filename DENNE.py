import time
import serial
#from periphery import GPIO
#import periphery
from multiprocessing import Process
import argparse

"""ap = argparse.ArgumentParser()
ap.add_argument("--rpm",required = True, help = "Enter rpm")
args = vars(ap.parse_args())
rpm = args['rpm']"""

def CheckPhotoCell(oldState, new_state):
    if oldState and oldState != new_state:
        return (True, new_state)
    else:
        return (False, new_state)

serial_port = serial.Serial("ttyAM0",9600)
measurementsIn = []
measurementsOut = []
#speed = 3.14 * 46 * rpm / 60

def measureIn():
    if heightDecode.find("Inn") != -1 and start - time.time() < 5:
        heightIn = heightDecode.replace("Inn", "")
        print(heightIn)
        measurementsIn.append(float(heightIn))
    if start - time.time() > 5:
        maxIn = max(measurementsIn)
        with open("measurementsIn.csv", "a") as f:
            for item in measurementsIn:
                f.write(f"{item},{maxIn}\n")
        measurementsIn.clear()
        return

# ta høyde for tid

def measureOut():
    if heightDecode.find("Ut") != -1 and start - time.time() < 5:
        heightOut = heightDecode.replace("Ut", "")
        print(heightOut)
        measurementsOut.append(heightOut)
    if start - time.time() > 5:
        maxOut = max(measurementsOut)
        with open("measurementsOut.csv", "a") as f:
            for item in measurementsOut:
                f.write(f"{item},{maxOut}\n")
        measurementsOut.clear()
        return

if __name__ == "__main__":   
    start = time.time()
    sensor = GPIO(156, "in")
    bagCount = 0
    oldState = False
    height = serial_port.readline()
    heightDecode = height.decode("utf-8")
    bagPassed, oldState = CheckPhotoCell(oldState, sensor.read())
    measure1 = Process(target=measureIn)
    measure2 = Process(target=measureOut)
    if bagPassed:
        start = time.time()
        measure1.start()
        measure2.start()

# tanken er at denne skal ligge å måle hele tiden, mens et annet program leser fra filene
# og skriver til en annen fil som kan brukes til å plotte i guien