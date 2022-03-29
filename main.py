# Author : Kartik Panchal
# required dependency
from time import sleep
import cv2
import numpy as np
import serial
import smtplib
from cvpackage import FaceMeshDetectionModule, commonFunction
from twilio.rest import Client

# *******************

# logic to send sms using twilio
accSid = "ACd7c443e0dd312e639d30a03e296cf0aa"
authToken = "7f2d356aaac5532fdf259da03443a7aa"


# function to draw buttons
def drawButtons(image, btnList):
    for button in btnList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(images, (x, y), (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(images, button.text, (x + 10, y + 38), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

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
msgList = [["LON", "LOFF", "SLEEP"],
           ["MUSIC", "BUZZ", "EME"]]
for i in range(len(msgList)):
    for j, msg in enumerate(msgList[i]):
        buttonList.append(Button(((130 * j) + 10, 10 + (i * 70)), (120, 60), msg))

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
# on = False

# important variables
counter = 0
msgCounter = 0
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

            # if both eyes are closed perform action
            if lefRatioAvg < 19 and rigRatioAvg < 21:
                if selected == 0:
                    send = False
                    data = "ON"
                    if not send:
                        serialCom.write(data.encode("utf-8"))
                        print(data)
                        send = True
                        sleep(0.6)

                if selected == 1:
                    msgCounter = 0
                    if send:
                        send = False
                    data = "OFF"
                    if not send:
                        serialCom.write(data.encode("utf-8"))
                        print(data)
                        send = True
                        sleep(0.6)

                if selected == 5:
                    if msgCounter == 0:
                        msgCounter = 1
                        if send:
                            send = False
                        if not send:
                            send = True
                            client = Client(accSid, authToken)
                            message = client.messages.create(
                                from_="+12348039084",
                                to="+917984881897",
                                body="Come fast to hospital"
                            )
                            print(message)
                            sleep(1.6)

                if selected == 4:
                    if send:
                        send = False
                    if not send:
                        data = "BON"
                        serialCom.write(data.encode("utf-8"))
                        print("BON")
                        send = True
                        sleep(1.6)

            # ******************* block end *******************

            if counter == 0:
                if lefRatioAvg < 16:
                    if rigRatioAvg > 18:
                        if selected > 0:
                            selected = selected - 1
                        counter = 1

            if counter == 0:
                if rigRatioAvg < 20:
                    if lefRatioAvg > 15:
                        if selected < 5:
                            selected = selected + 1
                        counter = 1
            if counter != 0:
                counter += 1
                if counter == 10:
                    counter = 0
            # ******************* block end *******************

            # updating selected button according to eye blink
            if selected == 0:
                cv2.rectangle(images, (10, 10), (130, 70), (0, 255, 0), 10)
            if selected == 1:
                cv2.rectangle(images, (10 + 130, 10), (130 + 130, 70), (0, 255, 0), 10)
            if selected == 2:
                cv2.rectangle(images, (10 + 260, 10), (130 + 260, 70), (0, 255, 0), 10)
            if selected == 3:
                cv2.rectangle(images, (10, 10 + 70), (130, 70 + 70), (0, 255, 0), 10)
            if selected == 4:
                cv2.rectangle(images, (10 + 130, 10 + 70), (130 + 130, 70 + 70), (0, 255, 0), 10)
            if selected == 5:
                cv2.rectangle(images, (10 + 260, 10 + 70), (130 + 260, 70 + 70), (0, 255, 0), 10)
            # ******************* block end *******************

        # final image output
        # cv2.flip(images, 1)
        images = drawButtons(images, buttonList)
        # print(selected)
        cv2.imshow("WebCam", images)
        cv2.waitKey(1)
