# Eerst foto blurren (vb gaussian)
# Dan lijnen uit foto halen
# Daarna vormen detecteren


# Muren detecteren => lijnen die parallel zijn wijzen op muren!!
# dit zullen dunne lijntjes zijn

import numpy as np
from PIL import ImageGrab
from PIL import Image
import cv2
import sys
import os
import time
import matplotlib
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def draw_lines(img, lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)


def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500],
                         ], np.int32)

    # sharpLines = np.copy(processed_img)
    # sharpLines = roi(sharpLines, [vertices])
    # for i in range(0, 1):
    kernel = 5
    processed_img = cv2.GaussianBlur(processed_img, (kernel, kernel), 0)

    processed_img = roi(processed_img, [vertices])
    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                          edges       rho   theta   thresh         # min length, max gap:
    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, 20, 15)
    getAngle(lines)
    draw_lines(processed_img, lines)
    cv2.imshow("", processed_img)
    return processed_img


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def getAngle(lines):
    angles = []
    for line in lines:
        coords = line[0]
        # Y/X
        if len(coords)==4:
            angle = math.atan2((coords[3] - coords[1]), (coords[2] - coords[0]))
            angle=angle*180/math.pi
        # if angle < 0:
        #     angle = angle + 360
            angles.append(angle)
    # de frequentie van iedere waarde plotten met stap van 5
    x = angles
    num_bins = 20
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    # get 2 max values out of n
    plt.show()

def morfologie(image, korrelgrote):
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    imageCopy = np.copy(image)
    lastSize = korrelgrote
    currentSize = korrelgrote
    lines = cv2.HoughLinesP(imageCopy, 1, np.pi / 180, 180, 20, 15)
    while (lines is not None) and (len(lines) > 2):
        morphImage = cv2.morphologyEx(imageCopy, cv2.MORPH_OPEN,
                                      cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (currentSize, currentSize)))
        lines = cv2.HoughLinesP(morphImage, 1, np.pi / 180, 180, 20, 15)
        lastSize = currentSize
        currentSize = currentSize + 1
    print(lastSize)
    return cv2.morphologyEx(imageCopy, cv2.MORPH_OPEN,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (lastSize, lastSize)))


relativePath = os.getcwd()
picturePath = "\\testFotos\\IMG_0017.jpg"
complPath = relativePath + picturePath
print(complPath)
jpgfile = Image.open(
    complPath)  # "C:\Users\Jacob Delabie\Desktop\sem6\ing project\pythonFolder\\testFotos\slaapkamer.jpg"
jpgfile = np.array(jpgfile)
jpgfile = cv2.resize(jpgfile, (960, 540))
ProcessedImage = process_img(jpgfile)
cv2.imshow("lol", jpgfile)
getAngle(jpgfile)
while (True):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
