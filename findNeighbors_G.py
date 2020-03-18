import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

#takes gene table and finds the nearest backbone genes up and downstream of every ARG
#input file:file created by prokkaReformat.py
#output file is .csv of ARG (with ARG type), upstream BG, downstream BG, inc group, and plasmid name 
def findNeighbors(filePath):
    with open(filePath,'r') as  csvreadfile:
        csvreader = csv.reader(csvreadfile)
        tempN1 = ""
        N1 = ""
        N2 = ""
        outList = []
        resList = []
        afterRES = False 
        for line in csvreader:
        	#set gene in BG column to upstream neighbor temporarily
            if not line[4] == "NA" and afterRES == False:
                tempN1 = line[4]
            #if theres an ARG, set temp upstream neighbor to neighbor1 and assign ARG
            if not line[2] == "NA":
                N1 = tempN1
                resName = line[2]
                resType = line[3]#inserted by Leslie
                afterRES = True 
                #resLIst accounts for the possibility of multiple ARGS in row
                resList.append([resName, resType])#resType inserted by Leslie 
            #first BG that occurs after the res gene is neighbor 2 (downstream)
            if not line[4] == "NA" and afterRES == True:
                N2 = line[4]
                afterRES = False
                #Account for absent data.
                if len(line) > 9:
                    Plasmid= line[6]
                    Inc= line[14]
                else:
                    Plasmid= "NA"
                    Inc= "NA"
                if not line[14] == None:
                    Inc= line[14]
                else:
                    Inc= "NA"
                #every ARG in a cluster will share the same up/downstream BG neighbors
                for gene in resList:
                    #Careful to run this function only after obtaining the MOB table
                    outList.append([gene,N1,N2,Inc,Plasmid])#resType inserted by Leslie, Gabrielle changed line[5] to line[14] to incorporate reliable inc groups from MOB-suite
                tempN1 = line[4]
                resList = []
    return outList
    
newNeighbors = findNeighbors('/Users/ghovis/Documents/Research2019-20/Databases/'+fName+'mobTable.csv')
with open(fName+'Neighbors.csv','w') as csvwritefile:
    csvwriter = csv.writer(csvwritefile)
    csvwriter.writerows(newNeighbors) 
