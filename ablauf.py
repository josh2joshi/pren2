import serial
import time

# port = "COM3"
port = "/dev/ttyACM1"  # USB2
ser = serial.Serial(port=port, baudrate=57600, timeout=1, write_timeout=5)
ser.flushInput()



def readLine():
    read = ser.readline()
    decoded = read.decode('utf-8')
    return decoded


def sendCommand(comand):
    sendcommand = comand.encode('utf-8')
    ser.write(sendcommand)
    ser.flushInput()
    time.sleep(1)


def main():
    print("Main Program")

    command = "InitTerm\n"
    sendCommand(command)
    print("Tiny say: ", readLine())

    print("Tiny say: ", readLine())

    command = "Servo GetTrigger\n"
    sendCommand(command)

    print("Tiny say: ", readLine())

    command = "Servo GetCam\n"
    sendCommand(command)

    print("Cam Position: ", readLine())

    # enable usensors
    command = "USens Init\n"
    sendCommand(command)

    command = "USens SetUSEnableFront 1\n"
    sendCommand(command)

    command = "USens SetUSEnableBottom 1\n"
    sendCommand(command)

    command = "USens GetDistanceFront\n"
    sendCommand(command)
    print(readLine())

    searchPictogram()
    spring()
    setcamtop()
    searchpictogramtop()


def searchPictogram():
    turn = 0
    picFound = objectdetectionbottom()
    while picFound < 1:
        if picFound < 1:
            command = "Mot Angle 30, 10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            turn = turn + 1
            time.sleep(1)
        else:
            picFound = 1
    while turn > 0:
        command = "Mot Angle -30, 10\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        turn = turn - 1
        time.sleep(1)
    positionbottom()

def objectdetectionbottom():
    # object Detection Code
    pictogramfound = 0

    return pictogramfound

def positionbottom():
    import sys
    sys.path.append("./StairDedection")
    import StairDetectionForRaspi

    positionTreppe = dedectStair()
    if positionTreppe == -1:
        print("ERROR TREPPE NICHT GEFUNDEN")
    elif positionTreppe == 0:
        while positionTreppe == 0:
            command = "Mot Angle 90, 10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(1)
            command = "Mot Dis 50,10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(2)
            command = "Mot Angle -90, 10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(1)
            positionTreppe = dedectStair()
    else:
        while positionTreppe == 1:
            command = "Mot Angle -90, 10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(1)
            command = "Mot Dis 50,10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(2)
            command = "Mot Angle 90, 10\n"
            sendcommand = command.encode('utf-8')
            ser.write(sendcommand)
            time.sleep(1)
            positionTreppe = dedectStair()
    distancefront = getdistancefront()
    while distancefront > 100:
        command = "Mot Dis 50,10\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        time.sleep(2)
        distancefront = getdistancefront()
    command = "Mot Dis -500,10\n"
    sendcommand = command.encode('utf-8')
    ser.write(sendcommand)
    time.sleep(10)
    return

def spring():
    command = "Servo SetTrigger 90\n"
    sendcommand = command.encode('utf-8')
    ser.write(sendcommand)
    time.sleep(10)


    print("Trigger Position: ", readLine())
    return



def setcamtop():
    print("start setcamtop")
    command = "USens GetDistanceBottom\n"
    sendcommand = command.encode('utf-8')
    ser.write(sendcommand)
    rcv = readLine(ser)
    time.sleep(2)
    rcv = str(rcv, 'utf-8')
    rcv = int(rcv)
    print("distance Sensor Bottom: ", rcv)
    if rcv < 100:
        command = "Servo SetCam 80\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        print("cam nach oben setzen")
    else:
        command = "Servo SetCam 70\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        print("cam nach unten setzen")
    time.sleep(1)
    return


def objectdetectiontop():
    # object Detection Code

    return 0


def searchpictogramtop():
    pictogramfound = objectdetectiontop()
    while pictogramfound == 0:
        command = "Mot Angle 30, 10\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        time.sleep(1)
        pictogramfound = objectdetectiontop()
        print("motor hat sich gedreht")

    distancefront = getdistancefront()

    while distancefront > 60:
        command = "Mot Dis 20,10\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        time.sleep(2)
        print("fährt vorwärts")
        distancefront = getdistancefront()

    command = "led set 1\n"
    sendcommand = command.encode('utf-8')
    ser.write(sendcommand)
    print("led läuchtet hell yea >.<")

    return


def getdistancefront():
    command = "USens GetDistanceFront\n"
    sendcommand = command.encode('utf-8')
    ser.write(sendcommand)
    rcv = readLine(ser)
    time.sleep(2)
    rcv = str(rcv, 'utf-8')
    rcv = int(rcv)
    return rcv


main()
