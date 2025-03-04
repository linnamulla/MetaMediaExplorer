from datetime import datetime
import pandas as pd

def reorderTimeColumns(df: pd.DataFrame) -> None:
    # Reorder the columns that contain date and time
    ## Get the columns of the dataframe
    cols = list(df.columns)
    ## Reorder the columns
    colsDateTime: list = cols[6:9] + cols[17:18]
    cols: list = cols[0:6] + cols[9:17] + cols[19:]
    cols[6:6] = colsDateTime
    df: pd.DataFrame = df[cols]

def cleanDateTime(df: pd.DataFrame) -> None:
    ## Clean values in the recorded column
    for i in range(len(df["recorded"])):
        try:
            if int(str(df["recorded"][i])[0:4]) > datetime.now().year or int(str(df["recorded"][i])[0:4]) < 2000:
                df.loc[i, "recorded"] = None
        except ValueError:
            df.loc[i, "recorded"] = None

def findLikelyTime(df, dateTimeCol='DateTime', recordedCol='recorded', modifiedCol='modified', creationCol='creation', newCol='filtered') -> None:

    filtered = []
    for index, row in df.iterrows():
        try:
            dateTimeVal = int(str(row[dateTimeCol])[:4]) if pd.notna(row[dateTimeCol]) else None
            try:
                recordedVal = int(str(row[recordedCol])[:4]) if pd.notna(row[recordedCol]) else None
            except KeyError:
                recordedVal = None
            modifiedVal = int(str(row[modifiedCol])[:4]) if pd.notna(row[modifiedCol]) else None
            creationVal = int(str(row[creationCol])[:4]) if pd.notna(row[creationCol]) else None

            if dateTimeVal:
                filtered.append(row[dateTimeCol])
            elif recordedVal and modifiedVal and recordedVal == modifiedVal:
                filtered.append(row[recordedCol])
            elif recordedVal and modifiedVal and recordedVal < modifiedVal:
                filtered.append(row[recordedCol])
            elif recordedVal and creationVal and modifiedVal == creationVal:
                filtered.append(row[modifiedVal])
            elif modifiedVal and creationVal and modifiedVal < creationVal:
                filtered.append(row[modifiedCol])
            else:
                filtered.append(row[creationCol])
        except ValueError:
            filtered.append(None)

    df.insert(6, newCol, filtered)

    df["filtered"] = pd.to_datetime(df["filtered"].astype(str).str.replace(":", "-", 2))

    return df