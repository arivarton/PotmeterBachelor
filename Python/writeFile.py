# read 

with open("measurementsIn.csv", "r") as original1: data1 = original1.readlines()
with open("measurementsOut.csv", "r") as original2: data2 = original2.readlines()

with open("measurements.csv", "w") as modified:
    modified.write("Inn,Ut\n")
    for i in range(len(data1)):
        modified.write(f"{data1[i].replace(',', '')},{data2[i].replace(',', '')}")
