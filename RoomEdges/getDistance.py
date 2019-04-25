# Er is reeds toegang tot het dieptebeeld en de panorama

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import GraphCalculations
wallLines = []  # contains all the corner lines in a room (no roof lines!), format: x,y1,y2

def getRoomCoords(panorama):  # ONLY VERTICAL LINES! the variable should be a line detection image of a depth image
    steps = 60  # amount of steps we want
    edgesMax = 4

    global wallLines
    imageWidth = len(panorama[0])
    imageHeight = len(panorama)
    threshold = 233
    # we split the image into parts, the stepwidth..

    stepHeight = len(panorama) / steps
    stepWidth = len(panorama[0])/steps
    if(stepHeight<1 or stepWidth<1):
        print("steps to small")
        exit(0)
    Values = np.zeros(steps)
    index = 0
    for width in range(0, len(panorama[0]), stepWidth):
        # subImage = panorama[height:height + 1]  # get a line of the image
        # clippedSubImage = np.where(subImage > threshold, True, False)
        max=0
        for height in range(0, len(panorama), stepHeight):
            if(panorama[height][width]>max): # 0 weg doen of toevoegen..
                max = panorama[height][width] # 0 weg doen
        if(index<steps):
            Values[index] = max
            index = index+1
    plt.plot(Values)
    plt.ylabel("foto afstanden")
    plt.show()
    breakLoop=False
    loopCycles=0
    errorFactor = 0
    while(breakLoop is False):
        if(len(GraphCalculations.getMaximaCoords(Values,errorFactor,stepWidth))<=4):
            wallLines = GraphCalculations.getMaximaCoords(Values, errorFactor,stepWidth)
            breakLoop = True
        else:
            errorFactor +=1
        if(loopCycles>100):
            breakLoop = True
        loopCycles+=1
    return wallLines # this returns the wall location in the room

    # maxima should always be followed by a minima (with minima difference of delta > max/3


        # for width in range(0, len(subImage[1])):
            # if (clippedSubImage[1][width] == True):
                # np.append(cornerCoords,
                 #          (height, width, subImage[1][width]))  # add the coordinates, + distance to an array
                # np.append(xValues,subImage[0][width]) # get a list of all the x coords
        # np.clip(subImage, threshold, 6500, subImage)  # clip the image to only get the max
    #histogram for X coords.. (https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html)
        #min amount of points => nodes


    # plt.hist(xValues, bins='auto')  # arguments are passed to np.histogram
    # plt.title("Histogram with 'auto' bins")
    # plt.show()

    # min distance between lines
    # if not -> chose the longest line
    # lines should have a min length
    # put the resulting lines into wallLines
    # if no lines: print("no wall lines!!)
    # return wallLines


def setRoomCoords(newWallLines):
    global wallLines
    wallLines = newWallLines


# by having access to the room coords we should be able to determine the position of objects in a room, as the distance between walls is lineair
def getCoordObject(objectLocation):  # parameter: [x1,x2,y1,y2]
    global wallLines
    startX = (objectLocation[0]+objectLocation[1])/2
    if wallLines is None:
        exit(-1) #exit as no walllines have been initialised
    # find closest wall lines, should be chronological
    leftWall = 0
    rightWall = 0
    for wallLocation in range(0,len(wallLines)):
        if(wallLines[wallLocation][0]>startX): # the right wall of our object
            rightWall = wallLocation
            if(wallLocation>0):
                leftWall = rightWall-1
            else:
                leftWall = len(wallLines)-1
    return leftWall,rightWall,startX


    # xValues = []
    # index = 0
    # for lines in wallLines:
    #     np.append(xValues[0], abs(lines[0] - ((objectLocation[0] + objectLocation[1]) / 2)))
    #     np.append(xValues[1], index)
    #     index = index + 1
    # np.sort(xValues[0])
    # lineIndex1 = xValues[0]
    # lineIndex2 = xValues[1]