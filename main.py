# required dependency
import cv2
from cvpackage import FaceMeshDetectionModule, commonFunction

# *******************


# reading camera input using cv2
camInput = cv2.VideoCapture(0)
faceDetector = FaceMeshDetectionModule.MbFaceMeshDetector(
    iMaxFaces=1,
    iMinDetectionCon=0.7
)

# face lm near eyes list
# lmList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243, ]
lmList = [130, 243, 27, 23, 463, 359, 257, 253]
selected = 0

# when camera input is opened
while camInput.isOpened():
    success, images = camInput.read()

    if success:
        images, faces = faceDetector.detectFaces(images)

        # drawing points on face
        if faces:
            face = faces[0]
            for lm in lmList:
                cv2.circle(images, face[lm], 2, (255, 0, 0), 2, cv2.FILLED)

            # right dist
            lefUp = face[27]
            lefDown = face[23]
            cv2.line(images, lefUp, lefDown, (0, 255, 0), 2, cv2.FILLED)
            lenRigVer = commonFunction.getDistance(point1=lefUp, point2=lefDown)

            # left dist
            rigUp = face[257]
            rigDown = face[253]
            lenLefVer = commonFunction.getDistance(point1=rigUp, point2=rigDown)
            cv2.line(images, rigUp, rigDown, (0, 0, 255), 2, cv2.FILLED)

            cv2.rectangle(images, (50, 50), (100, 100), (0, 220, 0), cv2.FILLED),
            cv2.rectangle(images, (150, 50), (200, 100), (0, 220, 0), cv2.FILLED)

            if lenRigVer < 18:
                selected += 1
                # cv2.putText(images, "Right", (50, 50), fontFace=cv2.FONT_ITALIC, fontScale=1, color=(200, 0, 0),
                #             thickness=2)
            if lenLefVer < 17:
                selected -= 1
                # cv2.putText(images, "Left", (50, 50), fontFace=cv2.FONT_ITALIC, fontScale=1, color=(200, 0, 0),
                #             thickness=2)

            print(selected)
            # cv2.rectangle(images, (50, 50), (100, 100), (0, 0, 0), 3, None)
            if selected == 0:
                cv2.rectangle(images, (150, 50), (200, 100), (0, 0, 0), 3, None)
            if selected > 0:
                cv2.rectangle(images, (50, 50), (100, 100), (0, 0, 0), 3, None)
            if selected < 0:
                cv2.rectangle(images, (150, 50), (200, 100), (0, 0, 0), 3, None)

    # final image output
    images = cv2.flip(images, 1)
    cv2.imshow("WebCam", images)
    cv2.waitKey(1)
