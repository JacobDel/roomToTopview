import sys
import getopt
import turtle

from PIL import Image
import numpy as np
import cv2
# import turtle
import math

def getCoords(edges, panoramaLength): # can be used by lines or objects
    # convert to coords (x,y)
    # xValues = the X indexes of all the edges in the panorama
    # valueDistances = the actual distance of the edge
    # the length of the panorama => width of the panorama image
    # coords = [[0 for y in range(len(xValues))] for x in range(2)] # set up array for xy coords
    coords = []
    degreePerPixel = (float)(360/(float)(panoramaLength)) # pixel location to degree calculation
    for index in range(0,len(edges)): # go over every value in the array
        alpha = edges[index][0]*degreePerPixel*math.pi/180 # calculate the "angle" in the panorama, python math works in radians..
        depthValue = edges[index][1] # the measured value in the depthmap
        # coords[index][0]=math.cos(alpha)*depthValue # calc the x value
        # coords[index][1]=math.sin(alpha)*depthValue # calc the y value
        coords.append([])
        arrIndex = len(coords)-1
        coords[arrIndex].append(math.cos(alpha)*depthValue)
        coords[arrIndex].append(math.sin(alpha) * depthValue) # coords
    return coords

def turtleImage(coords):
    turtle.penup()
    for i in range(0,len(coords)): # go through every point
        turtle.goto(coords[i])
        turtle.pendown()
    turtle.goto(coords[0])
    turtle.hideturtle()
    turtle.exitonclick()
    # this should draw the shape of our object