from matplotlib import pyplot as plt
from pylab import rcParams
import cv2 as cv
import math
import numpy as np

def loadImage(fileName):
    src = cv.imread(cv.samples.findFile(fileName), 0)
    if src is None:
        print ('Error opening image!')
    return src

def showCentroids (image, centroids):
    demo = np.zeros((np.shape(image)), dtype = np.uint8);

    if centroids is not None:
        for centroid in centroids:
            if centroid[0] != -1 and centroid[1] != -1:
                demo[int(centroid[1]), int(centroid[0])] = 255

    return demo;

def showLines(lines, DemoImg):
    for line in lines:
        rho = line[0]
        theta = line[1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(DemoImg, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    plt.imshow(DemoImg);
