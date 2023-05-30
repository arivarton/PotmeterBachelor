import serial

serial_port = serial.Serial("/dev/cu.usbmodem113101",9600)
while True:
    if heightDecode.find("Inn") != -1:
        height = serial_port.readline()
        heightDecode = height.decode("utf-8")
        print(heightDecode)