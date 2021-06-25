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

    # spring()


def objectdetectionbottom():
    # object Detection Code
    pictogramfound = 0

    return pictogramfound


def spring():
    command = "Servo SetTrigger 90\n"
    sendCommand(command)

    # just testings
    command = "Servo GetTrigger\n"
    sendCommand(command)

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

    return


def objectdetectiontop():
    # object Detection Code

    return 0


def searchpictogramtop():
    pictogramfound = objectdetectiontop()
    pictogramfound = 0
    while pictogramfound < 2:
        command = "Mot Angle 30, 10\n"
        sendcommand = command.encode('utf-8')
        ser.write(sendcommand)
        time.sleep(1)
        pictogramfound = pictogramfound + 1
        print("motor hat sich gedreht")

        # pictogramfound = objectdetectiontop()

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
