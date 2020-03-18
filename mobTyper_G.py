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
#Runs mob_suite on the plasmid sequences then inputs the data from each of the mob_suite output files into a multidimensional list
#Input: lists from isolatePlasmid function output
#Output: multidimensional list of mob_suite data (each new entry contains data for a different plasmid)
def mobTyper (plasmidList, plasmidNames):
    #Desired output folder (in mobsuite directory)
    outFolder= "MobOut"
    #Path for location of the output folder
    mobpath= "/Users/ghovis/mob-suite/mob_suite/"+str(outFolder)
    #Path for plasmid file
    filepath= "/Users/ghovis/Documents/Research2019-20/Databases/"
    #Create list for mob outputs
    mobOutputList= []
    
    for i in range(0,2):
    #for i in range(0,len(plasmidList)):
        #Create a new file to write sequence for one plasmid parsed from the file containing all plasmids
        outUnoPlasmid= open(str(filepath)+"unoPlasmid.fasta","w")
        outUnoPlasmid.write(plasmidList[i])
        os.chdir(filepath)
        os.rename("unoPlasmid.fasta","outPlasmid"+str(i)+".fasta")
        #Run mob_typer on the file containing the sequence of one plasmid (from isolatePlasmid output)
        #Output goes into output directory specified above
        os.system("mob_typer --infile %s --outdir %s" % (str(filepath)+"outPlasmid"+str(i)+".fasta", str(mobpath)))
        #Open mob output file
        newfilepath= str(mobpath)+"/mobtyper_"+"outPlasmid"+str(i)+".fasta_report.txt"
        lineNum= 2
        #Pull mob-suite output data from the file
        line= linecache.getline(newfilepath, lineNum)
        mobOutputList.append(line)
        
    #Edit lines for later conversion to CSV format
    mobOutputList= [entry.replace(",", ";") for entry in mobOutputList]
    mobOutputList= [entry.replace("\t", ",") for entry in mobOutputList]
    return mobOutputList

mobRun= mobTyper(plasmidList, plasmidNames)
with open("outMob.csv","a",newline= '') as csvfile:
    #Make new csv file for mob_suite data of all the plasmids
    writecsv= csv.writer(csvfile, delimiter= "\t", lineterminator= "'", skipinitialspace= "True")
    writecsv.writerow(mobRun)
