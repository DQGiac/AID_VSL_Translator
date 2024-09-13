import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
test = 0
starttime = time.time()
xy = []
move = "n"
while True:
    _, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img, draw=True)
    if hands:
        x, y, w, h = hands[0]["bbox"]
        r_centera, r_centerb = hands[0]["center"]
        nodes = [i for i in hands[0]["lmList"]]
        cv2.putText(img, str(nodes[test][0] + x) + " " + str(nodes[test][1] + y), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        cv2.circle(img, (nodes[test][0], nodes[test][1]), 20, (255, 0, 255), 5)
        if time.time() - starttime > 1:
            starttime = time.time()
            if len(xy) == 2:
                move = ""
                if nodes[test][0] + x - xy[0] > w:
                    move = "r"
                elif xy[0] - nodes[test][0] - x > w:
                    move = "l"
                if nodes[test][1] + y - xy[1] > h:
                    move += "d"
                elif xy[1] - nodes[test][1] - y > h:
                    move += "u"
                if move == "":
                    move = "n"
            xy = [nodes[test][0] + x, nodes[test][1] + y]
        cv2.putText(img, move, (500, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("1"):
        cv2.destroyAllWindows()
        break
