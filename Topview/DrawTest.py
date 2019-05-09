import RoomShape
import cv2
from random import randint
import numpy as np
points = [[5,5],[10,0],[7,20],[5,5]]
RoomShape.turtleImage(points,RoomShape.getRandomColor(),7)
points = [[-10,5],[14,8],[19,-7],[-4,-9]]
RoomShape.turtleImage(points,RoomShape.getRandomColor(),3)
for j in range (0,10):
    points = []
    for i in range(0,5):
        points.append([])
        for coo in range(0,2):
            points[i].append(randint(-20,20))
    RoomShape.turtleImage(points,RoomShape.getRandomColor(),4)
while (True):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
