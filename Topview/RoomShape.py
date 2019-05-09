import sys
import getopt
import turtle
import random
from PIL import Image
import numpy as np
import cv2
import Color
# import turtle
import math
import numpy
def drawRoom(points,panoramaLength):
    turtleImage(getCoords(points,panoramaLength),Color.Color.room,3)
def drawObject(points,panoramaLength,objectColor):
    # points mogelijk converteren
    turtleImage(getCoords(points,panoramaLength),objectColor(),5)
def getCoords(points, panoramaLength): # can be used by lines or objects
    # convert to coords (x,y)
    # xValues = the X indexes of all the points in the panorama
    # valueDistances = the actual distance of the edge
    # the length of the panorama => width of the panorama image
    # coords = [[0 for y in range(len(xValues))] for x in range(2)] # set up array for xy coords
    coords = []
    degreePerPixel = (float)(360/(float)(panoramaLength)) # pixel location to degree calculation
    for index in range(0,len(points)): # go over every value in the array
        alpha = points[index][0]*degreePerPixel*math.pi/180 # calculate the "angle" in the panorama, python math works in radians..
        depthValue = points[index][1] # the measured value in the depthmap
        # coords[index][0]=math.cos(alpha)*depthValue # calc the x value
        # coords[index][1]=math.sin(alpha)*depthValue # calc the y value
        coords.append([])
        arrIndex = len(coords)-1
        coords[arrIndex].append(math.cos(alpha)*depthValue)
        coords[arrIndex].append(math.sin(alpha) * depthValue) # coords
    return coords

def turtleImage(coords, colorr,penSize):
    draw = turtle.Turtle()
    draw.pensize(penSize)
    draw.speed(100)
    height = draw.window_height()
    width = draw.window_width()
    max=0
    for i in range(0,len(coords)):
        for j in range(0,2):
            if(abs(coords[i][j])>max):
                max = abs(coords[i][j])
    factor = height/(max*2*1.2)
    newCoords= numpy.multiply(coords,factor)
    draw.color(colorr)
    draw.penup()
    for i in range(0,len(coords)): # go through every point
        draw.goto(newCoords[i])
        draw.pendown()
    draw.goto(newCoords[0])
    draw.hideturtle()
    # draw.exitonclick()
    # this should draw the shape of our object
def getRandomColor():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)
