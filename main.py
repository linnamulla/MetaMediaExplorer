from extraction.extractionMain import extractData
from transformation.transformationMain import transformData

import os
import pandas as pd
import shutil

def main() -> str:
    while True:
        print("\nPlease enter name of source folder, or type \"break\" to break:")
        sourceFolder: str = input("")
        if sourceFolder == "break":
            print("\nProgram has been broken.\n")
            sourceFolder = None
            return sourceFolder
        else:
            try:
                extractData(sourceFolder)
                transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
            except OSError as e:
                print(str(e), "OSError. Likely causes are: (1) files are being downloaded from cloud access and can't be accessed, or (2) the .csv file is opened by the user and can't be overwritten.", sep = "\n")
            except ValueError as e:
                print(str(e), "ValueError. Please enter a valid source folder.", sep = "\n")
            finally:
                return sourceFolder
            
def removeNonAlpha(s):
    return ''.join(c for c in s if c.isalpha())

def renameFilesFromDataFrame(df) -> None:
    for index, row in df.iterrows():
        initialPath: str = row['path']
        initialFileName: str = os.path.basename(initialPath)
        if removeNonAlpha(str(row['file']).split('.')[0]) != "":
            newFileName: str = str(row['indicated']) + "_" + removeNonAlpha(str(row['folder'])) + "_" + removeNonAlpha(str(row['file']).split('.')[0]) + str(row['type'])
        else:
            newFileName: str = str(row['indicated']) + "_" + removeNonAlpha(str(row['folder'])) + str(row['type'])
            
        directory: str = os.path.dirname(initialPath)
        newPath: str = os.path.join(directory, newFileName)

        if os.path.exists(initialPath):
                shutil.move(initialPath, newPath)
                print(f"Renamed '{initialFileName}' to '{newFileName}', in directory: '{directory}'")
        else:
            print(f"File not found: '{initialFileName}' in directory: '{directory}'")

if __name__ == "__main__":
    sourceFolder = main()
    if sourceFolder is not None:
        try:
            renameFilesFromDataFrame(df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";"))
        except FileNotFoundError:
            print(f"File not found: '{sourceFolder}\\mediaMetaData.csv'. Please ensure the file exists before renaming files. Exiting program.")