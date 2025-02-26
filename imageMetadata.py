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
            fileApp: str = "WhatsApp"
        else:
            fileApp: None = None
    elif file.startswith(("Screenshot", "SVID")):
        fileStripped: str = file[10:].lstrip("-_")
        fileApp: str = file[27:].rsplit(".", 1)[0]
    else:
        fileStripped: str = file
        fileApp: None = None
    return fileStripped, fileApp
    
# Get the recorded time of the file
def getRecordedTime(fileStripped: str) -> str:
    try:
        fileRecorded: str = parse(timestr = fileStripped, yearfirst = True, fuzzy = True).strftime('%Y:%m:%d %H:%M:%S')
    except:
        fileRecorded: None = None
    return fileRecorded

# Get the creation and modified time of the file
def getCreationModifiedTime(path: str) -> tuple[str, str]:
    fileCreation: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(os.path.getctime(path)))
    fileModified: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(os.path.getmtime(path)))

    return fileCreation, fileModified

# Get the exif data of the file
## Only for image files
def getExifData_ForDictionary(path: str, metaDataDictionary: dict) -> dict[str: str]:
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
        metaDataDictionary[imageTag] = mediaMetaData
    return metaDataDictionary

def getRegularData_ForDictionary(roots: str, file: str) -> tuple[str, dict[str: str]]:
    # Get the path of the file
    path: str = str(roots + "\\" + file)
    # Print the path of the file
    print(f"Retrieving metadata for file: {path}")

    # Get the regular meta data of the file
    fileStripped, fileApp = getFileStripped(file)
    fileRecorded = getRecordedTime(fileStripped)
    fileCreation, fileModified = getCreationModifiedTime(path)

    # Create a dictionary with the meta data
    metaDataDictionary: dict[str : str] = {"path": path,
                                        "root": roots,
                                        "file": file,
                                        "folder": os.path.basename(roots),
                                        "type": os.path.splitext(file)[1],
                                        "filesize": os.path.getsize(path),
                                        "creation": fileCreation,
                                        "modified": fileModified,
                                        "recorded": fileRecorded,
                                        "app": fileApp}
    
    return path, metaDataDictionary

# Get the meta data of the files in the folder
def getDataDictionaryList(sourceFolder: str, supportedTypes: list[tuple]) -> list[dict]:

    metaDataDictionaryList: list = []

    for roots, _, files in os.walk(sourceFolder):
            print(f"\nRetrieving metadata for files in folder: {roots}\n")

            for file in files:
                if file.lower().endswith(supportedTypes[0]) == True: # For image files
                    ## Get the regular meta data of the file
                    path, metaDataDictionary = getRegularData_ForDictionary(roots, file)

                    ## Get the exif data of the file and add it to the dictionary
                    metaDataDictionary: dict[str : str] = getExifData_ForDictionary(path, metaDataDictionary)

                    ## Append the dictionary to the list
                    metaDataDictionaryList.append(metaDataDictionary)

                elif file.lower().endswith(supportedTypes[1]) == True: # For video files

                    ## Get the regular meta data of the file
                    _, metaDataDictionary = getRegularData_ForDictionary(roots, file)

                    ## Append the dictionary to the list
                    metaDataDictionaryList.append(metaDataDictionary)
                                               
                else: # For other files
                     print(f"Cannot access metadata for file: {file} - moving on...")

    return metaDataDictionaryList

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
