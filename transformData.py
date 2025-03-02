from datetime import datetime
import pandas as pd

from transformation.dateTimeFilter import select_date_time

def transformData(sourceFolder: str) -> None:
    df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")

    # Reorder the columns that contain date and time
    ## Get the columns of the dataframe
    cols = list(df.columns)
    ## Reorder the columns
    colsDateTime = cols[7:10] + cols[18:19]
    cols = cols[0:7] + cols[10:18] + cols[19:]
    cols[7:7] = colsDateTime
    df = df[cols]

    # Clean values in the recorded column
    for i in range(len(df["recorded"])):
        try:
            if int(str(df["recorded"][i])[0:4]) > datetime.now().year or int(str(df["recorded"][i])[0:4]) < 2000:
                df.loc[i, "recorded"] = None
        except ValueError:
            df.loc[i, "recorded"] = None

    # Add a column for the program and reorder the columns
    ## Combine the columns for app and software
    df["program"] = df["app"].astype(str) + "; " + df["Software"].astype(str)
    ## Reorder the columns
    cols = list(df.columns)
    colsAppSoftware = cols[11:12] + cols[23:24] + cols[42:43]
    cols = cols[0:11] + cols[12:23] + cols[24:42]
    cols[11:11] = colsAppSoftware
    df = df[cols]

    # Drop the columns that are empty
    df = df.dropna(axis = 1, how = "all")

    select_date_time(df)

    # Get the information of the dataframe
    print(df.info(verbose = True, show_counts = True))

    # Save the dataframe as a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";", index = False)

