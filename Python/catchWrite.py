import argparse
import serial

parser = argparse.ArgumentParser(
        prog='Bagheight reader',
        description='Catch potmeter values from arduino and write out highest value to file')
parser.add_argument('-p', '--port', required=True)
parser.add_argument('-l', '--length', required=False)
parser.add_argument('-t', '--timeout', type=int, default=0)

args = parser.parse_args()

feil_inn = 3
feil_ut = 55

try:
    inn_liste = []
    ut_liste = []
    ser = serial.Serial(args.port)
    ser.baudrate = 9600

    while True:
        inn_ut = ser.readline().strip().decode('utf-8')
        if inn_ut == 'Inn:':
            inn_liste.append(int(ser.readline().strip().decode('utf-8')))
        elif inn_ut == 'Ut:':
            ut_liste.append(int(ser.readline().strip().decode('utf-8')))

except KeyboardInterrupt:
    ser.close()
    inn_verdi = 1024-feil_inn
    ut_verdi = 1024-feil_ut
    print(inn_verdi - min(inn_liste))
    print(ut_verdi - min(ut_liste))
    #40mm
    justert_inn_verdi = inn_verdi + 60
    justert_ut_verdi = ut_verdi - 60
    print('Justert inn verdi (40mm kloss)')
    print(justert_inn_verdi - min(inn_liste))
    print('Justert ut verdi (40mm kloss)')
    print(justert_ut_verdi - min(ut_liste))



    #  print('\n\nHoyeste inn verdi')
    #  print(inn_verdi - min(inn_liste))
    #  print('I mm:')
    #  print((50/inn_verdi) * (inn_verdi - min(inn_liste)))
    #  print((50/1024) * (1024 - min(inn_liste)))
    #  print('\n\nHoyeste ut verdi')
    #  print(ut_verdi - min(ut_liste))
    #  print('I mm:')
    #  print((50/ut_verdi) * (ut_verdi - min(ut_liste)))
