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


# keyboard part
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# read keyboard function
def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


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

# while loop keep listening the keyboard input
while True:
    key = readkey()

    if key == 'w':
        move(0, 20)  # go up 20 steps
        print('forward')
    if key == 's':
        move(1, 20)  # go down 20 steps
        print('backward')

    if key == 'a':  # go left 20 steps
        move2(1, 20)
        print('turnleft')
    if key == 'd':  # go right 20 steps
        move2(0, 20)
        print('turnright')

    if key == 'q':  # stop
        break

# destroy()





