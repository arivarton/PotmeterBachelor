import serial 
import argparse
import datetime
import time
import random

measurementsIn = []
measurementsOut = []

def measureHeight(name): 
    date = datetime.datetime.now().date()
    fileIn = open(f"{date}Inn.csv", "w")
    fileIn.close()
    fileOut = open(f"{date}Ut.csv", "w")
    fileOut.close()
    counterIn = 0
    counterOut = 0
    maxInList = []
    maxOutList = []
    try:
        serial_port = serial.Serial(name,9600)

        while True:
            height = serial_port.readline()
            heightDecode = height.decode("utf-8")

            if heightDecode.find("Inn") != -1:
                heightIn = heightDecode.replace("Inn", "")
                print(heightIn)
                measurementsIn.append(heightIn)
            if heightDecode.find("PoseI") != -1 and len(measurementsIn) > 0:
                start = time.time()
                counterIn += 1
                fileIn = open(f"{date}Inn.csv", "a")
                maxIn = max(measurementsIn)
                maxInList.append(float(maxIn))
                fileIn.write(f"{counterIn}, {maxIn}, {len(measurementsIn)} \n ")
                measurementsIn.clear()
                fileIn.close()
            if heightDecode.find("Ut") != -1:
                heightOut = heightDecode.replace("Ut", "")
                heightOut = heightOut.replace("\r\n", "")
                print(heightOut)
                measurementsOut.append(float(heightOut))
            if heightDecode.find("PoseU") != -1 and len(measurementsOut) > 0:
                counterOut += 1
                fileOut = open(f"{date}Ut.csv", "a")
                maxOut = max(measurementsOut)
                maxOutList.append(float(maxOut))
                print(maxOut)
                fileOut.write(f"{counterOut}, {maxOut}, {len(measurementsOut)} \n ")
                print(f"{measurementsOut}")
                measurementsOut.clear()
                fileOut.close()

                if counterOut == counterIn:
                    maxIn2 = float(maxInList[counterOut-1])
                    maxOut2= float(maxOutList[counterIn-1])
                    compared = maxIn2 - maxOut2
                    print(f"Avvik: {compared}")
                    with open('expo.csv', 'r') as original: data = original.readlines()
                    with open('expo.csv', 'w') as modified: 
                        modified.writelines(data[0])
                        modified.write(f"{compared},{maxIn2},N/A,N/A,N/A,{maxInList[counterOut-1]}\n")
                        for i in data[1:]:
                            modified.writelines(i)
                        #modified.close()
                    
                if counterOut < counterIn and time.time() - start > 5:
                    print("Pose ikke målt på vei ut!")
                if counterOut > counterIn:
                    print("Ingen måling inn!")


    except:
        print("Something went wrong")
        return
    
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
args = vars(ap.parse_args())
PORT = args['port']

measureHeight(PORT)