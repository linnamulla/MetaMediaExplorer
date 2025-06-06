import pandas as pd
import os

# Assuming these are in transformation/datetimeFilter.py and can be imported at the top
from transformation.datetimeFilter import filterDateTime, selectDateTime

#### DATA TRANSFORMATION ####
"""
This module transforms metadata extracted from image and video files. It reads metadata
from a CSV, cleans and selects date/time columns, sets the index, sorts the DataFrame,
and optionally drops empty or float columns. The transformed data is then saved back
to the CSV file.
"""

def transformData(sourceFolder: str, dropEmptyCols: bool = True, dropFloatCols: bool = True) -> None:
    """
    Transforms metadata from a CSV file.

    Args:
        sourceFolder (str): The path to the folder containing the .mediaMetaData.csv file.
        dropEmptyCols (bool): If True, drops columns that are entirely empty (NaN).
        dropFloatCols (bool): If True, drops float64 columns, except for "GPSInfo".
    """
    csvFilePath = os.path.join(sourceFolder, ".mediaMetaData.csv")

    try:
        # Use index_col=0 if the first column is always an unnamed index from a previous save.
        # This prevents pandas from creating a new default index and avoids the need to drop it later.
        df = pd.read_csv(csvFilePath, sep=";", index_col=0)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csvFilePath}. Transformation aborted.")
        return
    except pd.errors.EmptyDataError:
        print(f"Warning: CSV file at {csvFilePath} is empty. No data to transform.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}. Transformation aborted.")
        return

    # Filter and select date and time columns
    # Assuming filterDateTime and selectDateTime modify the DataFrame in-place.
    filterDateTime(df, columnName="recorded")
    filterDateTime(df, columnName="DateTime")
    selectDateTime(df)

    # Set index as the path column and sort descending by the "indicated" column
    df = df.set_index("path").sort_values(by="indicated", ascending=False)

    # Drop empty columns if requested
    if dropEmptyCols:
        df = df.dropna(axis=1, how="all")

    # Drop columns with data type float64, except the GPSInfo column, if requested
    if dropFloatCols:
        floatCols = df.select_dtypes(include=["float64"]).columns
        # Drop columns that are float64 type, but exclude "GPSInfo"
        colsToDrop = floatCols.difference(["GPSInfo"])
        df = df.drop(columns=colsToDrop)

    # Get and print the information of the DataFrame
    # df.info() prints directly to stdout and returns None.
    print("\n--- DataFrame Information ---") # A simpler, clear header
    df.info(verbose=True, show_counts=True)

    # Save the transformed DataFrame to a CSV file
    df.to_csv(csvFilePath, sep=";", index=True)