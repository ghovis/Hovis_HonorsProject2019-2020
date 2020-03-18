import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

#takes output.csv file from GeneTableEdit.py and edits to make more compatible with R
#changes instances of "NA" to "-", cleans ARG names 
#output .csv file of the same format 
#Leslie added ResType and moved most index numbers up 1 
def resGeneEdit(inputFile):
    with open(inputFile,'r') as csvreadfile:
        csvreader = csv.reader(csvreadfile)
        start = ""
        stop = ""
        ResGene1 = ""
        ResGene = ""
        ResType = ""
        BackboneGene = ""
        IncGroup = ""
        PlasmidName = ""
        plasmidNumContigs= ""
        outlist = []
        for line in csvreader:
            start = line[0]
            stop = line[1]
            #cleans/standardizes ARGS by removing subgroups 
            ResGene1 = line[2]
            ResType = line[3]
            ResGene = ResGene1[:4]
            #change "NA's" to hyphen for easier viewing
            if ResGene == "NA":
                ResGene = "-"
            if ResType == "NA":
                ResType = "-"
            BackboneGene = line[4]
            if BackboneGene == "NA":
                BackboneGene = "-"
            IncGroup = line[5]
            PlasmidName = line[6]
            plasmidNumContigs = line[7]
            outlist.append([start,stop,ResGene,ResType,BackboneGene,IncGroup,PlasmidName,plasmidNumContigs])
    return outlist

geneOutputList = resGeneEdit(fName+'EditedGeneTable.csv')
with open(fName+'RCompatibleTable.csv','w') as csvwritefile: #write in output file name 
    csvwriter = csv.writer(csvwritefile)
    csvwriter.writerows(geneOutputList)
