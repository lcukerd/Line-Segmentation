from Louloudis.Implementation import *

import os

accLou = 0;

fileCount = 0;

for fileName in os.listdir('Dataset/'):
    fileName = 'Dataset/' + fileName;
    if '.jpg' in fileName:
        fileCount += 1;
        count = -1;

        with open(fileName.replace('.jpg','.txt'), 'r') as file:
            data = file.read();
            count = data.count('\n');
        if count == -1:
            print ("Error reading text file");

        print (fileName + " True Count: " + str(count));

        countLou = performLouloudisSegmentation(fileName);
        print ("Louloudis: " + str(countLou));
        if (countLou < count + 2 and countLou > count -2):
            accLou += 1;

print ("Accuracy: Louloudis: " + str(accLou / fileCount));
