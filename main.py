from extraction.extractData import extractData
from transformation.transformData import transformData

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

def renameFilesFromDataFrame(df) -> None:
    for index, row in df.iterrows():
        initialPath: str = row['path']
        initialFileName: str = os.path.basename(initialPath)
        newFileName: str = str(row['indicated']) + "_" + str(row['folder']) + "_" + str(row['file'])
        directory: str = os.path.dirname(initialPath)
        newPath: str = os.path.join(directory, newFileName)

        if os.path.exists(initialPath):
            print(f"\nFor file: '{initialFileName}' in directory: '{directory}',")
            confirm = str(input(f"Rename to: '{newFileName}'? (Y/N): "))
            if confirm.upper != "Y":
                shutil.move(initialPath, newPath)
                print(f"\nRenamed '{initialFileName}' to '{newFileName}', in directory: '{directory}'")
            elif confirm.upper == "N":
                print(f"\nDid not rename '{initialFileName}' in directory: '{directory}'")
            else:
                print(f"\nDid not rename '{initialFileName}' in directory: '{directory}'")
        else:
            print(f"File not found: '{initialFileName}' in directory: '{directory}'")

if __name__ == "__main__":
    sourceFolder = main()
    if sourceFolder is not None:
        renameFilesFromDataFrame(df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";"))