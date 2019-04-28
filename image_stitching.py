# USAGE
# python image_stitching.py --images images/scottsdale --output output.png --crop 1

# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from pykinect import nui
import time
import math

# initializing data
print("[INFO] initializing kinect...")

# data containers
data = np.empty((480, 640, 4), np.uint8)
depth = np.empty((480,640),np.uint)

def video_handler_function(frame):
        video = np.empty((480,640,4), np.uint8)
        frame.image.copy_bits(video.ctypes.data)
        data[:,:,0:3] = video[:,:,0:3]

        #cv2.imshow('KINECT Video Stream', video)

def depth_handler_function(frame):
        deptht = np.empty((480,640),np.uint)
        frame.image.copy_bits(deptht.ctypes.data)
        deptht = np.repeat(np.repeat(deptht, 2, axis=0), 2, axis=1)[0:480,0:640]
        depth[:,:] = deptht[:,:]
#        data[:,:,3] = np.bitwise_and(np.right_shift(depth, 7), 255).astype("uint8")
        data[:,:,3] = np.right_shift(depth.copy(), 24) #warping is only compatible with 8 bit datatypes, so this 32 bit number gets split up into 4 pieces
#        data[:,:,4] = np.right_shift(np.left_shift(depth, 8), 24)
#        data[:,:,5] = np.right_shift(np.left_shift(depth, 16), 24)
#        data[:,:,6] = np.right_shift(np.left_shift(depth, 24), 24)

kinect = nui.Runtime()
kinect.video_frame_ready += video_handler_function
kinect.depth_frame_ready += depth_handler_function
kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)
kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)

def readImages(amountofimages):
    images = []
    depthimages = []
    for i in range(0, amountofimages):
        images.append(cv2.imread("sampledata/living_room/" + str(i) + ".jpg"))
        temp = np.zeros((480, 640), np.uint8)
        read = cv2.imread("sampledata/living_room/" + str(i) + "g.jpg")
        temp[:,:] = read[:,:,0]
        depthimages.append(temp)
        #time.sleep(1)
        #print(i)
        #images.append(data[:,:,0:3].copy())
        #depthimages.append(data[:,:,3].copy())
        #cv2.imwrite("sampledata/bedroom/" + str(i) + ".jpg", data[:,:,0:3])
        #cv2.imwrite("sampledata/bedroom/" + str(i) + "g.jpg", data[:,:,3])
    return (images, depthimages)

def stitchImages(images):
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    return stitcher.stitch(images)

def cropImage(image):
    imaget = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

    gray = cv2.cvtColor(imaget, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    mask = np.zeros(thresh.shape, dtype="uint8")
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    minRect = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRect = cv2.erode(minRect, None)
        sub = cv2.subtract(minRect, thresh)

    cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(c)

    imaget = imaget[y:y + h, x:x + w]
    return imaget

def writeToText(rgb, depth):
    file1 = open("colordata.txt", "w")
    file2 = open("positiondata.txt", "w")

    pixelangleX = 0.1  # amount of degrees per pixel
    pixelangleY = 0.1
    angleYOffset = -rgb.shape[0] / 2 * pixelangleY  # offset on the vertical angle to center the image

    for h in range(0, rgb.shape[0]):
       for w in range(0, rgb.shape[1]):
           posX = math.sin(-math.radians(pixelangleX) * w) * depth[h,w]
           posZ = math.cos(-math.radians(pixelangleX) * w) * depth[h,w]
           posY = math.sin(math.radians(pixelangleY*h+angleYOffset))
           file1.write("Vector3.new(" + str(rgb[h,w,0]) + ", " + str(rgb[h,w,1]) + ", " + str(rgb[h,w,2]) + ")," + "\n")
           file2.write("Vector3.new(" + str(posX) + ", " + str(posY) + ", " + str(posZ) + ")," + "\n")

def getPano(colordata, depthdata, doDepth, crop):
    print("[INFO] stitching images...")
    (statuscolor, colorpicture) = stitchImages(colordata)
    (statusdepth, depthpicture) = (None, None)
    if (doDepth):
        (statusdepth, depthpicture) = stitchImages(depthdata)
    success = True
    if (statuscolor > 0):
        success = False
        print("[INFO] color stitching unsuccessful...")
    if (statusdepth > 0 and doDepth):
       success = False
       print("[INFO] depth stitching unsuccessful...")
    if (success):
        print("[INFO] stitching successful...")
        if (crop):
            print("[INFO] cropping pictures...")
            croppedcolor = cropImage(colorpicture)
            if (doDepth):
                croppeddepth = cropImage(depthpicture)
                print("[INFO] finished panorama")
                return croppedcolor, croppeddepth
            else:
                print("[INFO] finished panorama")
                return croppedcolor, [None]
        else:
            print("[INFO] finished panorama")
            if (doDepth):
                return colorpicture, depthpicture
            else:
                return colorpicture, [None]
    else:
        return [None], [None]

def cylindricalWarp(img, K):
	h_, w_ = img.shape[:2]
	y_i, x_i = np.indices((h_, w_))
	X = np.stack([x_i, y_i, np.ones_like(x_i)], axis=-1).reshape(h_ * w_, 3)  # to homog
	Kinv = np.linalg.inv(K)
	X = Kinv.dot(X.T).T  # normalized coords
	A = np.stack([np.sin(X[:, 0]), X[:, 1], np.cos(X[:, 0])], axis=-1).reshape(w_ * h_, 3)
	B = K.dot(A.T).T  # project back to image-pixels plane
	B = B[:, :-1] / B[:, [-1]]
	B[(B[:, 0] < 0) | (B[:, 0] >= w_) | (B[:, 1] < 0) | (B[:, 1] >= h_)] = -1
	B = B.reshape(h_, w_, -1)

	return cv2.remap(img, B[:, :, 0].astype(np.float32), B[:, :, 1].astype(np.float32), cv2.INTER_AREA, borderMode=cv2.BORDER_TRANSPARENT)

print("[INFO] reading images...")
amountofimages = 29
(colordata, depthdata) = readImages(amountofimages)
nd = []
for i in range(0, amountofimages):
    temp = np.zeros((480, 640, 3), np.uint8)
    temp[:,:,0:2] = colordata[i][:,:,0:2]
    temp[:,:,2] = depthdata[i]
    nd.append(temp)

(colorpic, depthpic) = getPano(colordata[0:15], nd[0:15], True, True)
(colorpic2, depthpic2) = getPano(colordata[14:29], nd[14:29], True, True)
cv2.imshow("color", colorpic)
cv2.imshow("color2", colorpic2)
cv2.imwrite("color.jpg", colorpic)
cv2.imwrite("color2.jpg", colorpic2)
cv2.imshow("depth", depthpic)
cv2.imshow("depth2", depthpic2)
cv2.imwrite("depth.jpg", depthpic)
cv2.imwrite("depth2.jpg", depthpic2)
(combinedc, combinedd) = getPano([colorpic, colorpic2], [depthpic, depthpic2], True, True)
totaldepth = np.zeros((480, 640*amountofimages), np.uint8)
totalrgb = np.zeros((480, 640*amountofimages, 3), np.uint8)
K = np.array([[580, 0, 640 / 2], [0, 580, 480 / 2], [0, 0, 1]])
for i in range(0, amountofimages):
    temp = np.zeros((480,640,3), np.uint8)
    temp[:,:,0] = depthdata[i]
    #result = cylindricalWarp(temp, K)[:,:,0]
    totaldepth[:,int(i*640*0.22):int(i*640*0.22+640)] = np.where(temp == 0, totaldepth[:,int(i*640*0.22):int(i*640*0.22+640)], temp)
    #resultrgb = cylindricalWarp(colordata[i], K)
    totalrgb[:,int(i*640*0.22):int(i*640*0.22+640),:] = np.where(colordata[i] == 0, totalrgb[:,int(i*640*0.22):int(i*640*0.22+640),:], colordata[i])
cv2.imwrite("totaldepth.jpg", totaldepth[:,0:3600])
cv2.imwrite("totalrgb.jpg", totalrgb[:,0:3600,:])
writeToText(totalrgb[:,0:3600,:], totaldepth[:,0:3600])
if (combinedc.all() != None and combinedd.all() != None):
    cv2.imshow("combined", combinedc)
    cv2.imwrite("combined.jpg", combinedc)
    cv2.imshow("combineddepth", combinedd)
    cv2.imwrite("combineddepth.jpg", combinedd)
cv2.waitKey(0)