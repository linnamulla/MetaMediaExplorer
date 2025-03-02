import pandas as pd

def transformData(sourceFolder: str) -> None:
    df = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")
    print(df.head())