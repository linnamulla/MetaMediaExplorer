import pandas as pd
import re
from transformation.datetime.datetimeFilter import reorderColumns, filterDateTime, selectDateTime
from transformation.datetime.datetimeEstimation import estimateStamp

def transformData(sourceFolder: str, dropEmptyCols: bool = True, dropFloatCols: bool = True) -> None:
    df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")

    def estimateStamp(sourceFolder: str) -> None:
        def processString(inputString):
            """
            Reads a string, removes all non-numerical characters,
            cuts off everything after the 14th character.
            Then, applies conditional formatting based on the resulting length:
            - If less than 8 characters, the result is empty.
            - If exactly 8 characters, no spaces are added.
            - If 9, 10, 11, or 13 characters, everything after the 8th character is removed.
            - Otherwise (12 or 14 characters), a space is added after the 8th character.

            Args:
                inputString (str): The string to be processed.

            Returns:
                str: The processed string according to the new rules.
            """
            # Ensure input is treated as a string, especially if it might be a non-string type like None or NaN
            if not isinstance(inputString, str):
                inputString = str(inputString)

            # Step 1: Remove all non-numerical characters
            numericalString = re.sub(r"[^0-9]", "", inputString)

            # Step 2: Cut off everything after the 14th character
            truncatedString = numericalString[:14]

            finalString = ""
            currentLength = len(truncatedString)

            # Step 3: Apply new conditional checks based on length
            if currentLength < 8:
                # If less than 8 characters, make the result empty
                finalString = ""
            elif currentLength == 8:
                # If exactly 8 characters, don't add any spaces
                finalString = truncatedString
            elif currentLength in [9, 10, 11, 13]:
                # If 9, 10, 11, or 13 characters, remove everything after the 8th character
                finalString = truncatedString[:8]
            else:  # This covers lengths 12 and 14 due to earlier truncation
                # Otherwise, add a space after the 8th character
                finalString = truncatedString[:8] + " " + truncatedString[8:]

            return finalString
        df["recorded"] = df["file"].apply(processString)
    estimateStamp(sourceFolder)

    # Reorder the columns of the dataframe, filter the date and time columns and select the date and time column
    reorderColumns(df)
    filterDateTime(df)
    selectDateTime(df)

    # Set index and sort the dataframe
    ## Drop the first column of the dataframe
    df: pd.DataFrame = df.drop(df.columns[0], axis = 1)
    ## Set index as the path column and sort descending by the filesize column
    df: pd.DataFrame = df.set_index("path")
    df: pd.DataFrame = df.sort_values(by = "filesize", ascending = False)

    # Drop the empty columns of the dataframe
    if dropEmptyCols == True:
        df: pd.DataFrame = df.dropna(axis = 1, how = "all")

    # Drop columns with data type float64, except the GPSInfo column
    if dropFloatCols == True:
        df: pd.DataFrame = df.drop(df.select_dtypes(include = ["float64"]).columns.difference(["GPSInfo"]), axis = 1)

    # Get the information of the dataframe
    print("\nShowing columns for dataframe:\n")
    print(df.info(verbose = True, show_counts = True))

    # Save the dataframe as a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";", index = True)

