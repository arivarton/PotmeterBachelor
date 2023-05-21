##
# @mainpage Description 
# Python program for reading height from potentiometer connected to Arduino and writing said data to .csv-file.
# The program also compares the heights of the bags that go in and out of the system and writes to another file that will be displayed on the GUI.
# \n Copyrigth (c) 2023 HOLDT - Hull og Lekkasje Deteksjons Teknologi. All rights reserved.

##
# @file lesHoyde.py
# @brief Python program for measuring height of snack bags.
#
# @section author_doxygen Author (s)
# - Kristoffer Solheim

# Imports
import serial 
import argparse
import datetime

maalingerInn = []
maalingerUt = []
counterInn = 0
counterUt = 0

def maalHoyde(name): 
    """!Measures height and writes to file. 
    @param name: name of the port to be used
    """
    global counterInn, counterUt
    inn = "Inn"
    ut = "Ut"
    poseInn = "PoseI"
    poseUt = "PoseU"
    dato = datetime.datetime.now().date()
    try:
        """!Try to connect to the port and creates files for writing."""
        serial_port = serial.Serial(name,9600)
        filInn = open(f"{dato}Inn.csv", "w")
        filUt = open(f"{dato}Ut.csv", "w")
        while True:
            hoyde = serial_port.readline()
            hoydeNy = hoyde.decode("utf-8")
            if hoydeNy.find(inn) != -1:
                """!Looks for bags that go in to the system."""
                hoydeInn = hoydeNy.replace("Inn", "")
                print(hoydeInn)
                maalingerInn.append(hoydeInn)
            
            if hoydeNy.find(poseInn) != -1 and len(maalingerInn) > 0:
                """!Counts the number of bags that have gone in to the system. 
                Asks for the average height of the bag and writes to file when the bag is no longer under the sensor.
                """
                counterInn += 1
                gjennomsnittInn = regnGjennomsnitt(maalingerInn)
                filInn.write(f"{counterInn}, {gjennomsnittInn}, {len(maalingerInn)}\n ")
                maalingerInn.clear()
            
            if hoydeNy.find(ut) != -1:
                """!Looks for bags that go out of the system."""
                hoydeUt = hoydeNy.replace("Ut", "")
                print(hoydeUt)
                maalingerUt.append(hoydeUt)
            
            if hoydeNy.find(poseUt) != -1 and len(maalingerUt) > 0:
                """!Counts the number of bags that have gone out of the system.
                Asks for the average height of the bag and writes to file when the bag is no longer under the sensor.                
                """
                counterUt += 1
                gjennomsnittUt = regnGjennomsnitt(maalingerUt)
                filUt.write(f"{counterUt}, {gjennomsnittUt}, {len(maalingerUt)}\n ")
                maalingerUt.clear()
                sammenlignHoyde(filInn, filUt, counterUt, dato)
    except:
        """!If it is not possible to connect to the port."""
        print("ERROR")
        print("Sjekk port") # Vanligste feil er portnavn
        exit()

def regnGjennomsnitt(maalinger):
    """!Calculates the average of the measurements that have been made on the bag.
    @param maalinger: list of measurements
    @return gjennomsnitt: average of the measurements
    """
    gjennomsnitt = 0
    for i in range(len(maalinger)):
        gjennomsnitt += float(maalinger[i])
    gjennomsnitt = gjennomsnitt/len(maalinger)
    return gjennomsnitt

def sammenlignHoyde(filInn, filUt, counterUt, dato):
    """!Compares the height of the bag on the way in and out of the system.
    Writes to file with bag number, height in, height out and leakage to be displayed on the GUI.
    @param filInn: file containing the height of the bag on the way in to the system
    @param filUt: file containing the height of the bag on the way out of the system
    @param counterUt: counter to know which bag to compare
    @param dato: date to distinguish between files
    """
    filInn = open(f"{dato}Inn.csv", "r")
    filUt = open(f"{dato}Ut.csv", "r")
    inn = filInn.readlines()
    ut = filUt.readlines()
    lekkasje = float(inn[counterUt][1]) - float(ut[counterUt][1])
    filSammenlign = open(f"{dato}Sammenlign.csv", "a")
    filSammenlign.write(f"{counterUt}, {[counterUt][1]}, {ut[counterUt][1]}, {lekkasje}\n") 
    filInn.close()
    filUt.close()
    filSammenlign.close()

"""!Argumentparser for port name and bag size."""
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
ap.add_argument("-sz","--size",required = False, help = "Enter Size of the Bag")
args = vars(ap.parse_args())

PORT = args['port']

maalHoyde(PORT)