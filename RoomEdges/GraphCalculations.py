import numpy as np
def getMaximaCoords(points,topSteps,indexWidth): #min points required = 10
    # pattern: max,min,max,min,max or min,max,min,max,min,max
    # if after points/8 steps it doesn't go up or down we reset min/max
    max = 0
    min = 255
    stepped = 0
    maximas=[] # save all the maxima's
    index=0
    searchMaxim = True #search for minima OR maxima
    for point in points:
        stepped = stepped + 1 # steps since maxima/minima
        index = index + 1 #index in array
        if(searchMaxim is True):
            if(point>max):
                max=point
                stepped=0
        else:
            if(point<min):
                min=point
                stepped=0


        if(stepped>topSteps): # it's been 7 steps since the max has gone up
            if(searchMaxim):
                maximas.append([]) #https://stackoverflow.com/questions/856948/2d-arrays-in-python
                arrIndex = len(maximas)-1
                maximas[arrIndex].append((index-stepped)*indexWidth)
                maximas[arrIndex].append(max)
                # print("maxima is:")
                # print(index-stepped)
                # print("with value: ")
                # print(max)
                # print("-----")
            # else:
            #     print("minima found at: ")
            #     print(index)
            min = 255
            max = 0
            searchMaxim = not searchMaxim
            stepped=0
    return maximas

