import serial

serial_port = serial.Serial("/dev/cu.usbmodem113101",9600)
while True:
    with open("SystemHeight.txt", "r") as original: data = original.readlines()
    
    rise = serial_port.readline()
    riseDecode = rise.decode("utf-8")
    if riseDecode.find("UP") != -1:
        modified = open("SystemHeight.txt", "w")
        newHeight = riseDecode.replace("UP", "")
        newHeight = float(newHeight) + float(data[0])
        modified.writelines(f"{newHeight}")
        modified.close()
    elif riseDecode.find("DOWN") != -1:
        modified = open("SystemHeight.txt", "w")
        newHeight = riseDecode.replace("DOWN", "")
        newHeight = float(data[0]) - float(newHeight)
        modified.writelines(f"{newHeight}")
        modified.close()