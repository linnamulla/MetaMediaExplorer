from datetime import datetime
import pandas as pd

def reorderColumns(df: pd.DataFrame) -> None:
    # Reorder the columns that contain date and time
    ## Get the columns of the dataframe
    cols = list(df.columns)
    ## Reorder the columns
    colsDateTime: list = cols[6:9] + cols[17:18]
    cols: list = cols[0:6] + cols[9:17] + cols[19:]
    cols[6:6] = colsDateTime
    df: pd.DataFrame = df[cols]

def filterDateTime(df: pd.DataFrame) -> None:
    ## Clean values in the recorded column
    for i in range(len(df["recorded"])):
        try:
            if int(str(df["recorded"][i])[0:4]) > datetime.now().year or int(str(df["recorded"][i])[0:4]) < 2000:
                df.loc[i, "recorded"] = None
        except ValueError:
            df.loc[i, "recorded"] = None

def selectDateTime(df, dateTimeCol='DateTime', recordedCol='recorded', modifiedCol='modified', creationCol='creation', newCol='filtered') -> None:
    if dateTimeCol not in df.columns:
        dateTimeCol = 'creation'

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

            if recordedVal:
                if dateTimeVal:
                    if dateTimeVal < recordedVal:
                        filtered.append(row[dateTimeCol])
                    elif dateTimeVal > recordedVal:
                        filtered.append(row[recordedCol])
                else:
                    filtered.append(row[recordedCol])
            elif modifiedVal and creationVal:
                if modifiedVal <= creationVal:
                    filtered.append(row[modifiedCol])
                else:
                    filtered.append(row[creationCol])
            elif modifiedVal:
                filtered.append(row[creationCol])


            else:
                filtered.append(row[creationCol])

        except ValueError:
            filtered.append(None)

    df.insert(6, newCol, filtered)

    df["indicated"] = df["filtered"].astype(str).str.replace(":", "", regex=False).str.replace(" ", "_", regex=False)

    return df