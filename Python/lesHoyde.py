import serial 
import argparse
import datetime

maalingerInn = []
maalingerUt = []
counterInn = 0
counterUt = 0

# Mål høyde og skriv til fil
def maalHoyde(name):
    global counterInn, counterUt
    # Inn og ut er for å skille mellom poser som går inn og ut av systemet
    inn = "Inn"
    ut = "Ut"
    # PoseI og PoseU er for å se når posene ikke lenger er under målerene
    poseInn = "PoseI"
    poseUt = "PoseU"
    dato = datetime.datetime.now().date()

    try:
        serial_port = serial.Serial(name,9600)
        print(f"The Port name is {serial_port.name}")
        filInn = open(f"{dato}Inn.csv", "w")
        filUt = open(f"{dato}Ut.csv", "w")
        while True:
            hoyde = serial_port.readline()
            hoydeNy = hoyde.decode("utf-8")
            
            # ser etter poser som går inn
            if hoydeNy.find(inn) != -1:
                hoydeInn = hoydeNy.replace("Inn", "")
                print(hoydeInn)
                maalingerInn.append(hoydeInn)
            
            # Teller antall poser som har gått inn
            # Ber om gjennomsnittshøyden til posen og skriver til fil når posen ikke er under måleren
            if hoydeNy.find(poseInn) != -1 and len(maalingerInn) > 0:
                counterInn += 1
                gjennomsnittInn = regnGjennomsnitt(maalingerInn)
                filInn.write(f"{counterInn}, {gjennomsnittInn}, {len(maalingerInn)}\n ")
                maalingerInn.clear()
            
            # ser etter poser som går ut
            if hoydeNy.find(ut) != -1:
                hoydeUt = hoydeNy.replace("Ut", "")
                print(hoydeUt)
                maalingerUt.append(hoydeUt)
            
            # Teller antall poser som har gått ut
            # Ber om gjennomsnittshøyden til posen og skriver til fil når posen ikke er under måleren
            if hoydeNy.find(poseUt) != -1 and len(maalingerUt) > 0:
                counterUt += 1
                gjennomsnittUt = regnGjennomsnitt(maalingerUt)
                filUt.write(f"{counterUt}, {gjennomsnittUt}, {len(maalingerUt)}\n ")
                maalingerUt.clear()
                sammenlignHoyde(filInn, filUt, counterUt, dato)
    except:
        print("ERROR")
        print("Sjekk port") # Vanligste feil er portnavn
        exit()

def regnGjennomsnitt(maalinger):
    # Regner ut gjennomsnitt
    gjennomsnitt = 0
    for i in range(len(maalinger)):
        gjennomsnitt += float(maalinger[i])
    gjennomsnitt = gjennomsnitt/len(maalinger)
    return gjennomsnitt

def sammenlignHoyde(filInn, filUt, counterUt, dato):
    # Sammenligner høyden til posen som går ut med høyden til posen som gikk inn
    # Skriver til fil
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

# Argumentparser, tar inn portnavn
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
ap.add_argument("-sz","--size",required = False, help = "Enter Size of the Bag")
args = vars(ap.parse_args())

PORT = args['port']

maalHoyde(PORT)

# lengde potmeter: 5.2 cm
# sudo python3 lesHoyde.py -p "portnavn" -sz "størrelse"