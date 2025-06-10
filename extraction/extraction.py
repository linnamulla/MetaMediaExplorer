import pandas as pd
import PIL; from PIL import Image

#### DATA EXTRACTION ####
## This module is used to extract data from image and video files in a specified folder. It retrieves metadata from exif data for images and regular metadata for both images and videos. The supported file types are specified as a list of tuples, where each tuple contains the file extensions for image and video files respectively. The function `extractData` takes a source folder path and an optional maximum image pixel limit to avoid decompression bomb errors. It retrieves the metadata for all files in the folder and its subfolders, and saves the extracted data as a CSV file in the source folder.

def extractData(sourceFolder, maxImagePixels = None, supportedTypes = [(".gif", ".jpg", ".jpeg", ".png"), (".mov", ".mp4", ".mpg", ".mts")]) -> None:

    # Set the maximum image pixels to avoid decompression bomb errors
    PIL.Image.MAX_IMAGE_PIXELS = maxImagePixels

    # Get the list of metadata dictionaries for all files in the source folder
    from extraction.metadata.dictionaries import getDataDictionaryList
    ## This function retrieves exif and regular metadata from image and video files in the specified folder and its subfolders.
    metadataList: list[dict] = getDataDictionaryList(sourceFolder, supportedTypes)

    # Create a dataframe from the list of dictionaries and save it as a CSV file
    pd.DataFrame(metadataList).to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")

#### ####