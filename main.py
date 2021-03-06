import cv2
import numpy as np

def show(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)

def doLaneDet(path, times=0):
    img = cv2.imread(path, 0)
    h, w = img.shape
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # 5有道上的没检测出来
    # 8短线检测不出来（整体算法的问题，得加东西）
    img = cv2.Canny(img, 10+times*10, 200+times*2)  # min,max
    # 3:200, 300
    # 4:检测不出来
    # 进行花样滤波？
    lines = cv2.HoughLines(img, 1, np.pi / 180, 290)  # thr

    allK = []
    allPos = []
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

            k = (y1 - y2) / (x1 - x2)
            allK.append(k)
            allPos.append(((x1, y1), (x2, y2)))

    mean = np.median(allK)
    std = np.std(allK)
    print('mean:', mean, 'std:', std)
    if std < 0.1: std = 0.1

    num = 0
    img = cv2.imread(path)
    for i in allPos:
        p1, p2 = i
        x1, y1 = p1
        x2, y2 = p2
        k = (y1 - y2) / (x1 - x2)
        if k <= mean + std and k >= mean - std:
            print(k)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            num += 1
    ret = num / len(allK)
    print('可用率：', ret)

    if ret < 0.8:
        return doLaneDet(path,times+1)
    else:
        show(img)
        return ret

doLaneDet('8.png')
