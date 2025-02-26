import pandas as pd
import PIL

from metaDataList import getDataDictionaryList

if __name__ == "__main__":
    PIL.Image.MAX_IMAGE_PIXELS = None   # To avoid the decompression bomb error 
    supportedTypes: list[tuple] = [(".jpg", ".jpeg", ".png"), (".mp4", ".mov")]

    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")

    # Get the metadata list
    metaDataList: list[dict] = getDataDictionaryList(sourceFolder, supportedTypes)

    # Create a dataframe with the metadata
    df: pd.DataFrame = pd.DataFrame(metaDataList)

    # Save the dataframe to a csv file
    df.to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")