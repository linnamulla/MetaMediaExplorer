import pandas as pd

#### DATA TRANSFORMATION ####
## This module is used to transform the data extracted from image and video files. It reads the metadata from a CSV file, filters and selects date and time columns, sets the index, sorts the dataframe, drops empty columns, and drops float columns (except for GPSInfo). The transformed data is then saved back to the CSV file.

def transformData(sourceFolder: str, dropEmptyCols: bool = True, dropFloatCols: bool = True) -> None:

    # Read the metadata from the CSV file
    df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")

    # Filter and select date and time columns
    from transformation.datetimeFilter import filterDateTime, selectDateTime
    ## This function cleans up the date and time columns in the dataframe by filtering out invalid values and selecting the most appropriate date/time value for each row.
    filterDateTime(df, columnName = "recorded")
    filterDateTime(df, columnName = "DateTime")
    ## This function selects the most appropriate date/time value for each row based on a set of rules and inserts it into a new column.
    selectDateTime(df)

    # Set index and sort the dataframe
    ## Drop the first column of the dataframe
    df: pd.DataFrame = df.drop(df.columns[0], axis = 1)
    ## Set index as the path column and sort descending by the filesize column
    df: pd.DataFrame = df.set_index("path")
    df: pd.DataFrame = df.sort_values(by = "indicated", ascending = False)

    # Drop the empty columns of the dataframe
    if dropEmptyCols == True:
        df: pd.DataFrame = df.dropna(axis = 1, how = "all")

    # Drop columns with data type float64, except the GPSInfo column
    ## This removes columns that are of type float64, which are typically used for numerical data, but keeps the GPSInfo column if it exists. This is useful for cleaning up the dataframe and removing unnecessary columns that may not be relevant for further analysis.
    if dropFloatCols == True:
        df: pd.DataFrame = df.drop(df.select_dtypes(include = ["float64"]).columns.difference(["GPSInfo"]), axis = 1)

    # Get the information of the dataframe
    print("\nDataframe information:")
    print("Columns in current dataframe:\n")
    print(df.info(verbose = True, show_counts = True))

    # Save the transformed dataframe to a CSV file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";", index = True)

#### ####