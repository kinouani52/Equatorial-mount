
import cv2
import numpy as np
import time


img = cv2.imread('tp1.jpeg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY)



hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 152])
upper = np.array([255, 255, 255])
mask = cv2.inRange(hsv, lower, upper)


M = thresh1.shape[1] // 2
N = thresh1.shape[0] // 2
#€tiles = [img_gray[x:x + M, y:y + N] for x in range(0, img_gray.shape[0], M) for y in range(0, img_gray.shape[1], N)]
x, y, w, h = 0, 0, M, N
upleft = mask[y+h:y+h+h, x:x+w]
upright = mask[y+h:y+h+h, x+w:x+w+w]
downleft= mask[y:y+h, x:x+w]
downright = mask[y:y+h, x+w:x+w+w]



# Count pixels
upleft_pixels = cv2.countNonZero(upleft)
upright_pixels = cv2.countNonZero(upright)
downleft_pixels = cv2.countNonZero(downleft)
downright_pixels = cv2.countNonZero(downright)

print('up Left pixels:', upleft_pixels)
print('up Right pixels:', upright_pixels)
print('down Left pixels:', downleft_pixels)
print('down Right pixels:', downright_pixels)
cv2.imshow('image',img_gray)
#cv2.imshow('thresh',thresh)
cv2.imshow('mask', mask)
cv2.imshow('UL', upleft)
cv2.imshow('UR', upright)
cv2.imshow('DL', downleft)
cv2.imshow('DR', downright)
    # Wait longer to prevent freeze for videos.
cv2.waitKey()


cv2.destroyAllWindows()