import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

#Created by Gabrielle for mob_suite data
#A default mob_suite run creates output files using the file name as the plasmid identifier. The file name must be replaced with the name of the plasmid when this data is utilized.
#Replaces file name in plasmid identifier column with the name of the plasmid
#Input: csv file from mobTyper function, list of plasmid names created in isolatePlasmid function
#Output: new list with edited mob_suite data (file name replaced with plasmid name)
def cleanMobTyper (mobFile, plasmidNames):
    outFilePath= "/Users/ghovis/Documents/Research2019-20/Databases/"
    outFileName= "outMob.csv"
    #Create new list for edited output from mobTyper function
    newMobOutput= []
    with open(outFilePath+outFileName,"r") as openmob:
        mobreader= csv.reader(openmob,skipinitialspace= "True")
        i= 0
        for line in mobreader:
            #Clear empty entries
            if (len(line) == 1):
                line= ""
            else:
                #Replace name of file with name of associated plasmid
                newPName= str(plasmidNames[i])
                line[0]= newPName
                newMobOutput.append(line)
                if (i < (len(plasmidNames)-1)):
                    i += 1
    #Delete files in output directory
    #os.unlink(outFilePath+outFileName)
    for i in range(0,2):
    #for i in range(0,len(plasmidNames)):
        os.unlink(outFilePath+"outPlasmid"+str(i)+".fasta")
    return newMobOutput

#Name of csv file from mobRun output
mobfile= "outMob.csv"
cleanMob= cleanMobTyper(filepath+mobfile,plasmidNames)
with open("replaceFile.csv","a",newline= '') as replaceFile:
    writenew= csv.writer(replaceFile, skipinitialspace= "True")
    for i in range(0,len(cleanMob)):
        writenew.writerow(cleanMob[i])
    #Replace the mobRun output file with the edited spreadsheet from the cleanMob function
    os.rename(filepath+"replaceFile.csv","outMob.csv")
