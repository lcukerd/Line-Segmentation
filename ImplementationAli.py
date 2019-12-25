from Alireza.Implementation import *

import os

accAli = 0;

fileCount = 0;
true = [];
calc = [];

for fileName in os.listdir('Dataset/'):
    fileName = 'Dataset/' + fileName;
    if '.jpg' in fileName:
        print (fileName + " " + str(fileCount))
        fileCount += 1;
        count = -1;

        with open(fileName.replace('.jpg','.txt'), 'rb') as file:
            data = file.read();
            count = data.count('\n'.encode());
        true.append(count);
        if count == -1:
            print ("Error reading text file");

        print ("True Count: " + str(count));

        print ("Alireza:", end = " ");
        countAli = performAlirezaSegmentation(fileName, count, False);
        print (str(countAli), end  = " ");
        calc.append(countAli);
        if (countAli <= count + 2 and countAli >= count - 2):
            accAli += 1;
            print ("Passed");
        else:
            print ("Failed");

print ("Accuracy: Alireza: " + str(accAli / fileCount));
