import cv2
import numpy as np


cap = cv2.VideoCapture("moon2.mp4",0)
moon_cascade = cv2.CascadeClassifier('cascade.xml')

cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
while (True):
    success , img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    moon = moon_cascade.detectMultiScale(img, 1.3, 5)
    found = len(moon)
    for (x, y, w, h) in moon:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]


    if found != 0:
      blur = cv2.GaussianBlur(gray, (5, 5), 0)
      thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
      ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    M = gray.shape[0] // 2
    N = gray.shape[1] // 2
    x, y, w, h = 0, 0, M, N
    upleft = thresh1[y:y + h + h, x:x + w]
    upright = thresh1[y:y + h + h, x + w:x + w + w]
    downleft = thresh1[y:y + h, x:x + w]
    downright = thresh1[y:y + h, x:x + w + w]




    cv2.imshow("Video", img)
    cv2.imshow("Video threshold", thresh1)
    cv2.imshow("Video otsu threshold", thresh)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break