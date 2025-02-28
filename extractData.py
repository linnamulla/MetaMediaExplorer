import pandas as pd
import PIL

from metaDataList import getDataDictionaryList

def extractData(maxImagePixels = None, supportedTypes = [(".jpg", ".jpeg", ".png"), (".mp4", ".mov")]) -> None:
    PIL.Image.MAX_IMAGE_PIXELS = maxImagePixels   # To avoid the decompression bomb error

    # Get the metadata list
    metaDataList: list[dict] = getDataDictionaryList(sourceFolder, supportedTypes)

    # Create a dataframe with the metadata
    df: pd.DataFrame = pd.DataFrame(metaDataList)

    # Save the dataframe to a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")

if __name__ == "main":
    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")
    extractData(sourceFolder)