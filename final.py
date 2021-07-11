import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
import time, sys
import tty
import termios

stepPin1 = 31
dirPin1 = 33

stepPin2 = 35
dirPin2 = 37

enPin1 = 12
enPin2 = 16

# initialize PINS
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(enPin1, GPIO.OUT)
    GPIO.setup(enPin2, GPIO.OUT)

    GPIO.setup(stepPin1, GPIO.OUT)
    GPIO.setup(dirPin1, GPIO.OUT)

    GPIO.setup(stepPin2, GPIO.OUT)
    GPIO.setup(dirPin2, GPIO.OUT)

    GPIO.output(enPin1, 1)
    GPIO.output(enPin2, 1)


# movement function for motor1(Y axis)：To set movement direction and steps
def move(direc, steps):
    GPIO.output(dirPin1, direc)
    GPIO.output(enPin1, 0)
    for i in range(1, steps):
        GPIO.output(stepPin1, 1)
        time.sleep(0.005)
        GPIO.output(stepPin1, 0)
        time.sleep(0.005)
    GPIO.output(enPin1, 1)


# movement function for motor2(base)：To set movement direction and steps
def move2(direc, steps):
    GPIO.output(dirPin2, direc)
    GPIO.output(enPin2, 0)
    for i in range(1, steps):
        GPIO.output(stepPin2, 1)
        time.sleep(0.005)
        GPIO.output(stepPin2, 0)
        time.sleep(0.005)
    GPIO.output(enPin2, 1)


def destroy():
    GPIO.cleanup()

# initialize Pins
setup()


moon_cascade = cv2.CascadeClassifier('cascade.xml')
cap = cv2.VideoCapture("moon2.mp4")
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)
while (True):
    ret, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    moon = moon_cascade.detectMultiScale(img, 1.3, 5)
    found = len(moon)

    if found != 0:
        for (x, y, w, h) in moon:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = img_gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 8, 200])
            upper = np.array([179, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)

            M = thresh1.shape[1] // 2
            N = thresh1.shape[0]
            x, y, w, h = 0, 0, M, N
            upleft = mask[y:y + h + h, x:x + w]
            upright = mask[y:y + h + h, x + w:x + w + w]
            downleft = mask[y:y + h, x:x + w]
            downright = mask[y:y + h, x:x + w + w]

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





