import pandas as pd

def filterDateTime(df, dateTimeCol='DateTime', recordedCol='recorded', modifiedCol='modified', creationCol='creation', newCol='filtered'):

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
            elif recordedVal and modifiedVal and recordedVal < modifiedVal:
                filtered.append(row[recordedCol])
            elif modifiedVal and creationVal and modifiedVal < creationVal:
                filtered.append(row[modifiedCol])
            else:
                filtered.append(row[creationCol])
        except ValueError:
            filtered.append(None)

    df.insert(7, newCol, filtered)
    return df