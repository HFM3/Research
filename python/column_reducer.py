import os
import csv
import shutil

# ======================================================

'''
This script is used for removing unwanted columns from
every CSV within a folder.

Columns that are chosen to remain within the reduced CSV
can be reordered.

All reduced CSVs are saved to a new subfolder. If subfolder
already exists, it will be removed and replaced.

An amalgamation of all reduced CSVs is created.

Original CSVs are not edited

REQUIREMENTS:
Every CSV has the same number of header rows
Every CSV has the same number of header columns
Header columns are identically ordered
'''

# ======================================================
# PARAMETERS TO BE ADJUSTED

# Input - Folder that contains CSV files to be reduced
# All CSV files within folder will be processed
folderPath = "D:\\FilePath"

# Subfolder name - where reduced csv files will be saved
subfolder = "Reduced"

# File extension - should remain as ".csv"
fileExt = ".csv"

# Columns from original csv that will be retained - order can be customized
colsToKeep = [0,4,5,3,2]

# Create combined CSV? True OR False
combineCSVs = True

# ======================================================


def csvReducer(filePath, colsToKeep):
    csvSlim = []
    with open(filePath) as file:
        # read csv
        reader = csv.reader(file)
        # convert csv into list for index capabilities
        csvList = list(reader)

        for i in range(0, len(csvList)):
            # add a new row to csvSlim for each row in original csv
            csvSlim.append([])
            for j in colsToKeep:
                # append selected columns (j) to newly created row (i)
                csvSlim[i].append(csvList[i][j])
    return csvSlim

def csvCombine(folderPath, headerRows):
    csvCombine = []

    count = 0
    for fileName in os.listdir(folderPath):
        if fileName.endswith(".csv"):
            filePath = folderPath + "\\" + fileName

            # append entire first csv to retain header rows
            if count == 0:
                with open(filePath) as file:
                    # read csv
                    reader = csv.reader(file)
                    # convert csv into list for index capabilities
                    csvList = list(reader)

                csvCombine.extend(csvList)

            # if CSV is not the first CSV file in directory, skip header rows and append remainder
            else:
               with open(filePath) as file:
                    # read csv
                    reader = csv.reader(file)
                    # convert csv into list for index capabilities
                    csvList = list(reader)

               csvCombine.extend(csvList[headerRows:])
        count += 1

    print(str(count) + " CSVs have been combined")
    return csvCombine

def csvWriter(filePath, listToWrite):
    with open(filePath,"w") as csvOut:
        writer = csv.writer(csvOut, delimiter=",", lineterminator='\n')
        for i in listToWrite:
            writer.writerow(i)


def main():
    # create sub folder that will hold new csv files
    # If subfolder already exists, clear contents.
    # Subfolder is cleared to prevent combined CSVs from being combined if script is ran consecutively.
    if os.path.exists(folderPath + "\\" + subfolder):
        shutil.rmtree(folderPath + "\\" + subfolder, ignore_errors = True)
        os.makedirs(folderPath + "\\" + subfolder)
        print("SUBFOLDER CLEARED\n")
    else:
        os.makedirs(folderPath + "\\" + subfolder)
        print("SUBFOLDER CREATED\n")


    for fileName in os.listdir(folderPath):
        if fileName.endswith(fileExt):
            filePath = folderPath + "\\" + fileName
            csvSlimmed = csvReducer(filePath, colsToKeep)
            csvWriter(folderPath + "\\" + subfolder + "\\" + fileName[:len(fileName) - len(fileExt)] + "_slim" + fileExt, csvSlimmed)
            print(fileName, "- REDUCED AND SAVED")

    if combineCSVs == True:
        print("\nCombining CSVs...")
        csvFull = csvCombine(folderPath + "\\" + subfolder, 1)
        csvWriter(folderPath + "\\" + subfolder + "\\" + subfolder + "_combined.csv", csvFull)
    else:
        pass

    print("\nFILES SAVED TO:", str(folderPath + "\\" + subfolder), "\n")
    print("COMPLETE")


if __name__=="__main__":
    main()