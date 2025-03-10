import pandas as pd
from transformation.dateTimeFilter import reorderColumns, filterDateTime, selectDateTime

def transformData(sourceFolder: str, dropEmptyCols: bool = True, dropFloatCols: bool = True) -> None:
    df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")

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
    print(df.info(verbose = True, show_counts = True))

    # Save the dataframe as a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";", index = True)

