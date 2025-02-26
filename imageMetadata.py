from dateutil.parser import *
import os
import pandas as pd
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import time

# Get the stripped file name and app specification
def getFileStripped(file: str) -> tuple[str, str]:
    if file.startswith(("IMG", "VID")):
        fileStripped: str = file[3:].lstrip("-_")
        if "WA" in file:
            fileStripped: str = file.split("WA")[0].rstrip("-_ ")
            appSpecification: str = "WhatsApp"
        else:
            appSpecification: None = None
    elif file.startswith(("Screenshot", "SVID")):
        fileStripped: str = file[10:].lstrip("-_")
        appSpecification: str = file[27:].rsplit(".", 1)[0]
    else:
        fileStripped: str = file
        appSpecification: None = None
    return fileStripped, appSpecification
    
# Get the recorded time of the image
def getRecordedTime(fileStripped: str) -> str:
    try:
        imageRecordedTime: str = parse(timestr = fileStripped, yearfirst = True, fuzzy = True).strftime('%Y:%m:%d %H:%M:%S')
    except:
        imageRecordedTime: None = None
    return imageRecordedTime

# Get the creation and modified time of the image
def getTime(path: str) -> tuple[str, str]:
    ## Get the creation time of the image
    imageCreationEpoch: float = os.path.getctime(path)
    imageCreationTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageCreationEpoch))
    ## Get the modified time of the image
    imageModifiedEpoch: float = os.path.getmtime(path)
    imageModifiedTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageModifiedEpoch))
    ## Return the creation and modified time
    return imageCreationTime, imageModifiedTime

# Get the exif data of the image
def getExifData_ForDictionary(path: str, imageDictionary: dict) -> dict[str: str]:
    imageData: Image = Image.open(path)
    imageExifData: object = imageData.getexif()
    for imageTagId in imageExifData:
        imageTag: str = TAGS.get(imageTagId, imageTagId)
        mediaMetaData: str = imageExifData.get(imageTagId)
        if isinstance(mediaMetaData, bytes):
            try:
                mediaMetaData: str = mediaMetaData.decode()
            except:
                mediaMetaData = None
        imageDictionary[imageTag] = mediaMetaData
    return imageDictionary

def getRegularData_ForDictionary(roots: str, file: str) -> tuple[str, dict[str: str]]:
    # Get the path of the file
    path: str = str(roots + "\\" + file)
    # Print the path of the file
    print(f"Retrieving metadata for file: {path}")

    # Get the regular meta data of the image
    fileStripped, appSpecification = getFileStripped(file)
    imageRecordedTime = getRecordedTime(fileStripped)
    imageCreationTime, imageModifiedTime = getTime(path)

    # Create a dictionary with the meta data
    imageDictionary: dict[str : str] = {"path": path,
                                        "root": roots,
                                        "file": file,
                                        "folder": os.path.basename(roots),
                                        "type": os.path.splitext(file)[1],
                                        "filesize": os.path.getsize(path),
                                        "creation": imageCreationTime,
                                        "modified": imageModifiedTime,
                                        "recorded": imageRecordedTime,
                                        "app": appSpecification}
    
    return path, imageDictionary

# Get the metadata of the images in the folder
def getDataDictionaryList(sourceFolder: str, supportedTypes: list[tuple]) -> list[dict]:

    imageDictionaryList: list = []

    for roots, _, files in os.walk(sourceFolder):
            print(f"\nRetrieving metadata for files in folder: {roots}\n")

            for file in files:
                if file.lower().endswith(supportedTypes[0]) == True: # For image files
                    ## Get the regular meta data of the image
                    path, imageDictionary = getRegularData_ForDictionary(roots, file)

                    ## Get the exif data of the image and add it to the dictionary
                    imageDictionary: dict[str : str] = getExifData_ForDictionary(path, imageDictionary)

                    ## Append the dictionary to the list
                    imageDictionaryList.append(imageDictionary)

                elif file.lower().endswith(supportedTypes[1]) == True: # For video files

                    ## Get the regular meta data of the image
                    _, imageDictionary = getRegularData_ForDictionary(roots, file)

                    ## Append the dictionary to the list
                    imageDictionaryList.append(imageDictionary)
                                               
                else: # For other files
                     print(f"Cannot access metadata for file: {file} - moving on...")

    return imageDictionaryList

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
