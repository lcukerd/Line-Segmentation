from Papvassiliou.Implementation import *
from multiprocessing import Pool

import os

def performComputation(fileName):
    count = -1;

    with open(fileName.replace('.jpg','.txt'), 'rb') as file:
        data = file.read();
        count = data.count('\n'.encode());
    if count == -1:
        print ("Error reading text file");
    try:
        countAli = performPapvassiliouSegmentation(fileName);
    except:
        print (fileName);
        countAli = count;
    if (countAli <= count + 5 and countAli >= count - 5):
        return 1;
    else:
        return 0;


files = ['Dataset-old/' + fileName for fileName in os.listdir('Dataset-old/') if '.jpg' in fileName]

print (len(files));

cores = 16;
accAli = 0;

for i in range(int (len(files)/cores) + (1 if len(files)%cores != 0 else 0)):
    with Pool(cores) as p:
        out = p.map(performComputation, files[i*cores : (i+1)*cores if (i+1)*cores < len(files) else len(files)-1])
    for j in out:
        accAli += j;
    print ("Accuracy:" + str((i+1)*cores) + " Alireza: " + str(accAli / ((i + 1) * cores)));

print ("Accuracy: Alireza: " + str(accAli / len(files)));
