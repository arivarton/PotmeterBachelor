import random


compared = float(100.0) - float(97.4)
print(f"Avvik: {compared}")
leakage = random.random()
reasons = ["Chip i søm", "Hull i pose", "Pose ikke lukket"]
reasonNumber = random.randint(0,2)
measurements = random.randint(60, 100)

"""fileCompared = open(f"Python/expo.csv", "a")
fileCompared.write(f"{compared},{100},{leakage},{reasons[reasonNumber]},Hvertfall 60cm. Minst! ,{measurements}\n")
fileCompared.close()"""

# write to second line in file
fileCompared = open(f"Python/expo.csv", "a")
with open('expo.csv', 'r') as original: data = original.readlines()
with open('expo.csv', 'w') as modified: 
    
    modified.writelines(data[0])
    modified.write("Hallaballa\n")
    for i in data[1:]:
        modified.writelines(i)
    
    
    
        

