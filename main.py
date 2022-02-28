# Author : Kartik Panchal
# required dependency
from time import sleep
import cv2
import serial
from cvpackage import FaceMeshDetectionModule, commonFunction


# *******************

# function to draw buttons
def drawButtons(image, btnList):
    for button in btnList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(images, (x, y), (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(images, button.text, (x + 5, y + 38), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

    return image


# class to set button initial properties
class Button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text


# button list
buttonList = []
# message list
msgList = ["LON", "WALK", "MUSIC", "LOFF"]
for i, msg in enumerate(msgList):
    buttonList.append(Button((i * 120 + 10, 10), (100, 60), msgList[i]))

# reading camera input using cv2
camInput = cv2.VideoCapture(0)
faceDetector = FaceMeshDetectionModule.MbFaceMeshDetector(
    iMaxFaces=1,
    iMinDetectionCon=0.7
)
# serial obj to communicate with arduino
serialCom = serial.Serial(port="COM4", baudrate=9600, bytesize=8)
data = ""
send = False

# important variables
counter = 0
lefRatioList = []
rigRatioList = []
lefRatioAvg = 0
rigRatioAvg = 0
selected = 0
# *******************

while camInput.isOpened():
    success, images = camInput.read()

    if success:
        images, faceLm = faceDetector.detectFaces(images)
        if faceLm:
            # taking first face landmarks
            face = faceLm[0]

            # drawing vertical and horizontal line on right eye
            rigUp = face[159]
            rigDown = face[145]
            rigLeft = face[133]
            rigRight = face[33]
            cv2.line(images, rigUp, rigDown, (0, 0, 0), 2)
            cv2.line(images, rigLeft, rigRight, (0, 0, 0), 2)
            # ******************* block end *******************

            # drawing vertical and horizontal line on left eye
            lefLeft = face[463]
            lefRight = face[359]
            lefUp = face[386]
            lefDown = face[374]
            cv2.line(images, lefUp, lefDown, (0, 0, 0), 2)
            cv2.line(images, lefLeft, lefRight, (0, 0, 0), 2)
            # ******************* block end *******************

            # calculating horizontal and vertical distance of both eyes
            lefVerLen = commonFunction.getDistance(point1=lefUp, point2=lefDown)
            lefHorLen = commonFunction.getDistance(point1=lefLeft, point2=lefRight)
            rigVerLen = commonFunction.getDistance(point1=rigUp, point2=rigDown)
            rigHorLen = commonFunction.getDistance(point1=rigLeft, point2=rigRight)
            # ******************* block end *******************

            # calculating ratio of hor / ver of both eyes
            lefRatio = int((lefVerLen / lefHorLen) * 100)
            rigRatio = int((rigVerLen / rigHorLen) * 100)

            lefRatioList.append(lefRatio)
            rigRatioList.append(rigRatio)

            if len(lefRatioList) > 5:
                lefRatioList.pop(0)
            lefRatioAvg = sum(lefRatioList) / len(lefRatioList)
            if len(rigRatioList) > 5:
                rigRatioList.pop(0)
            rigRatioAvg = sum(rigRatioList) / len(rigRatioList)

            if counter == 0:
                if lefRatioAvg < 17:
                    if selected > 0:
                        selected = selected - 1
                    counter = 1

            if counter == 0:
                if rigRatioAvg < 21:
                    if selected < 3:
                        selected = selected + 1
                    counter = 1
            if counter != 0:
                counter += 1
                if counter == 10:
                    counter = 0

            # ******************* block end *******************

            # updating selected button according to eye blink
            if selected == 0:
                cv2.rectangle(images, (10, 10), (110, 70), (0, 0, 0), 10)
            if selected == 1:
                cv2.rectangle(images, (10 + 120, 10), (110 + 120, 70), (0, 0, 0), 10)
            if selected == 2:
                cv2.rectangle(images, (10 + 240, 10), (110 + 240, 70), (0, 0, 0), 10)
            if selected == 3:
                cv2.rectangle(images, (10 + 360, 10), (110 + 360, 70), (0, 0, 0), 10)
            # ******************* block end *******************

            # if both eyes are closed perform action
            if lefRatioAvg < 20 and rigRatioAvg < 22:
                if selected == 0:
                    send = False
                    data = "ON"
                    if not send:
                        serialCom.write(data.encode("utf-8"))
                        send = True
                        sleep(1.5)

                if selected == 3:
                    if send:
                        send = False
                    data = "OFF"
                    if not send:
                        serialCom.write(data.encode("utf-8"))
                        send = True
                        sleep(2)
            # ******************* block end *******************

        # final image output
        images = drawButtons(images, buttonList)
        # print(selected)
        cv2.imshow("WebCam", images)
        cv2.waitKey(1)
