import serial 
import argparse

maalingerInn = []
maalingerUt = []
counterInn = 0
counterUt = 0

# Mål høyde og skriv til fil
def maalHoyde(name):
    global counterInn, counterUt
    inn = "Inn"
    ut = "Ut"
    poseInn = "PoseI"
    poseUt = "PoseU"

    try:
        serial_port = serial.Serial(name,9600)
        print(f"The Port name is {serial_port.name}")
        f = open("dataInn.csv", "a")
        g = open("dataUt.csv", "a")
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
                f.write(f"{counterInn}, {gjennomsnittInn}, {len(maalingerInn)}\n ")
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
                g.write(f"{counterUt}, {gjennomsnittUt}, {len(maalingerUt)}\n ")
                maalingerUt.clear()
    except:
        print("ERROR")
        print("Sjekk port")
        exit()

def regnGjennomsnitt(maalinger):
    #regner ut gjennomsnitt
    gjennomsnitt = 0
    for i in range(len(maalinger)):
        gjennomsnitt += float(maalinger[i])
    gjennomsnitt = gjennomsnitt/len(maalinger)
    return gjennomsnitt

# Argumentparser, tar inn portnavn
ap = argparse.ArgumentParser()
ap.add_argument("-p","--port",required = True, help = "Enter Port Name")
args = vars(ap.parse_args())

PORT = args['port']

maalHoyde(PORT)

# lengde potmeter: 5.2 cm