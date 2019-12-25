import cv2 as cv
import numpy as np
import math
from statistics import mean

from matplotlib import pyplot as plt
try:
    from Processing import *
except ModuleNotFoundError:
    from Alireza.Processing import *

def findComponents(image):
    edgyImg = cv.Canny(image, 50, 200, None, 3)
    edgyColor = cv.cvtColor(edgyImg, cv.COLOR_GRAY2BGR)

    DemoImg = np.zeros_like(edgyColor);

    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(edgyImg);
    avg_width = 0;
    for stat in stats:
        avg_width += stat[cv.CC_STAT_WIDTH]
    avg_width /= num_labels
    try:
        display ("Found " + str(num_labels) + " components with height " + str(avg_width) + " in image")
    except NameError:
        i = 0;

    return avg_width;

def putGLM(image, width):
    (h, w) = np.shape(image);
    strips = int (w/width);
    if (w % width != 0):
        strips += 1;
    for i in range(strips):
        for j in range(h):
            avg_gray = 0;
            strip_width = ((i+1) * width if (((i+1) * width) < w) else w) - i*width + 1;

            for k in range(i*width, (i+1) * width if (((i+1) * width) < w) else w):
                avg_gray = image[j,k];

            avg_gray = int (avg_gray / strip_width);

            for k in range(i*width, (i+1) * width if (((i+1) * width) < w) else w):
                image[j,k] = avg_gray;
    return image, strips;

def filterWhite(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        heights = [];
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
            continue;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if (tempH < mode):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 0;
                tempH = 0;
                start = -1;
        if (tempH < mode and tempH != 0):
            image[start:j,l:r] = np.ones((j-start, r-l)) * 0;
    return image;

def filterBlack(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        heights = [];
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

        if (heights != []):
            m = int (mean([heights[i] for i in range(len(heights)) if i%8 ==0]))
        else:
            continue;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if ((tempH < m) or (tempH < 3*m and checkDangle(image[start:j,l-1 if l!= 0 else 0:r+1 if r!=w else w]))):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
                tempH = 0;
                start = -1;
        if ((tempH != 0) and ((tempH < m) or (tempH < 3*m and checkDangle(image[start:j,l-1 if l!= 0 else 0:r+1 if r!=w else w])))):
            image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
    return image;

def removeBlack(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;

    height = avgBlackH(np.copy(image), strips, width);

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if (tempH >= 2 * height):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
                tempH = 0;
                start = -1;
        if (tempH >= 2 * height and tempH != 0):
            image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
    return image;

def constructLines(image, strips, width, height):
    (h, w) = np.shape(image);
    dist = int (height);

    for i in range(1,h-1):
        for j in range(1,w-1):
            if lonelyStart(image, i, j) == 0 and lonelyEnd(image, i, j) > 0:
                image = findLine(image, i, j, dist);
            elif lonelyEnd(image, i, j) == 0 and j < w/2 and lonelyStart(image, i, j) > 0:
                cv.line(image, (0, i), (j, i), 1, 1, cv.LINE_AA)
    plt.imshow(image);
    return image;

def processSkeleton(image):
    (h,w) = np.shape(image);
    nimage = np.ones((h,w), dtype=np.uint8);
    for i in range(h):
        for j in range(w):
            nimage[i,j] = image[i,j];
    edgyImg = cv.Canny(nimage, 50, 200, None, 3)
    edgyColor = cv.cvtColor(edgyImg, cv.COLOR_GRAY2BGR)
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(edgyImg);
    try:
        display (str(num_labels) + " lines found");
    except NameError:
        random = 0;

    return nimage, labels, stats

def connectLines(image, strips, width, stats, blockImage, orig):
    (h,w) = np.shape(image);
    avgH = avgWhiteHLater(blockImage, strips, width);
    distMat = np.ones((len(stats))) * (-1);
    neighMat = np.ones((len(stats))) * (-1);


    for i in range(len(stats)):
        for j in range(len(stats)):
            dist = abs (stats[i][cv.CC_STAT_TOP] - stats[j][cv.CC_STAT_TOP]);
            if (stats[i][cv.CC_STAT_LEFT] + stats[i][cv.CC_STAT_WIDTH] <= stats[j][cv.CC_STAT_LEFT]):
                if (dist < avgH) and (distMat[i] == -1 or dist < distMat[i]):
                    distMat[i] = dist;
                    neighMat[i] = j;

    for i in range(len(distMat)):
        if distMat[i] != -1:
            j = int(neighMat[i]);
            x1 = int (stats[i][cv.CC_STAT_LEFT] + stats[i][cv.CC_STAT_WIDTH])
            y1 = int (stats[i][cv.CC_STAT_TOP] + 1)

            x2 = int (stats[j][cv.CC_STAT_LEFT])
            y2 = int (stats[j][cv.CC_STAT_TOP] + 1)

            cv.line(image, (x1, y1), (x2, y2), 255, 1, cv.LINE_AA);

    lines  = -1;
    for i in range(len(stats)):
        stat = stats[i];

        if i not in neighMat and stat[cv.CC_STAT_LEFT] < w/2 and neighMat[i] == -1 and stat[cv.CC_STAT_LEFT] + stat[cv.CC_STAT_WIDTH] > w/2:
            cv.line(orig, (0, int (stat[cv.CC_STAT_TOP] + 1)), (w, int (stat[cv.CC_STAT_TOP] + 1)), 1, 1, cv.LINE_AA);
            lines += 1;
        elif (neighMat[i] == -1 and i in neighMat) or (neighMat[i] == -1 and i not in neighMat and stat[cv.CC_STAT_WIDTH] >= w):
            cv.line(orig, (0, int (stat[cv.CC_STAT_TOP] + 1)), (w, int (stat[cv.CC_STAT_TOP] + 1)), 1, 1, cv.LINE_AA);
            lines += 1;

    return image, lines, orig;
