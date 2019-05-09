import numpy as np
import sys
import glob
import laspy
import os
import math
import shutil

def writeToLAS(depth,colorImage):
    header = laspy.header.Header(point_format=2)
    pt = laspy.file.File("output.las", mode="w", header=header)
    degreePerPixelY = (float)(60 / (float)(len(depth[0])))  # pixel location to degree calculation
    degreePerPixelX = (float)(360 / (float)(len(depth)))

    # convert all the points
    size = len(depth)*len(depth[0])+1
    ptX= np.zeros(size)
    ptY=np.zeros(size)
    ptZ=np.zeros(size)
    ptR = np.zeros(size)
    ptG = np.zeros(size)
    ptB = np.zeros(size)
    ptInt = np.zeros(size)
    for x in range(0, len(depth[0])):
        for y in range(0, len(depth)):
            alphaX = (float)(x * degreePerPixelX * math.pi / 180)  # calculate the "angle" in the panorama, python math works in radians..
            alphaY = (float)(y * degreePerPixelY * math.pi / 180)  # calculate the "angle" in the panorama, python math works in radians..
            index = x+y*len(depth[0])
            newX = depth[y][x] * (float)(math.cos(alphaY)) * (float)(math.cos(alphaX))
            newY = (float)(math.sin(alphaY)) * depth[y][x]
            newZ = depth[y][x] * (float)(math.cos(alphaY)) * (float)(math.sin(alphaX))
            ptZ[index] = newZ
            ptY[index] = newX
            ptX[index] = newY
            ptInt[index] = x*y
            # ptR =
            # ptG =
            # ptB =
            # print("x is ")
            # print(newX)
            # print("y is ")
            # print(newY)
            # print("z is ")
            # print(newZ)
            # print("---------------")
    pt.header.offset = [0,0,0]
    pt.header.scale = [0.001, 0.001, 0.001]
    pt.x = ptZ
    pt.y = ptY
    pt.z = ptX
    pt.intensity = ptInt
    pt.Intensity = ptInt
    pt.red= ptR
    pt.Red = ptR
    pt.green = ptG
    pt.Green = ptG
    pt.blue = ptB
    pt.Blue = ptB
    pt.close()

    potreePath = os.getcwd() + "\potreeFolder"
    if os.path.exists(potreePath):
        shutil.rmtree(potreePath)  # delete the old data
    os.mkdir(potreePath)
    absPath = os.getcwd()
    os.chdir(absPath + "\PotreeConverter_1.6_windows_x64")
    os.system("PotreeConverter" + ' "' + absPath + '"' + " -o " + '"' + potreePath + '"')
    os.chdir(absPath)
    print("process done")
    print("search on following path:")
    print(potreePath)

