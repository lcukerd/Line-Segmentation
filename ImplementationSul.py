from Alireza.Implementation import *
from Louloudis.Implementation import *
# from Suleman/Implementation import *
# from Papvassiliou/Implementation import *

import os

accAli = 0;
accLou = 0;
accSul = 0;
accPap = 0;

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

        countAli = performAlirezaSegmentation(fileName);
        print ("Alireza: " + str(countAli));
        if (countAli < count + 2 and countAli > count -2):
            accAli += 1;

        # countLou = performLouloudisSegmentation(fileName);
        # print ("Louloudis: " + str(countLou));
        # if (countLou < count + 2 and countLou > count -2):
        #     accLou += 1;

        # countSul = performSulemanSegmentation(fileName);
        # print ("Suleman: " + str(countAli));
        # if (countSul < count + 2 and countSul > count -2):
        #     accSul += 1;

        # countPap = performPapavassiliouSegmentation(fileName);
        # print ("Papavassiliou: " + str(countAli));
        # if (countPap < count + 2 and countPap > count -2):
        #     accPap += 1;

print ("Accuracy: Alireza: " + str(accAli / fileCount) + " Louloudis: " + str(accLou / fileCount) + " Suleman: " + str(accSul / fileCount) + " Papavassiliou: " + str(accPap / fileCount));
