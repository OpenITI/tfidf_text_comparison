import os

drive = "/Volumes/SandiskSSD/"

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
    drive + "/OpenITI_TEMP/RAW_Masaha/",
    #drive + "/OpenITI_TEMP/RAW_Ghbook/"
]

for folder in foldersToCompare:
    lof = os.listdir(folder)

    for f in lof:
        if not f.startswith("."):
            print(folder + f)
            with open(folder + f, "r", encoding="utf8") as f1:
                test = f1.read()