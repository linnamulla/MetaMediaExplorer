from datetime import datetime
import pandas as pd

from transformation.dateTimeFilter import filterDateTime

def transformData(sourceFolder: str) -> None:
    df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")

    # Drop the first column of the dataframe
    df: pd.DataFrame = df.drop(df.columns[0], axis = 1)

    # Reorder the columns that contain date and time
    ## Get the columns of the dataframe
    cols = list(df.columns)
    ## Reorder the columns
    colsDateTime: list = cols[7:10] + cols[18:19]
    cols: list = cols[0:7] + cols[10:18] + cols[19:]
    cols[7:7] = colsDateTime
    df: pd.DataFrame = df[cols]

    # Filter the date and time in a new column
    ## Clean values in the recorded column
    for i in range(len(df["recorded"])):
        try:
            if int(str(df["recorded"][i])[0:4]) > datetime.now().year or int(str(df["recorded"][i])[0:4]) < 2000:
                df.loc[i, "recorded"] = None
        except ValueError:
            df.loc[i, "recorded"] = None
    ## Filter the date and time in a new column
    filterDateTime(df)
    df["filtered"] = pd.to_datetime(df["filtered"].astype(str).str.replace(":", "-", 2))

    # Set index as the path column and sort ascending by the filtered column
    df: pd.DataFrame = df.set_index("path")
    df: pd.DataFrame = df.sort_values(by = "filtered", ascending = True)

    # Get the information of the dataframe
    print(df.info(verbose = True, show_counts = True))
    print(df.head(20))

    # Save the dataframe as a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";", index = False)

