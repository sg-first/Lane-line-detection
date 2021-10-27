import cv2
import numpy as np

img = cv2.imread('0.png',0)
h, w = img.shape
img = cv2.GaussianBlur(img,(3, 3),0)
img = cv2.Canny(img,160,180) # min,max
lines = cv2.HoughLines(img, 1, np.pi / 180, 300) # thr

img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
for i in range(len(lines)):
    for rho, theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + w * (-b))
        y1 = int(y0 + w * (a))
        x2 = int(x0 - w * (-b))
        y2 = int(y0 - w * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('img',img)
cv2.waitKey(0)