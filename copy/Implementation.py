import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt
from pylab import rcParams
from skimage.morphology import skeletonize
from skimage.util import invert
from skimage.filters import sobel_h
import random

try:
    from ImageHandler import *
    from ImageProcessing import *
    from Processing import *
    from ImageProcessing import *
except ModuleNotFoundError:
    from Alireza.ImageHandler import *
    from Alireza.ImageProcessing import *
    from Alireza.Processing import *
    from Alireza.ImageProcessing import *

# replace pixel with avg gray value
def PPA(image, width):
    (h, w) = np.shape(image);
    stripped_image, strips = putGLM(np.copy(image), width);

    # apply otsu's algo
    th = np.copy(stripped_image);
    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w
        _,th[:,l:r] = cv.threshold(stripped_image[:,l:r],0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    filteredWImage = filterWhite(np.copy(th), strips, width)
    Wheight = avgWhiteH(np.copy(th), strips, width)

    filteredBImage = filterBlack(np.copy(filteredWImage), strips, width)

    mode = modeWhite(np.copy(filteredBImage), strips, width);
    return mode, filteredBImage, strips, Wheight;

def performAlirezaSegmentation(file_name, true, filter):
    image = cv.imread(cv.samples.findFile(file_name), 0);
    if filter == True:
        image = cv.medianBlur(image, 5)
    (h, w) = np.shape(image);
    width = int (findComponents(image));

    new_width, filteredBImage, strips, height = PPA(image, width)
    mode, filteredBImage, strips, height = PPA(image, new_width)

    avgBH = removeBlack(np.copy(filteredBImage), strips, new_width);

    img = [];
    for row in avgBH:
        rows = [];
        for ele in row:
            if (ele == 255):
                rows.append(0);
            else:
                rows.append(255);
        img.append(rows);
    img = np.array(img, dtype = np.uint8);
    dilated_img = cv.dilate(img, np.ones((1,4* new_width),np.uint8), iterations=3)

    img = [];
    for row in dilated_img:
        rows = [];
        for ele in row:
            if (ele == 255):
                rows.append(0);
            else:
                rows.append(1);
        img.append(rows);
    img = np.array(img, dtype = np.uint8);

    skel = skeletonize(img)

    sobel_img = sobel_h(skel)
    pro_sobel_img, labels, stats = processSkeleton(np.copy(sobel_img))
    nstats = removeSmallLines(stats)
    image, lines, orig = connectLines(np.copy(pro_sobel_img), strips, new_width, nstats, img, image)

    if filter == True or (lines <= true + 5 and lines >= true - 5):
        return lines;
    else:
        return performAlirezaSegmentation(file_name, true, True)
