import cv2
import numpy as np
import time


moon_cascade = cv2.CascadeClassifier('cascade.xml')
cap = cv2.VideoCapture("moon2.mp4")
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
while (True):
    ret, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY)
    moon = moon_cascade.detectMultiScale(img, 1.3, 5)
    found = len(moon)

    if found != 0:
        for (x, y, w, h) in moon:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = img_gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 0, 200])
            upper = np.array([179, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)

            M = thresh1.shape[1] // 2
            N = thresh1.shape[0] // 2
            x, y, w, h = 0, 0, M, N
            upleft = mask[y + h:y + h + h, x:x + w]
            downright = mask[y + h:y + h + h, x + w:x + w + w]
            downleft = mask[y:y + h, x:x + w]
            upright = mask[y:y + h, x + w:x + w + w]



            Uleft_pixels = cv2.countNonZero(upleft)
            Uright_pixels = cv2.countNonZero(upright)
            Bleft_pixels = cv2.countNonZero(downleft)
            Bright_pixels = cv2.countNonZero(downright)

            print('Upper Left pixels:', Uleft_pixels)
            print('Bottom Left pixels:', Bleft_pixels)
            print('Upper Right pixels:', Uright_pixels)
            print('Bottom Right pixels:', Bright_pixels)


            time.sleep(2)


    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





