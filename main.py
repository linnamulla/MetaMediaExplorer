from extraction.extraction import extractData
from transformation.transformation import transformData

import os
import pandas as pd
import shutil

#### RENAMING FILES ####
## This module is used to rename files based on the metadata stored in a DataFrame. It reads the metadata from a CSV file, checks for duplicates in the 'indicated' column, and renames files accordingly. The new file names are constructed using the 'indicated', 'folder', and 'file' columns from the DataFrame, while removing any non-alphabetic characters.

# This function removes all non-alphabetic characters from a string.
def removeNonAlpha(fileString: str) -> str:
    return ''.join(character for character in fileString if character.isalpha())

# This function renames files based on the metadata stored in a DataFrame.
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
#### ####



#### MAIN FUNCTION ####        
## This is the main function that runs the program. It prompts the user for the source folder, checks if it exists, and then calls the extractData and transformData functions to extract and transform the data. It also reads the CSV file and renames files based on the DataFrame.

def main() -> None: 
    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")

    # Check if the source folder is provided and exists
    if sourceFolder is None:
        print("No source folder provided. Exiting program.")
        exit()
    elif not os.path.exists(sourceFolder):
        print(f"Source folder '{sourceFolder}' does not exist. Exiting program.")
        exit()
    else:
        # Attempt to extract and transform data from the source folder
        extractData(sourceFolder)
        transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
        print("\nData extraction and transformation completed successfully.\n")

        # Attempt to read the CSV file and rename files based on the DataFrame
        print("\nRenaming files based on metadata...\n")
        try:
            while False:
                renameFilesFromDataFrame(df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";"))
        
    # Handle potential errors when reading the CSV file or renaming files
        except FileNotFoundError as e:
            print(f"File not found: {e}. Please ensure the CSV file exists in the source folder.")
            exit()
        except KeyError as e:
            print(f"Key error occurred: {e}. Please check the column names in the CSV file.")
            exit()
        except OSError as e:
            print(f"OS error occurred: {e}. Exiting program.")
            exit()
        except ValueError as e:
            print(f"Value error occurred: {e}. Please check the data in the CSV file.")
            exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Exiting program.")
            exit()

#### ####



#### RUN THE MAIN FUNCTION ####
# This ensures that the main function is called when the script is run directly.
if __name__ == "__main__":
    main()
    print("\nProgram completed successfully.")
    exit()
#### ####