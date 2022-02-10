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
resultsFolder = "./data_test/"
resultsRawFolder = "./results_raw/"
lof = sorted(os.listdir(resultsRawFolder))

uris = list(metadataDic.keys())
random.shuffle(uris)

for uri in uris:
    print(uri)
    startTimeCycle = startTime
    if not os.path.isfile(resultsFolder + uri + ".tfidf.tsv"):
        tfidfDic = {}
        for f in lof:
            if not f.startswith(".") and f.endswith(".tsv"):
                libVar = re.sub("results_|_TFIDF_cosine_40000chunks|_?PRI(SEC)?|\.tsv", "", f)
                print("\t", libVar, ":\t",f)
                with open(resultsRawFolder + f, "r", encoding="utf8") as infile:
                    next(infile)
                    for l in infile:
                        l = l.split("\t")
                        val = float(l[2])

                        if uri == l[0]:
                            kNew  = l[0] + "\t" + l[1] + "\t" + libVar
                            if kNew in tfidfDic:
                                tfidfDic[kNew].append(val)
                                #print(kNew)
                                #input(tfidfDic[kNew])
                            else:
                                tfidfDic[kNew] = [val]

                final = ["target\tlib\ttfidfMax"]
                for k,v in tfidfDic.items():
                    toSave = "\t".join(k.split("\t")[1:])
                    #input(toSave)
                    temp = "\t".join([toSave, str(max(v))])
                    final.append(temp)


        entitiesFinalStringIO = io.StringIO("\n".join(final))
        df = pd.read_csv(entitiesFinalStringIO, sep="\t", header=0)
        df = df.sort_values(by="tfidfMax", ascending=False)
        df.to_csv(resultsFolder + uri + ".tfidf.tsv", sep="\t", index=False)

        timePassedCycle = datetime.now() - startTimeCycle
        print('\tTime for the URI (hh:mm:ss.ms) {}'.format(timePassedCycle))


timeElapsed = datetime.now() - startTime
print('Time elapsed (hh:mm:ss.ms) {}'.format(timeElapsed))
