import cv2
import numpy as np

def show(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)

img = cv2.imread('9.png',0)
h, w = img.shape
img = cv2.GaussianBlur(img,(5, 5),0)
# 5杂线很多，得调滤波器到7（但会滤掉车道线（主要是短线的问题））
# 8短线检测不出来（整体算法的问题，得加东西）
img = cv2.Canny(img,10,200) # min,max
# 3:200, 300
# 4:40, 50（阴影非全，而且现在的结果也有点问题）
# show(img)
# 进行花样滤波？
lines = cv2.HoughLines(img, 1, np.pi / 180, 290) # thr

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

show(img)