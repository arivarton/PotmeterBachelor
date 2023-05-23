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
import csv

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
    sammenlignetListe = []
    maxUt = []
    maxInn = []
    dato = datetime.datetime.now().date()
    try:
        """!Try to connect to the port and creates files for writing."""
        serial_port = serial.Serial(name,9600)

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
                filInn = open(f"{dato}Inn.csv", "a")
                maxInn.append(max(maalingerInn))
                filInn.write(f"{counterInn}, {maxInn[counterInn]}, {gjennomsnittInn}, {len(maalingerInn)}\n ")
                maalingerInn.clear()
                filInn.close()
            
            if hoydeNy.find(ut) != -1:
                """!Looks for bags that go out of the system."""
                hoydeUt = hoydeNy.replace("Ut", "")
                print(hoydeUt)
                maalingerUt.append(hoydeUt)
            
            if hoydeNy.find(poseUt) != -1 and len(maalingerUt) > 0:
                """!Counts the number of bags that have gone out of the system.
                Asks for the average height of the bag and writes to file when the bag is no longer under the sensor.                
                """
                filUt = open(f"{dato}Ut.csv", "a")
                counterUt += 1
                #gjennomsnittUt = regnGjennomsnitt(maalingerUt)
                maxUt.append(max(maalingerUt))
                filUt.write(f"{counterUt}, {maxUt[counterUt]}, {len(maalingerUt)}\n ")
                maalingerUt.clear()
                filUt.close()
                # compare height of bag in and bag out without using "sammenlignHoyde()" with
                if counterInn == counterUt or counterInn > counterUt:
                    filSammenlignet = open(f"{dato}Sammenlignet.csv", "a")
                    sammenlignet = float(maxInn[counterUt-1]) - float(maxUt[counterUt-1])
                    sammenlignetListe.append(sammenlignet)
                    if sammenlignetListe[counterUt-1] < 1:
                        filSammenlignet.write(f"{counterUt}, {sammenlignet}, Godkjent\n")
                        print(f"Godkjent: {sammenlignet}")
                        filSammenlignet.close()
                    else:
                        filSammenlignet.write(f"{counterUt}, {sammenlignet}, Underkjent\n")
                        print(f"Underkjent: {sammenlignet}")
                        filSammenlignet.close()

                else:
                    # dont crash
                    print("Fillern")

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

def sammenlignHoyde():
    dato = datetime.datetime.now().date()
    inn = []
    ut = []
    sammenlignetListe = []
    kvalitet = []
    antallPoser = 0
    filInn = csv.reader(f"{dato}Inn.csv", delimiter=",")
    filUt = csv.reader(f"{dato}Ut.csv", delimiter=",")

    with open(f"{dato}Inn.csv", "r") as filInn:
        innLes = csv.reader(filInn, delimiter=",")
        for row in innLes:
            inn.append(row)
    with open(f"{dato}Ut.csv", "r") as filUt:
        utLes = csv.reader(filUt, delimiter=",")
        for row in utLes:
            ut.append(row)

    # sjekk om inn[i][1] == ut[i][1]
    for i in range(len(inn)):
        sammenlignet = float(inn[i][1]) - float(ut[i][1])
        sammenlignetListe.append(sammenlignet)
        if inn[i][1] == ut[i][1]: # juster
            print("Jippi")
            kvalitet.append("Godkjent")
        else:
            print("Fillern")
            kvalitet.append("Underkjent")

    """print(sammenlignetListe)
    for i in range(len(utLes)):
        sammenlignetFil = open(f"{dato}Sammenlignet.csv", "a")
        antallPoser += 1
        sammenlignetFil.write(f"{antallPoser}, {sammenlignetListe[i]}, {kvalitet[i]} \n")
        sammenlignetFil.close()"""

    
    

"""!Argumentparser for port name and bag size."""
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
args = vars(ap.parse_args())
PORT = args['port']

maalHoyde(PORT)
