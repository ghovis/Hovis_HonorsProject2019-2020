import sys
import re
import csv
import copy
import os
import linecache
from collections import defaultdict
from Bio import SeqIO

csv.field_size_limit(100000000)

def rowsFromProkka(inFile, dbDelim = ".faa"):
	### Note that infile is a .csv file of output from Prokka
    	# Input 
	#	inFile = csv file for reading Prokka output
	# 	dbDelim = the key indicating user defined database in the Prokka output
	# Output
	#	outlist = a list of each CDS's data formatted as
	# 	(start, stop, arg, arg type, bg, inc croup, plasmidName, keep (Boolean indicating if it was from a passed in database)
	with open(inFile, "r") as csvfile:

		csvreader = csv.reader(csvfile, delimiter= '\t')

		#create an empty dictionary to temporarily hold the information for one gene	
		tempout = {"start" : "NA", "stop" : "NA", "geneName" : "NA", "plasmidName" : "NA", 'keep' : False, "plasmidFileId" : "NA", "plasmidNumContigs" : "NA"}
		outlist = []

		for line in csvreader: 
			# identify lines specifying the start of a new plasmid
			if len(line) == 1 and line[0].find(">")==0:
				# identify when the plasmids are switching and write out the previous record
				outlist.append([tempout[I] for I in tempout])
				# clear tempout
				tempout = {"start" : "NA", "stop" : "NA", "resName" : "NA", "resType" : "NA", "geneName" : "NA","incGroup" : "NA",\
				 "plasmidName" : line[0][line[0].index(" "):], 'keep' : False, "plasmidNumContigs" : "NA"}

			# identify rows starting a new CDS
			elif len(line) == 3 and line[2] == 'CDS':
				outlist.append([tempout[I] for I in tempout])
				# replace values in tempout, note that we only need to 
				# replace the plasmid name when we get to a new plasmid
				tempout["start"] = line[0]
				tempout["stop"] = line[1]
				tempout["geneName"] = "NA" 
				tempout["resName"] = "NA" 
				tempout["resType"] = "NA"
				tempout["incGroup"] = "NA"
				tempout["plasmidFileId"] = "NA"
				tempout["plasmidNumContigs"] = "NA"
				tempout['keep'] = False
		
			# identify if the CDS is from database and tag for keeping
			elif len(line)>4 and line[3] == 'inference' and ((line[4].find(dbDelim)>-1) or (line[4].find('ISfinder'))):
				tempout['keep'] = True
		
			# identify the gene name if it has one
			elif len(line)>4 and line[3] == 'product':
				if "group" not in line[4] and "RES" not in line[4]:
					tempout['geneName'] = line[4]
					tempout['incGroup'] = "NA"
					tempout['resName'] = "NA"
					tempout["resType"] = "NA"                    
				if "group" in line[4]:
					tempout['incGroup'] = line[4]
					tempout['geneName'] = "NA"
					tempout['resName'] = "NA"
					tempout["resType"] = "NA"                    
				if "RES" in line[4]:
					tempout['resName'] = line[4]
					tempout['geneName'] = "NA"
					tempout['incGroup'] = "NA"
					tempout["resType"] = "NA"
				if "_:_" in line[4]:
					resToList = line[4].split("_:_")
					tempout['resName'] = resToList[0]
					tempout['geneName'] = "NA"
					tempout['incGroup'] = "NA"
					tempout['resType'] = resToList[1]					                    
	return outlist

def cleanList(CDSlist):
	### function removes rows that were not from the current database
	# Input
	#	CDSlist = a list of the information contained for each CDS in one row. 
	#		Last element determines if it was from user defined database
	# Out
	#	returns a list of only the rows from CDS's from our database, 
	#	removes column identifying keeper rows
	return [row[:-1] for row in CDSlist if row[-1]]


#INPUT: Prokka will output 10 files, this function takes in the file from Prokka ending in .tbl.
#OUTPUT: Function will output a .csv file with the start index, stop index, ARG name, Backbone Gene Name, 
#fName begins each file name to identify output files
fName = "FileName"
with open(fName+'TableOutput.csv','w') as csvfile: #name of output file here
    csvwriter = csv.writer(csvfile)
#Use the following loop if PROKKA returned multiple files. Number each file accordingly.
    for i in range(1,19):
        cleanedUp = (cleanList(rowsFromProkka("PROKKA_06282019 ("+str(i)+").tbl"))) #Edit to match names of PROKKA files.
        csvwriter.writerows(cleanedUp)
