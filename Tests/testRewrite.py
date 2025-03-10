from main import main
import os
import pandas as pd
import shutil

# Rename the files from the dataframe
def renameFilesFromDataFrame(df) -> None:
    for index, row in df.iterrows():
        # Rename the file
        try:
            # Get the old path from the path column
            oldPath: list[str] = row['path']
            # Create the new name from the value and type columns
            newName: str = str(row['value']) + str(row['type'])
            # Get the directory from the old path
            directory: str = os.path.dirname(oldPath)
            # Create the new path with the new name
            newPath: str = os.path.join(directory, newName)

            # Rename the file
            if os.path.exists(oldPath):
                shutil.move(oldPath, newPath)
                print(f"Renamed '{oldPath}' to '{newPath}'")
            else:
                print(f"File not found: '{oldPath}'")

        except Exception as e:
            # Print the error message
            print(f"Error processing row {index}: {e}")

# Generate a unique value for the files
def generateUniqueValue(df) -> None:
    # Create a dictionary to store the values and a list to store the values
    valuesDict: dict = {}   
    values: list = []

    # Generate the unique value for each file
    for index, row in df.iterrows():
        # Get the folder value
        folderValue: list[str] = row['folder']

        # Check if the folder value starts with "Favorieten"
        # Get the first and last word of the folder value
        isFavorieten: bool = folderValue.startswith("Favorieten")
        if isFavorieten or folderValue.startswith("Overig"):
            words: str = folderValue.split()
            firstWord: str = words[1]
            lastWord: str = words[-1]
        else:
            words: str = folderValue.split()
            firstWord : str = words[0]
            lastWord : str = words[-1]

        # Get the first three characters of the first and last word
        firstThreeFirst: str = firstWord[:3].upper()
        firstThreeLast: str = lastWord[:3].upper()
        baseValue: str = firstThreeFirst + firstThreeLast

        # Check if the base value is not in the dictionary
        if baseValue not in valuesDict:
            valuesDict[baseValue] = 10
            if isFavorieten:
                newValue: str = f"{baseValue}10010"
            else:
                newValue: str = f"{baseValue}00010"
        else:
            count: int = valuesDict[baseValue]
            while True:
                if isFavorieten:
                    newValue: str = f"{baseValue}1{count:04d}"
                else:
                    newValue: str = f"{baseValue}0{count:04d}"
                if newValue not in values:
                    valuesDict[baseValue] = count + 10
                    break
                count += 10

        # Add the value to the list
        values.append(newValue)

    # Add the value column to the dataframe
    df['value'] = values
    
    # Save the dataframe as a csv file
    df.to_csv(path_or_buf=(sourceFolder + "\\.mediaMetaData.csv"), sep=";", index=True)

    # Rename the files
    renameFilesFromDataFrame(df)

sourceFolder = main()
df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep=";")
generateUniqueValue(df)