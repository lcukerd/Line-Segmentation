from matplotlib import pyplot as plt
from pylab import rcParams
import cv2 as cv
import math

def loadImage(fileName):
    src = cv.imread(cv.samples.findFile(fileName), 0)
    if src is None:
        print ('Error opening image!')
    return src

def imshow_components(labels):
    # Map component labels to hue val
    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv.cvtColor(labeled_img, cv.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0
    plt.imshow(labeled_img)
    plt.show()

def showLines(lines, DemoImg):
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv.line(DemoImg, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    plt.imshow(DemoImg);
