import pandas as pd
import os
import shutil

def removeNonAlpha(string: str) -> str:
    return ''.join(c for c in string if c.isalpha())

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