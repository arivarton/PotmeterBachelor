import argparse
import datetime
import pickle
import os.path
import csv

import serial
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
        prog='Bagheight reader',
        description='Catch potmeter values from arduino and write out highest value to file')
parser.add_argument('-p', '--port', required=True)
parser.add_argument('-l', '--length', required=False)
parser.add_argument('-d', '--delay', type=float, default=5)
parser.add_argument('--cal', type=float, default=0,
                    help='Manuell kalibrerings verdi. (Maal med skyvelaer og finn differansen\
                            mellom hoydepunktene, se instruksjoner for potmeter kalibrering som\
                            finnes som et A4 ark ved prototypen.)'
                    )
parser.add_argument('-ac', '--auto_cal', action='store_true', help='Automatisk kalibrering.')

args = parser.parse_args()

feil_inn = 3
feil_ut = 55

inn_verdi = 1024
ut_verdi = 1024

kal_x = 26.5
auto_kal_fil = 'kal.pickle'

def skriv_csv(h_inn, h_inn_byte, h_ut, h_ut_byte, delta, delta_byte):
    file_name = '/home/radxa/SRRP-GUI/build/tests/data.csv'
    def lag_rad(k1, k2, k3, k4, k5, k6, append=True):
        if append:
            access_mode = 'a'
        else:
            access_mode = 'w'
        with open(f'{file_name}', access_mode, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([k1, k2, k3, k4, k5, k6])

    if not os.path.isfile(file_name):
        lag_rad('Inn (mm)', 'Inn (byte)', 'Ut (mm)',
                'Ut (byte)', 'Delta (mm)', 'Delta(byte)',
                append=False)

    lag_rad(h_inn, h_inn_byte, h_ut, h_ut_byte, delta, delta_byte)


def print_justerte(verdier, kal):
    print('--------------')
    justert_inn_verdi = verdier[0] + kal[0]
    justert_ut_verdi = verdier[1] - kal[0]

    #inn_hoyde = kal[1] + ((justert_inn_verdi - kal[2]) * (50/inn_verdi))
    inn_hoyde = kal[1] + ((verdier[0] - kal[2]) * (50/inn_verdi))
    #ut_hoyde = kal[1] + ((justert_ut_verdi - kal[3]) * (50/ut_verdi))
    ut_hoyde = kal[1] + ((verdier[1] - kal[3]) * (50/ut_verdi))

    print('Original inn verdi (byte):', verdier[0])
    print('Justert inn verdi:', justert_inn_verdi, '(byte)', inn_hoyde, '(mm)')

    print('Original ut verdi (byte):', verdier[1])
    print('Justert ut verdi:', justert_ut_verdi, '(byte)', ut_hoyde, '(mm)')

    delta = str((justert_ut_verdi-justert_inn_verdi)*(50/1024))
    delta_byte = justert_ut_verdi-justert_inn_verdi

    print('mm forskjell: %s' % str((justert_ut_verdi-justert_inn_verdi)*(50/1024)) )
    print('--------------\n')
    skriv_csv(inn_hoyde, justert_inn_verdi, ut_hoyde, justert_ut_verdi, delta, delta_byte)

def les_hoyeste(delay=args.delay, graph=True):
    try:
        run = True
        inn_liste = []
        inn_tid = []
        ut_liste = []
        ut_tid = []
        ser = serial.Serial(args.port)
        ser.baudrate = 9600
        start_time = datetime.datetime.now()

        while run:
            try:
                inn_ut = ser.readline().strip().decode('utf-8')
                run_time = datetime.datetime.now() - start_time
                if inn_ut == 'Inn:':
                    inn_liste.append(int(ser.readline().strip().decode('utf-8')))
                    inn_tid.append(float(str(run_time.seconds) + '.' + str(run_time.microseconds)))
                elif inn_ut == 'Ut:':
                    ut_liste.append(int(ser.readline().strip().decode('utf-8')))
                    ut_tid.append(float(str(run_time.seconds) + '.' + str(run_time.microseconds)))
                if delay != 0:
                    if delay <= float(str(run_time.seconds) + '.' + str(run_time.microseconds)):
                        run = False
            except (UnicodeDecodeError, ValueError):
                pass

    except KeyboardInterrupt:
        ser.close()

    ser.close()
    if graph:
        print('Loading graphs...')

        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('Hoydemalinger over tid')
        ax1.plot(sorted(inn_tid), [-i for i in inn_liste])
        ax1.set_title('Inn')
        ax1.set(ylabel='Hoyde')
        ax2.plot(sorted(ut_tid), [-i for i in ut_liste])
        ax2.set_title('Ut')
        ax2.set(xlabel='Tid', ylabel='Hoyde')
        fig.savefig('inn_plot.pdf')

    return (inn_verdi - min(inn_liste), ut_verdi - min(ut_liste))

def auto_kal():
    kal_klosse_h = float(input('Hoyde pa kalibrerings kloss: '))
    input('Sett kalibrerings kloss under "inn" potmeter og trykk enter')
    inn_verdi = les_hoyeste(delay=3)[0]
    input('Sett kalibrerings kloss under "ut" potmeter og trykk enter')
    ut_verdi = les_hoyeste(delay=3)[1]
    print('Inn:', inn_verdi, 'Ut:', ut_verdi)
    verdier = (inn_verdi, ut_verdi)

    kal = (round((max(verdier)-min(verdier))/2), kal_klosse_h, inn_verdi, ut_verdi)

    print('Kalibrerings verdi:', kal)
    with open(auto_kal_fil, 'wb') as f:
        pickle.dump(kal, f)
    print(f'Kalibrerings verdi lagret i {auto_kal_fil}')
    print_justerte(verdier, kal)

    return kal

# Hvis automatisk kalibrering kjor dette forst
if args.auto_cal:
    if os.path.isfile(auto_kal_fil):
        sp = 'x'
        while(sp.lower() not in ('y', 'n', '')):
            sp = input(f'Auto kalibrerings fil {auto_kal_fil} finnes, vil du lage en ny? [y/N]\n')
            if sp.lower() == 'y':
                kal = auto_kal()
            elif sp.lower() in ('n', ''):
                with open(auto_kal_fil, 'rb') as f:
                    kal = pickle.load(f)
                    print('Eksisterende kalibrerings verdi er:', kal)
            else:
                print('Kun [y/N] er aksepterte verdier.')
    else:
        kal = auto_kal()
else:
    kal = round((args.cal * kal_x)/2)

#verdier = les_hoyeste()
#print(verdier)
#print_justerte(verdier, kal)

while True:
    sp = input(f'Les pose [Y/n] ({args.delay}s)\n')
    if sp.lower() in ('y', ''):
        verdier = les_hoyeste(args.delay)
        print_justerte(verdier, kal)
    elif sp.lower() == 'n':
        break
    else:
        print('Kun [Y/n] er aksepterte verdier.')
