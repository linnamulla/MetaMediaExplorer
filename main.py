from extraction.extraction import extractData
from transformation.transformation import transformData

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
            extractData(sourceFolder)
            transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
            print("\nData extraction and transformation completed successfully.\n")
            return sourceFolder
            
def removeNonAlpha(s):
    return ''.join(c for c in s if c.isalpha())

def renameFilesFromDataFrame(df: pd.DataFrame) -> None:
    # Create a Series to keep track of the counts for each 'indicated' value
    indicated_counts = {}

    for index, row in df.iterrows():
        initialPath: str = row['path']
        initialFileName: str = os.path.basename(initialPath)
        
        original_indicated = str(row['indicated'])
        
        # Check for duplicates and append appropriate suffix
        if original_indicated not in indicated_counts:
            indicated_counts[original_indicated] = 0
            current_indicated = f"{original_indicated}_0"
        else:
            indicated_counts[original_indicated] += 1
            current_indicated = f"{original_indicated}_{indicated_counts[original_indicated]}"
            
        # Update the 'indicated' value for the current row with the suffixed version
        # This modification is only for the current iteration's newFileName construction
        # It does not alter the original DataFrame in place, which is generally safer
        # if you need the original 'indicated' for other purposes later.
        row_indicated_for_filename = current_indicated


        if removeNonAlpha(str(row['file']).split('.')[0]) != "":
            newFileName: str = row_indicated_for_filename + "_" + \
                               removeNonAlpha(str(row['folder'])) + "_" + \
                               removeNonAlpha(str(row['file']).split('.')[0]) + \
                               str(row['type'])
        else:
            if removeNonAlpha(str(row['folder'])) == "":
                newFileName: str = row_indicated_for_filename + \
                str(row['type'])
            else:
                newFileName: str = row_indicated_for_filename + "_" + \
                removeNonAlpha(str(row['folder'])) + \
                str(row['type'])
            
        directory: str = os.path.dirname(initialPath)
        newPath: str = os.path.join(directory, newFileName)

        if os.path.exists(initialPath):
            try:
                shutil.move(initialPath, newPath)
                print(f"Renamed '{initialFileName}' to '{newFileName}', in directory: '{directory}'")
            except Exception as e:
                print(f"Error renaming '{initialFileName}' to '{newFileName}': {e}")
        else:
            print(f"File not found: '{initialFileName}' in directory: '{directory}'")
            
if __name__ == "__main__":
    sourceFolder = main()
    print(f"Source folder: {sourceFolder}")
    if sourceFolder is None:
        print("No source folder provided. Exiting program.")
        exit()
    else:
        try:
            _ = None
            renameFilesFromDataFrame(df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";"))
        except FileNotFoundError:
            print(f"File not found: '{sourceFolder}\\mediaMetaData.csv'. Please ensure the file exists before renaming files. Exiting program.")