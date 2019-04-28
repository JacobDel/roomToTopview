import numpy as np
import sys
import glob
import laspy
import os
import math
import shutil

def writeToLAS(depth):
    folderNumber = 1
    header = laspy.header.Header(point_format=2)
    pt = laspy.file.File("room.las", mode="w", header=header)
    degreePerPixelY = (float)(360 / (float)(len(depth[0])))  # pixel location to degree calculation
    degreePerPixelX = (float)(360 / (float)(len(depth)))

    # convert all the points
    ptX=[]
    ptY=[]
    ptZ=[]
    for x in range(0, len(depth[0])):
        for y in range(0, len(depth)):
            alphaX = x * degreePerPixelX * math.pi / 180  # calculate the "angle" in the panorama, python math works in radians..
            alphaY = x * degreePerPixelY * math.pi / 180  # calculate the "angle" in the panorama, python math works in radians..
            ptX = np.append(ptX,depth[x][y] * math.cos(alphaY) * math.sin(alphaX))
            ptY = np.append(ptY, math.sin(alphaY) * depth[x][y])
            ptZ = np.append(ptZ,depth[x][y] * math.cos(alphaY) * math.cos(alphaX))
            pt.x = ptX
            pt.y = ptY
            pt.z = ptZ
    pt.close()

    potreePath = os.getcwd() + "\potreeFolder"+str(folderNumber)
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

