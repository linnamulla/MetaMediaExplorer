import pandas as pd
import PIL

from extraction.dictionarylist.metaData import getDataDictionaryList

def extractData(sourceFolder, maxImagePixels = None, supportedTypes = [(".gif", ".jpg", ".jpeg", ".png"), (".mov", ".mp4", ".mpg", ".mts")]) -> None:
    PIL.Image.MAX_IMAGE_PIXELS = maxImagePixels   # To avoid the decompression bomb error

    # Get the metadata list
    metaDataList: list[dict] = getDataDictionaryList(sourceFolder, supportedTypes)

    # Create a dataframe with the meta data and save it as a csv file
    pd.DataFrame(metaDataList).to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")