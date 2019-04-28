import sys
import getopt

import RoomEdges.getDistance
from PIL import Image
import numpy as np
import cv2
import RoomEdges.GraphCalculations
import Topview.RoomShape
from Topview.RoomShape import turtleImage
import Parse.ParseToLAS as parse

# # test graphFunction
# points = [50,50,60,5,65,70,85,90,130,140,180,50,40,30,40,20,10,10,9,5,4,3,30,32,38,39,45,90,56,150,190,190,190,50,70,56,64,78,65,45,54]
# GraphCalculations.getMaximaCoords(points,3)

# main
pano = np.asarray(Image.open("testFotos/pano.jpg"))
# cv2.imshow(pano.astype('uint8'),'org foto')
parse.writeToLAS(pano)
edges = RoomEdges.getDistance.getRoomCoords(pano) #returns 4 angles
coords = Topview.RoomShape.getCoords(edges,len(pano[0]))

turtleImage(coords)
while (True):
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
