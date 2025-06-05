from datetime import datetime
import pandas as pd

def filterDateTime(df: pd.DataFrame) -> pd.DataFrame:
    ## Clean values in the recorded column
    for i in range(len(df["recorded"])):
        try:
            if int(str(df["recorded"][i])[0:4]) > datetime.now().year or int(str(df["recorded"][i])[0:4]) < 2000:
                df.loc[i, "recorded"] = None
        except ValueError:
            df.loc[i, "recorded"] = None

def selectDateTime(df, dateTimeCol='DateTime', recordedCol='recorded', modifiedCol='modified', creationCol='creation', newCol='filtered') -> pd.DataFrame:
    if dateTimeCol not in df.columns:
        dateTimeCol = 'creation'

    print(f"INDICATED START OF MODULE DATETIMEFILTER with dateTimeCol: {dateTimeCol}, recordedCol: {recordedCol}, modifiedCol: {modifiedCol}, creationCol: {creationCol}, newCol: {newCol}")

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