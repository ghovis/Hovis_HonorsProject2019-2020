import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

#Created by Gabrielle for mob-suite data
#Adds data from the csv file containing mob-suite output to new columns for each plasmid containing the previous data
#Input: csv file from resGeneEdit function, csv file from cleanMobTyper function
#Output: list with previous data and the new mob-suite data for each plasmid
def addMobData(inputFile, mobFile, organismDict):
    mobDict= {}
    species= ""
    handle= open("newFile.csv", "w")
    newFile= csv.writer(handle)
    #Open file with mob-suite data and read rows
    with open(mobFile,"r") as readcsvfile:
        readMobFile= csv.reader(readcsvfile)
        #For each row, add a new dictionary entry; {(plasmid name) : (the row of mob-suite data in a list form)}
        for row in readMobFile:
            key= row[0].strip()
            value= list(row)
            mobDict.update({key: value})
    #Open output csv file from resGeneEdit function and read rows
    with open(inputFile, "r") as readFile:
        for line in csv.reader(readFile):
            #Check to ensure that there are enough entries to implement the code
            if not (len(line) < 9):
                if (line[6].strip() in organismDict):
                    species= organismDict[str(line[6].strip())]
                    line.append(species)
                #If the plasmid name from inputFile is in the mob-suite dictionary
                if (line[6].strip() in mobDict):
                    #Add the mob-suite data to the inputFile row for the corresponding plasmid and write to the new csv file
                    newFile.writerow(line+mobDict[str(line[6]).strip()])
                #When the plasmid name is not referenced in the mob-suite data, add only the row from inputFile to the new csv file
                else:
                    newFile.writerow(line)
    handle.close()
    return 

#Name of csv file from last run.
inputFilePath= "/Users/ghovis/Documents/Research2019-20/Databases/"
inputFile= fName+"TableOutput.csv"
#Name of csv file with mob_suite data from each plasmid
outMobPath= "/Users/ghovis/Documents/Research2019-20/Databases/"
outMobName= "outMob.csv"
addMobData(inputFilePath+inputFile,outMobPath+outMobName,organismDict)
os.rename(inputFilePath+"newFile.csv",fName+"mobTable.csv")
