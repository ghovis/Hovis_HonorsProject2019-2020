import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

#function takes in a parameter, the parameter will be an absolute file pathway
# to the gene table file (should be .csv file from prokkaReformat.py)
#(ex:/Users/marielelensink/Documents/H2/GeneTable1Edit.csv)
#output is  another gene table that is compatible with R
#Gabrielle altered to add incompatibility group 
#Leslie just changes all the numbers up one basically
def geneTableEditor(filePath):
    with open(filePath, 'r') as csvreadfile:
        csvreader = csv.reader(csvreadfile)
        incList= []
        #Create default dictionary for incompatibility (inc) groups 
        dDict= defaultdict(list)
        outList = []
        plasmid = ""
        for line in csvreader:
            if not (line[0] == "NA" and line[1] == "NA"):
                plasmid = line[6]
                plasmid = plasmid.strip()
                if not line[5] == 'NA':
                    incOld= line[5]
                    #Splice inc group name to make it easier to read
                    incSave= incOld[5:10]
                    #Add plasmid and inc group pairs to list
                    incList.append([plasmid, incSave])
                #Add all the inc groups to each plasmid key in the default dictionary
                for plasmid, incSave in incList:
                    dDict[plasmid].append(incSave)
    #Write the data for each plasmid to a new file
    with open(filePath, 'r') as csvreadfile:
        csvreader = csv.reader(csvreadfile)  
        resName1 = ""
        for line in csvreader:
            #nullrow is a count variable to indicate if values were assigned to a row for writing to the new spreadsheet.
            nullrow= 1
            #Avoid entering a gene without values (specifically the start and end positions)
            if not (line[0] == "NA" and line[1] == "NA"):
                start= line[0]
                stop = line[1]
                if "RES" in line[2]:
                    resName1 = line[2]
                    resName = resName1[3:]
                    resType = line[3]
                else:
                    resName = line[2]
                    resType = line[3]
                    geneName = line[4]
                    parseinc = line[5]
                    plasmid = line[6]
                    plasmidNumContigs = line[7]
                    parseinc = parseinc[5:10]
                    nullrow= 0
                    #Ensure that all the inc groups will be listed for each plasmid 
                    countplasmid = 0
                    for i in dDict.keys():
                        key= str(plasmid)
                        key= key.strip()
                        if (key == str(i)):
                            countplasmid += 1
                            curincs= dDict[key]
                            lencurincs= len(curincs)
                            count= 0
                            if (lencurincs > 1):
                                for j in range(0,lencurincs):
                                    oneinc= str(curincs[j])
                                    if (oneinc == parseinc):
                                        count += 1
                                if (count == 0):
                                    incgroup= ",".join(dDict[key])
                                    break
                            else:
                                if (str(curincs) != str(parseinc)):
                                    incgroup= ",".join(dDict[key])
                                    break
                    if (countplasmid == 0):
                        incgroup= "other"
                    if (nullrow == 0):
                        outList.append([start,stop,resName,resType,geneName,incgroup,plasmid,plasmidNumContigs])
    return outList    


editedTable = geneTableEditor("/Users/ghovis/Documents/Research2019-20/Databases/"+fName+"TableOutput.csv")#name of input file from prokkareformat
with open(fName+'EditedGeneTable.csv','w') as csvwritefile:#need to change the input here
    csvwriter = csv.writer(csvwritefile)
    csvwriter.writerows(editedTable)
