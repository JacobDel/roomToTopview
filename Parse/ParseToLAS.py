import numpy as np
import sys
import glob
import laspy
import os
import math
import shutil

def writeToLAS(depth):
    header = laspy.header.Header(point_format=2)
    pt = laspy.file.File("output.las", mode="w", header=header)
    degreePerPixelY = (float)(45 / (float)(len(depth[0])))  # pixel location to degree calculation
    degreePerPixelX = (float)(360 / (float)(len(depth)))

    # convert all the points
    ptX= np.array([])
    ptY=np.array([])
    ptZ=np.array([])
    ptInt = np.array([])
    for x in range(0, len(depth[0])):
        for y in range(0, len(depth)):
            alphaX = x * degreePerPixelX * math.pi / 180  # calculate the "angle" in the panorama, python math works in radians..
            alphaY = y * degreePerPixelY * math.pi / 180  # calculate the "angle" in the panorama, python math works in radians..
            ptX = np.append(ptX,depth[y][x] * math.cos(alphaY) * math.sin(alphaX))
            ptY = np.append(ptY, math.sin(alphaY) * depth[y][x])
            ptZ = np.append(ptZ,depth[y][x] * math.cos(alphaY) * math.cos(alphaX))
            ptInt = np.append(ptInt,depth[y][x])
    pt.header.offset = [0,0,0]
    pt.header.scale = [0.001, 0.001, 0.001]
    pt.x = ptZ
    pt.y = ptY
    pt.z = ptX
    pt.intensity = ptInt
    pt.Intensity = ptInt
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

