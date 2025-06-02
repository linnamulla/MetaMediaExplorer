import os

from extraction.dataextraction.exifData import getExifData_ForDictionary
from extraction.dataextraction.fileData import getRegularData_ForDictionary

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
