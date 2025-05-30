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

def selectDateTime(df, dateTimeCol='DateTime', recordedCol='recorded', modifiedCol='modified', creationCol='creation', newCol='filtered') -> pd.DataFrame:

    filtered = []
    for index, row in df.iterrows():
        try:
            dateTimeVal = row[dateTimeCol] if pd.notna(row[dateTimeCol]) else None
            recordedVal = row[recordedCol] if pd.notna(row[recordedCol]) else None
            modifiedVal = row[modifiedCol] if pd.notna(row[modifiedCol]) else None
            creationVal = row[creationCol] if pd.notna(row[creationCol]) else None

            if recordedVal is not None:
                if dateTimeVal is not None:
                    if str(dateTimeVal).replace(": ", "") < str(recordedVal).replace(": ", ""):
                        filtered.append(dateTimeVal)
                    else:
                        filtered.append(recordedVal)
                else:
                    filtered.append(recordedVal)
            elif modifiedVal is not None and creationVal is not None:
                if str(modifiedVal).replace(": ", "") <= str(creationVal).replace(": ", ""):
                    filtered.append(modifiedVal)
                else:
                    filtered.append(creationVal)
            elif modifiedVal is not None:
                filtered.append(modifiedVal)
            elif creationVal is not None:
                filtered.append(creationVal)
            else:
                filtered.append(None)
        except (ValueError, TypeError):
            print(f"ValueError or TypeError occurred at index {index}")
            filtered.append(None)

    df.insert(6, newCol, filtered)
    df["indicated"] = df["filtered"].astype(str).str.replace(":", "", regex=False).str.replace(" ", "_", regex=False)
    return df