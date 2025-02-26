from dateutil.parser import *
import os
import pandas as pd
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import time

PIL.Image.MAX_IMAGE_PIXELS = 10 ** 20

def getMetadataList(sourceFolder: str) -> list[dict]:
    imageDictionaryList: list = []
    for roots, _, files in os.walk(sourceFolder):
            print(f"\nRetrieving metadata for files in folder: {roots}\n")
            for file in files:
                if file.endswith((".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG")) == True:
                    fileName: str = str(roots + "\\" + file)
                    print(f"Retrieving metadata for file: {fileName}")

                    imageDictionary: dict = {}

                    imageDictionary["file"] = file
                    imageDictionary["folder"] = os.path.basename(roots)
                    imageDictionary["path"] = roots
                    _, imageDictionary["type"] = os.path.splitext(file)

                    imageCreationEpoch: float = os.path.getctime(fileName)
                    imageCreationTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageCreationEpoch))
                    imageDictionary["creation"] = imageCreationTime

                    imageModifiedEpoch: float = os.path.getmtime(fileName)
                    imageModifiedTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageModifiedEpoch))
                    imageDictionary["modified"] = imageModifiedTime

                    if file.startswith("IMG"):
                        strippedFile: str = file[3:].lstrip("-_")
                        if "WA" in file:
                            strippedFile: str = file.split("WA")[0].rstrip("-_ ")
                        appSpecification: None = None
                    elif file.startswith("Screenshot"):
                            strippedFile: str = file[10:].lstrip("-_")
                            appSpecification: str = file[27:].rsplit(".", 1)[0]
                        
                    else:
                        strippedFile: str = file
                        appSpecification: None = None

                    try:
                        imageRecordedTime: str = parse(strippedFile, yearfirst = True, fuzzy = True).strftime('%Y:%m:%d %H:%M:%S')
                        imageDictionary["recorded"] = imageRecordedTime
                    except:
                        pass

                    imageDictionary["app"] = appSpecification

                    imageFilesize: int = os.path.getsize(fileName)
                    imageDictionary["filesize"] = imageFilesize

                    imageData: Image = Image.open(fileName)
                    imageExifData: object = imageData.getexif()

                    for imageTagId in imageExifData:
                        imageTag: str = TAGS.get(imageTagId, imageTagId)
                        imageMetadata: str = imageExifData.get(imageTagId)
                        if isinstance(imageMetadata, bytes):
                            try:
                                imageMetadata: str = imageMetadata.decode()
                            except:
                                imageMetadata: None = None
                        imageDictionary[imageTag] = imageMetadata
                    
                    imageDictionaryList.append(imageDictionary)
                elif file.endswith((".mp4", ".MP4", ".mov", ".MOV")) == True: 
                    fileName: str = str(roots + "\\" + file)
                    print(f"Retrieving metadata for file: {fileName}")

                    imageDictionary: dict = {}

                    imageDictionary["file"] = file
                    imageDictionary["folder"] = os.path.basename(roots)
                    imageDictionary["path"] = roots
                    _, imageDictionary["type"] = os.path.splitext(file)

                    imageCreationEpoch: float = os.path.getctime(fileName)
                    imageCreationTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageCreationEpoch))
                    imageDictionary["creation"] = imageCreationTime

                    imageModifiedEpoch: float = os.path.getmtime(fileName)
                    imageModifiedTime: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(imageModifiedEpoch))
                    imageDictionary["modified"] = imageModifiedTime

                    if file.startswith(("VID", "WIN")):
                        strippedFile: str = file[3:].lstrip("-_")
                        if "WA" in file:
                            strippedFile: str = file.split("WA")[0].rstrip("-_ ")
                        appSpecification: None = None
                    elif file.startswith("SVID"):
                            strippedFile: str = file[10:].lstrip("-_")
                            appSpecification: str = file[27:].rsplit(".", 1)[0]
                        
                    else:
                        strippedFile: str = file
                        appSpecification: None = None

                    try:
                        imageRecordedTime: str = parse(strippedFile, yearfirst = True, fuzzy = True).strftime('%Y:%m:%d %H:%M:%S')
                        imageDictionary["recorded"] = imageRecordedTime
                    except:
                        pass

                    imageDictionary["app"] = appSpecification

                    imageFilesize: int = os.path.getsize(fileName)
                    imageDictionary["filesize"] = imageFilesize

                    imageDictionaryList.append(imageDictionary)
                else:
                     print(f"Cannot access metadata for {file}, moving on...")

    return imageDictionaryList

if __name__ == "__main__":
    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")
    metaDataList: list[dict] = getMetadataList(sourceFolder)
    df: pd.DataFrame = pd.DataFrame(metaDataList)
    df.to_csv(path_or_buf = (sourceFolder + "\\.imageMetadata.csv"), sep = ";")
