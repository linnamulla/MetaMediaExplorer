import pandas as pd

def select_date_time(df, datetime_col='DateTime', recorded_col='recorded', modified_col='modified', creation_col='creation', new_col='selected_date'):

    selected_dates = []
    for index, row in df.iterrows():
        try:
            datetime_val = int(str(row[datetime_col])[:4]) if pd.notna(row[datetime_col]) else None
            recorded_val = int(str(row[recorded_col])[:4]) if pd.notna(row[recorded_col]) else None
            modified_val = int(str(row[modified_col])[:4]) if pd.notna(row[modified_col]) else None
            creation_val = int(str(row[creation_col])[:4]) if pd.notna(row[creation_col]) else None

            if datetime_val:
                selected_dates.append(row[datetime_col])
            elif recorded_val and modified_val and recorded_val < modified_val:
                selected_dates.append(row[recorded_col])
            elif modified_val and creation_val and modified_val < creation_val:
                selected_dates.append(row[modified_col])
            else:
                selected_dates.append(row[creation_col])
        except ValueError:
            selected_dates.append(None)

    df.insert(7, new_col, selected_dates)
    return df