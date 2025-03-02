import pandas as pd
import PIL

from extraction.metaDataList import getDataDictionaryList

def extractData(sourceFolder, maxImagePixels = None, supportedTypes = [(".jpg", ".jpeg", ".png"), (".mp4", ".mpg", ".mov")]) -> None:
    PIL.Image.MAX_IMAGE_PIXELS = maxImagePixels   # To avoid the decompression bomb error

    # Get the metadata list
    metaDataList: list[dict] = getDataDictionaryList(sourceFolder, supportedTypes)

    # Create a dataframe with the meta data and save it as a csv file
    pd.DataFrame(metaDataList).to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")

if __name__ == "__main__":
    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")
    extractData(sourceFolder)