import datetime
import csv

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
        print(inn)
    with open(f"{dato}Ut.csv", "r") as filUt:
        utLes = csv.reader(filUt, delimiter=",")
        for row in utLes:
            ut.append(row)
        print(ut)

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

    print(sammenlignetListe)
    for i in range(len(sammenlignetListe)):
        sammenlignetFil = open(f"{dato}Sammenlignet.csv", "a")
        antallPoser += 1
        sammenlignetFil.write(f"{antallPoser}, {sammenlignetListe[i]}, {kvalitet[i]} \n")
        sammenlignetFil.close()

    """for row in filInn:
        inn.append(filInn[1][1])
        print(inn)
    for row in filUt:
        ut.append(row)

    for i in range(len(inn)):
        if inn[i] - ut[i] == 0:
            print("Jippi")
        else:
            print("Fillern")"""
            
        

    """lekkasje = float(inn[counter][1]) - float(ut[counter][1])
    filSammenlign = open(f"{dato}Sammenlign.csv", "a")
    filSammenlign.write(f"{counter}, {inn[counter][0]}, {ut[counter][0]}, {lekkasje}\n") 
    filSammenlign.close()"""

sammenlignHoyde()

