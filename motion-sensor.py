
pos = new linkedList()

pos.add(sensor.data)

while True:
    pos.add(sensor.data)
    if (pos.getsecondlast.angle > pos.getlast.angle):
        break

while True:
    x = sensor.data
    b = False
    for i in pos:
        if (i == "is close to x"):
            b = True
    if (b == False):
        sendSignal(x)

def sendSignal(x):
    sendRosSignal(x)
