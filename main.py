from extraction.extraction import extractData
from transformation.transformationMain import transformData

import os
import pandas as pd
import shutil

from tempname import renameFilesFromDataFrame

def main() -> str:
    while True:
        print("\nPlease enter name of source folder, or type \"break\" to break:")
        sourceFolder: str = input("")
        if sourceFolder == "break":
            print("\nProgram has been broken.\n")
            sourceFolder = None
            break
        else:
            print("running extraction")
            extractData(sourceFolder)
            print("running transformation")
            transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
            break
            
if __name__ == "__main__":
    sourceFolder = main()
    print(f"renaming in Source folder: {sourceFolder}")
    renameFilesFromDataFrame(df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";"))