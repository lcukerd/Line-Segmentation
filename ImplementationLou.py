from Louloudis.Implementation import *
from multiprocessing import Pool

import os
import sys

def getFiles():
    values = [];
    with open('IAM/lines.txt', 'r') as file:
        data = file.read();
        data = data.split('\n')
        for i in data:
            i = i.split(' ');
            values.append([i[0], i[4]]);
    return values;

def getCountIcdar(fileName):
    with open(fileName.replace('.jpg','.tif.dat'), 'rb') as file:
        data = file.read();
        count = -1;
        for i in data:
            if (i > count):
                count = i;
        if count == -1:
            print ("Error reading text file");
    return count;

def getCountIam(fileName):
    count = int (fileName[1])
    fileName = 'IAM/' + fileName[0] + '.png'
    if count == -1:
        print ("Error reading text file");
    return count, fileName;

def getCountNorm(fileName):
    count = -1;
    with open(fileName.replace('.jpg','.txt'), 'rb') as file:
        data = file.read();
        count = data.count('\n'.encode());
    if count == -1:
        print ("Error reading text file " + fileName);
    return count;

def performComputation(fileName):
    if type == 'iam':
        count, fileName = getCountIam(fileName);
    elif type == 'icdar':
        count = getCountIcdar(fileName);
    else:
        count = getCountNorm(fileName);
    try:
        countLou = performLouloudisSegmentation(fileName, debug);
    except:
        print ('Errored for ' + fileName);
        countLou = count;
    if (countLou <= count + 5 and countLou >= count - 5):
        if (debug == 'd'):
            print ("Correct: Got " + str(countLou) + " / " + str(count) + " for " + fileName);
        return 1;
    else:
        if (debug == 'd'):
            print ("Wrong: Got " + str(countLou) + " / " + str(count) + " for " + fileName);
        return 0;

type = sys.argv[1];
cores = int(sys.argv[2]);
debug = 'n';
if len(sys.argv) == 4:
    debug = sys.argv[3];

if type == 'iam':
    files = getFiles();
elif type == 'icdar':
    files = ['icdar/' + fileName for fileName in os.listdir('icdar/') if '.jpg' in fileName]
else:
    files = ['Dataset/' + fileName for fileName in os.listdir('Dataset/') if '.jpg' in fileName]

print ("Found " + str(len(files)) + " files for " + str(type) + ", working with " + str(cores) +  " cores on " + debug);
accAli = 0;

for i in range(int (len(files)/cores) + (1 if len(files)%cores != 0 else 0)):
    with Pool(cores) as p:
        out = p.map(performComputation, files[i*cores : (i+1)*cores if (i+1)*cores < len(files) else len(files)-1])
    for j in out:
        accAli += j;
    print ("Accuracy:" + str((i+1)*cores) + " Louloudis: " + str(accAli / ((i+1)*cores if (i+1)*cores < len(files) else len(files)-1)));

print ("Accuracy: Louloudis: " + str(accAli / len(files)));
