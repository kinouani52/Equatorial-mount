import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
# roi_color =[0,0,0]
#global roi_gray
#global roi_color


cap = cv2.VideoCapture("moon3.mp4")
moon_cascade = cv2.CascadeClassifier('cascade.xml')
while True:
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    moon = moon_cascade.detectMultiScale(img, 1.3, 5)
    for (x, y, w, h) in moon:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = img_gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]


    M = img_gray.shape[0] // 2
    N = img_gray.shape[1] // 2
    tiles = [img_gray[x:x + M, y:y + N] for x in range(0, img_gray.shape[0], M) for y in range(0, img_gray.shape[1], N)]



    template = roi_gray
    #w, h = template.shape[:, :, 0]
    res = cv2.matchTemplate(tiles[0], template, cv2.TM_CCOEFF_NORMED)
    res1 = cv2.matchTemplate(tiles[1], template, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(tiles[2], template, cv2.TM_CCOEFF_NORMED)
    res3 = cv2.matchTemplate(tiles[3], template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.7
    flag = 0
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0

    loc = np.where(res >= threshold)
    loc1 = np.where(res1 >= threshold)
    loc2 = np.where(res2 >= threshold)
    loc3 = np.where(res3 >= threshold)

    for pt in zip(*loc[::-1]):
        flag = 1
        if flag:
            print("upper left")
        else:
            print("No, upper left")
    for pt in zip(*loc1[::-1]):
        flag1 = 1
        if flag1:
           print("upper right")
        else:
            print("No, upper right")
    for pt in zip(*loc2[::-1]):
        flag2 = 1
        if flag2:
            print("bottom left")
        else:
            print("No, bottom left.")
    for pt in zip(*loc3[::-1]):
        flag3 = 1
        if flag3:
            print("bottom right")
        else:
            print("No, bottom right.")
            flag=0
     #if (set(roi_color).issubset(set(tiles[0]))):
       # flag = 1


    cv2.imshow("upper left", tiles[0])
    cv2.imshow("upper right", tiles[1])
    cv2.imshow("bottom left", tiles[2])
    cv2.imshow("bottom right", tiles[3])
    cv2.imshow("Result", img)
    cv2.imshow("Result 2 ", roi_color)
    cv2.imshow("Result 2 ", roi_gray)
    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
