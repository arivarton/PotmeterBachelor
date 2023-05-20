"""
Program for å lese høyde fra potmeter som er koblet til Arduino og skrive til fil.
Programmet sammenligner også høydene på posene som går inn og ut av systemet og skriver til fil som skal vises på GUI.
"""
import serial 
import argparse
import datetime

maalingerInn = []
maalingerUt = []
counterInn = 0
counterUt = 0

def maalHoyde(name): 
    """
    Mål høyde og skriv til fil 
    name: navnet på porten som skal brukes
    """
    global counterInn, counterUt
    inn = "Inn"
    ut = "Ut"
    poseInn = "PoseI"
    poseUt = "PoseU"
    dato = datetime.datetime.now().date()
    try:
        """
        Prøver å koble til porten
        """
        serial_port = serial.Serial(name,9600)
        print(f"The Port name is {serial_port.name}")
        filInn = open(f"{dato}Inn.csv", "w")
        filUt = open(f"{dato}Ut.csv", "w")
        while True:
            hoyde = serial_port.readline()
            hoydeNy = hoyde.decode("utf-8")
            if hoydeNy.find(inn) != -1:
                """
                Programmet ser etter poser som går inn i systemet
                """
                hoydeInn = hoydeNy.replace("Inn", "")
                print(hoydeInn)
                maalingerInn.append(hoydeInn)
            
            # Teller antall poser som har gått inn
            # Ber om gjennomsnittshøyden til posen og skriver til fil når posen ikke er under måleren
            if hoydeNy.find(poseInn) != -1 and len(maalingerInn) > 0:
                """
                Programmet teller antall poser som har gått inn i systemet
                Programmet ber om gjennomsnittshøyden til posen og skriver til fil når posen ikke er under måleren
                """
                counterInn += 1
                gjennomsnittInn = regnGjennomsnitt(maalingerInn)
                filInn.write(f"{counterInn}, {gjennomsnittInn}, {len(maalingerInn)}\n ")
                maalingerInn.clear()
            
            # ser etter poser som går ut
            if hoydeNy.find(ut) != -1:
                """ 
                Programmet ser etter poser som går ut av systemet
                """
                hoydeUt = hoydeNy.replace("Ut", "")
                print(hoydeUt)
                maalingerUt.append(hoydeUt)
            
            if hoydeNy.find(poseUt) != -1 and len(maalingerUt) > 0:
                """
                Programmet teller antall poser som har gått ut av systemet
                Programmet ber om gjennomsnittshøyden til posen og skriver til fil når posen ikke er under måleren
                """
                counterUt += 1
                gjennomsnittUt = regnGjennomsnitt(maalingerUt)
                filUt.write(f"{counterUt}, {gjennomsnittUt}, {len(maalingerUt)}\n ")
                maalingerUt.clear()
                sammenlignHoyde(filInn, filUt, counterUt, dato)
    except:
        """
        Hvis det ikke er mulig å koble til porten
        """
        print("ERROR")
        print("Sjekk port") # Vanligste feil er portnavn
        exit()

def regnGjennomsnitt(maalinger):
    """ 
    Regner ut gjennomsnittet av målingene som har blitt gjort på posen 
    maalinger: liste med målinger
    """
    gjennomsnitt = 0
    for i in range(len(maalinger)):
        gjennomsnitt += float(maalinger[i])
    gjennomsnitt = gjennomsnitt/len(maalinger)
    return gjennomsnitt

def sammenlignHoyde(filInn, filUt, counterUt, dato):
    """
    Sammenligner høyden til posen på vei inn og ut av systemet
    Skriver til fil med posenummer, høyde inn, høyde ut og lekkasje som skal vises på GUI
    filInn: filen som inneholder høyden til posen på vei inn i systemet
    filUt: filen som inneholder høyden til posen på vei ut av systemet
    counterUt: teller for å vite hvilken pose som skal sammenlignes
    dato: dato for å skille mellom filer
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

"""
Argumentparser, tar inn portnavn og størrelse på posen
"""
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
ap.add_argument("-sz","--size",required = False, help = "Enter Size of the Bag")
args = vars(ap.parse_args())

PORT = args['port']

maalHoyde(PORT)

# lengde potmeter: 5.2 cm
# sudo python3 lesHoyde.py -p "portnavn" -sz "størrelse"