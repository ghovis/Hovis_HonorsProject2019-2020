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
#Creates separate files for each plasmid sequence (mob_suite requires separate files for each plasmid) 
#Input: one fasta file with data from multiple plasmids
#Output: list of plasmid sequences, list of plasmid names associated with each sequence
def isolatePlasmid (plasmidFile):
    plasmidList= []
    plasmidNames= []
    organismDict= {}
    organism= ""
    #Open file containing all plasmids
    with open(plasmidFile) as handle:
        #Isolate sequence of one single plasmid
        for plasmidrec in SeqIO.parse(handle,'fasta'):
            sequence= ">"+str(plasmidrec.id)+"\n"+str(plasmidrec.seq)
            plasmidList.append(sequence)
            #Separate ID of plasmid from file denotation and save name of plasmid for future use
            plasmidID= str(plasmidrec.id)
            if (plasmidID[-6:] == ".fasta"):
                plasmidNames.append(plasmidID[:-6])
            elif (plasmidID[-4:] == ".faa"):
                plasmidNames.append(plasmidID[:-4])
            else:
                plasmidNames.append(plasmidID)
            #Make a list of all the host organisms
            
            #descript= [x.strip() for x in plasmidrec.description.split(", ")]
            #print(descript)
            #organism= str(descript[0])
            #organism= organism[14:]
            #print(organism)
            organism1= plasmidrec.description.split()[1]
            organism2= plasmidrec.description.split()[2]
            organism= organism1 + " " + organism2
            #organism= plasmidrec.description.split()[1]
            organismDict.update({plasmidID: organism})
        #print(organismDict)
    return plasmidList,plasmidNames,organismDict

#Path for plasmid file
filepath= "/Users/ghovis/Documents/Research2019-20/Databases/"
#Name of file with multiple plasmids
filename= "1794plasmidSeq_9-6.fasta"
plasmidList, plasmidNames, organismDict= isolatePlasmid(str(filepath)+str(filename))
