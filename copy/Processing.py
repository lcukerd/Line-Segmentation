import numpy as np
import math
import cv2 as cv
from statistics import mean

def checkDangle(image):
    for row in image:
        if (row[0] == 0 or row[-1] == 0):
            return False;
    return True;

def modeWhite(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;
    heights = [];
    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        mode = max(set(heights), key=heights.count);
    else:
        mode = 0;
    return mode

def avgBlackH(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;
    heights = [];

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        return mean(heights);
    else:
        return 0;

def avgWhiteH(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;
    heights = [];

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        return mean(heights);
    else:
        return 0;

def avgWhiteHLater(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;
    heights = [];

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;
    if (heights != []):
        return int(mean(heights));
    else:
        return 0;

def removeSmallLines(stats):
    avgLen = 0;
    for stat in stats:
        avgLen += stat[cv.CC_STAT_WIDTH];
    avgLen = int (avgLen / len(stats));
    filteredStats = [];
    for stat in stats:
        if (stat[cv.CC_STAT_WIDTH] >= avgLen and stat[cv.CC_STAT_HEIGHT] < 5):
            filteredStats.append(stat);
    return filteredStats;
