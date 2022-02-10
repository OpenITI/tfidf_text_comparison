###########################################################
# The script aggregates results from raw results of TFIDF 
# analysis of known and unknown books, generates TSV data
# with results: 
# - known text (URI/filename)
# - unknown text (filename)
# - distance (TFIDF-based)
# Each file contains results of comparison for a single
# known book; the URI of the book is used as a filename;
# extension .TFIDF is added to the file
###########################################################

###########################################################
# VARIABLES ###############################################
###########################################################

drive = "/Volumes/SandiskSSD/"

metadataFile = "./metadata/OpenITI_metadata_2021-2-5.csv"
releasePath = drive + "/OpenITI_TEMP/_RELEASE/"


foldersToCompare = [
    #drive + "/OpenITI_TEMP/RAWrabica005000/",
    #drive + "/OpenITI_TEMP/RAWrabica010000/",
    #drive + "/OpenITI_TEMP/RAWrabica015000/",
    #drive + "/OpenITI_TEMP/RAWrabica020000/",
    #drive + "/OpenITI_TEMP/RAWrabica025000/",
    #drive + "/OpenITI_TEMP/RAWrabica030000/",
    #drive + "/OpenITI_TEMP/RAWrabica035000/",
    #drive + "/OpenITI_TEMP/RAWrabica040000/",
    #drive + "/OpenITI_TEMP/RAWrabica045000/",
    #drive + "/OpenITI_TEMP/RAWrabicaRafed/",
    #drive + "/OpenITI_TEMP/RAWrabicaSham19Y/",
    #drive + "/OpenITI_TEMP/raw_ShamelaY19/",
    #drive + "/OpenITI_TEMP/RAWrabicaShamAY1/",
    #drive + "/OpenITI_TEMP/RAWrabicaShamAY2/",
    #drive + "/OpenITI_TEMP/RAWrabicaShamAY3/",
    #drive + "/OpenITI_TEMP/RAW_ABLibrary/",
    #drive + "/OpenITI_TEMP/RAW_Masaha/",
    #drive + "/OpenITI_TEMP/RAW_Ghbook/"
]

###########################################################
# VARIABLES ###############################################
###########################################################

import pandas as pd
import numpy as np

import os, io
import re
import random

### necessary libraries
import csv
from datetime import datetime 

###########################################################
###  functions ############################################
###########################################################

startTime = datetime.now()

# loading all the data
def loaData():
    print("=" * 80)
    print(">> Loading OpenITI RELEASE metadata:")
    metadataDic = {}
    with open(metadataFile, 'r') as data:     
        for record in csv.DictReader(data, delimiter='\t'):
            #if record["status"] == "pri" or record["status"] == "sec":
            if record["status"] == "pri" or record["status"] == "sec":
                metadataDic[record["version_uri"]] = record
                metadataDic[record["version_uri"]]["path"] = record["local_path"].replace("../", releasePath)
                #input(record)

    print("Corpus prepared!")
    return(metadataDic)

metadataDic = loaData()

resultsFolder = "./data/"
resultsFolder = "./data_pd/"
resultsRawFolder = "./results_raw/"

lof = sorted(os.listdir(resultsRawFolder))
for f in lof:
    startTimeCycle = startTime
    if not f.startswith(".") and f.endswith(".tsv"):
        libVar = re.sub("results_|_TFIDF_cosine_40000chunks|_?PRI(SEC)?|\.tsv", "", f)
        print("\t", libVar, ":\t",f)

        dfLib = pd.read_csv(resultsRawFolder + f, sep="\t", header=0)
        dfLib["libVar"] = libVar

        URIs = list(set(dfLib["known"]))
        counter = len(URIs)
        print("\t\t", counter)
        for uri in URIs:
            counter -= 1
            if counter % 1000 == 0:
                print("\t\t", counter)

            #print("\t\t", uri)
            dfTemp = dfLib.loc[dfLib["known"] == uri]
            dfTemp = dfTemp[["unknown", "TFIDF_cosine", "libVar"]]   

            mainFileName = resultsFolder + uri + ".tfidf.csv"
            if os.path.isfile(mainFileName):
                mainDF = pd.read_csv(mainFileName, sep=",", header=0)
            else:
                mainDF = pd.DataFrame()

            mainDF = pd.concat([mainDF, dfTemp])
            mainDF = mainDF.reset_index(drop=True)
            mainDF = mainDF.sort_values(by="TFIDF_cosine", ascending=False)
            mainDF.to_csv(mainFileName, sep=",", index=False) 

    timePassedCycle = datetime.now() - startTimeCycle
    print('\tTime for the data file (hh:mm:ss.ms) {}'.format(timePassedCycle))


timeElapsed = datetime.now() - startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
