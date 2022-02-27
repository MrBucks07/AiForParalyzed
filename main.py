# required dependency
import cv2
import numpy as np
from cvpackage import FaceMeshDetectionModule, commonFunction


# *******************

def drawButtons(image, btnList):
    for button in btnList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(images, (x, y), (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(images, button.text, (x + 5, y + 38), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

    return image


class Button:
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
msgList = ["Hii", "walk", "music", "sleep"]
selected = 0
for i, msg in enumerate(msgList):
    buttonList.append(Button((i * 120 + 10, 10), (100, 60), msgList[i]))

# reading camera input using cv2
camInput = cv2.VideoCapture(0)
faceDetector = FaceMeshDetectionModule.MbFaceMeshDetector(
    iMaxFaces=1,
    iMinDetectionCon=0.7
)

# face lm near eyes list
# lmList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243, ]
lmList = [130, 243, 27, 23, 463, 359, 257, 253]

lenRigList = []
lenLefList = []
avgLef = 0
avgRig = 0
counter = 0
selected = 0
count = 0
# when camera input is opened
# while camInput.isOpened():
#     success, images = camInput.read()
#     # images = btn.drawButton(images)
#     if success:
#         images, faces = faceDetector.detectFaces(images, draw=True)
#
#         # drawing points on face
#         if faces:
#             face = faces[0]
#             for lm in lmList:
#                 cv2.circle(images, face[lm], 2, (255, 0, 0), 2, cv2.FILLED)
#
#             # right dist
#             lefUp = face[159]
#             lefDown = face[23]
#             lefRight = face[130]
#             lefLeft = face[243]
#             cv2.line(images, lefUp, lefDown, (0, 255, 0), 2, cv2.FILLED)
#             cv2.line(images, lefLeft, lefRight, (0, 255, 0), 2, cv2.FILLED)
#             lenLefVer = commonFunction.getDistance(point1=lefUp, point2=lefDown)
#             lenLefHor = commonFunction.getDistance(point1=lefLeft, point2=lefRight)
#
#             # left dist
#             rigUp = face[257]
#             rigDown = face[253]
#             rigLeft = face[463]
#             rigRight = face[359]
#             cv2.line(images, rigUp, rigDown, (0, 0, 255), 2, cv2.FILLED)
#             cv2.line(images, rigLeft, rigRight, (0, 0, 255), 2, cv2.FILLED)
#             lenRigVer = commonFunction.getDistance(point1=rigUp, point2=rigDown)
#             lenRigHor = commonFunction.getDistance(point1=rigLeft, point2=rigRight)
#
#             lenRig = int((lenRigVer / lenRigHor) * 100)
#             lenLef = int((lenLefVer / lenLefHor) * 100)
#             # print(f"left : {lenLef} and right : {lenRig}")
#
#             # appending five values and taking average for left eye
#             lenLefList.append(lenLef)
#             # appending five values and taking average for right eye
#             lenRigList.append(lenRig)
#
#             if len(lenLefList) > 5:
#                 lenLefList.pop(0)
#             avgLef = sum(lenLefList) / len(lenLefList)
#
#             if len(lenRigList) > 5:
#                 lenRigList.pop(0)
#             avgRig = sum(lenRigList) / len(lenRigList)
#
#             # print(f"left : {avgLef} and right : {avgRig}")
#
#             if avgLef < 39:
#                 count = count + 1
#                 cv2.putText(images, f" RightBlink {count}", (100, 100), cv2.FONT_ITALIC, 3, (255, 255, 255), 3)
#                 counter = 1
#                 # print(avgLef)
#                 # if selected == 0:
#                 #     selected = 1
#                 #     counter = 2
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 #
#                 # if selected == 1:
#                 #     selected = 2
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 #
#                 # if selected == 2:
#                 #     selected = 3
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 # cv2.putText(images, "RIGHT", (100, 100), cv2.FONT_ITALIC, 2, (0, 0, 255), 2)
#                 # counter = 1
#
#             # if avgRig < 39:
#                 # if selected == 1:
#                 #     selected = 0
#                 #     counter = 2
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 #
#                 # if selected == 2:
#                 #     selected = 1
#                 #     counter = 2
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 #
#                 # if selected == 3:
#                 #     selected = 2
#                 #     counter = 2
#                 # if counter != 0:
#                 #     counter += 1
#                 #     if counter > 10:
#                 #         counter = 0
#                 #
#                 # print(avgRig)
#                 # cv2.putText(images, "LEFT", (100, 100), cv2.FONT_ITALIC, 2, (0, 0, 255), 2)
#                 # counter = 1
#             cv2.putText(images, f" RightBlink {count}", (10, 100), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
#             if counter != 0:
#                 counter += 1
#                 if counter > 10:
#                     counter = 0
#
#         if selected == 0:
#             cv2.rectangle(images, (10 +(120 * 0), 10), (110 +(120 * 0), 70), (0, 0, 0), 10)
#         if selected == 1:
#             cv2.rectangle(images, (10 +(120 * 1), 10), (110 +(120 * 1), 70), (0, 0, 0), 10)
#         if selected == 2:
#             cv2.rectangle(images, (10 +(120 * 2), 10), (110 +(120 * 2), 70), (0, 0, 0), 10)
#         if selected == 3:
#             cv2.rectangle(images, (10 +(120 * 3), 10), (110 +(120 * 3), 70), (0, 0, 0), 10)
#
#     # final image output
#     # images = cv2.flip(images, 1)
#     images = drawButtons(images, buttonList)
#     cv2.imshow("WebCam", images)
#     cv2.waitKey(1)

lefCount = 0
rigCount = 0
counter = 0
lefRatioList = []
rigRatioList = []
lefRatioAvg = 0
rigRatioAvg = 0
selected = 0
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

            if lefRatioAvg < 18 and rigRatioAvg < 22:
                print(msgList[selected])
            # print(f"left : {int(lefRatioAvg)} and right : {int(rigRatioAvg)}")
            if counter == 0:
                if lefRatioAvg < 18:
                    if selected > 1:
                        selected = selected - 1
                    counter = 1

            if counter == 0:
                if rigRatioAvg < 22:
                    if selected < 3:
                        selected = selected + 1
                    counter = 1
            if counter != 0:
                counter += 1
                if counter == 10:
                    counter = 0

            # ******************* block end *******************

            if selected == 0:
                cv2.rectangle(images, (10, 10), (110, 70), (0, 0, 0), 10)
            if selected == 1:
                cv2.rectangle(images, (10 + 120, 10), (110 + 120, 70), (0, 0, 0), 10)
            if selected == 2:
                cv2.rectangle(images, (10 + 240, 10), (110 + 240, 70), (0, 0, 0), 10)
            if selected == 3:
                cv2.rectangle(images, (10 + 360, 10), (110 + 360, 70), (0, 0, 0), 10)
        # cv2.rectangle(images, (10 + 120, 10), (110 + 120, 70), (0, 0, 0), 10)
        # final image output
        # images = cv2.flip(images, 1)
        images = drawButtons(images, buttonList)
        # print(selected)
        cv2.imshow("WebCam", images)
        cv2.waitKey(1)
