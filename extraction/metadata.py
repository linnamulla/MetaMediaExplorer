from dateutil.parser import *
import os
from PIL import Image
from PIL.ExifTags import TAGS
import re
import time

#### REGULAR DATA ####
## This module is used to extract the regular meta data from both image and video files. Regular meta data includes the file path, file name, folder name, file type, file size, creation time, modified time, and app name. The app name is determined based on the file name prefix and is stored in the metadata dictionary. The creation and modified times are formatted as strings in the 'YYYYMMDD_HHMMSS' format. This module does not work for files that do not have regular meta data, such as text files or other types of files. 

## This function is used to get the app name from the file name and strip the file name of any prefixes or suffixes that are not needed. It returns a tuple containing the stripped file name and the app name.
def getFileStripped(file: str) -> tuple[str, str]:
    if file.startswith(("IMG", "VID")):
        fileStripped: str = file[3:].lstrip("-_")
        if "WA" in file:
            fileStripped: str = file.split("WA")[0].rstrip("-_ ")
            fileApp: str = "WhatsApp" # Get the app name from the file name
        else:
            fileApp: str = None
    elif file.startswith(("Screenshot", "SVID")):
        fileStripped: str = file[10:].lstrip("-_")
        fileApp: str = file[27:].rsplit(".", 1)[0] # Get the app name from the file name
    else:
        fileStripped: str = file # No stripping needed
        fileApp: str = None # No app name in the file name
        
    return fileStripped, fileApp

## This function is used to process a string according to specific rules. The result is a string that is formatted based on the length of the input string after removing non-numerical characters and truncating it to 14 characters. The function applies the following rules:
def processString(inputString: str) -> str:
        """
        Reads a string, removes all non-numerical characters,
        cuts off everything after the 14th character.
        Then, applies conditional formatting based on the resulting length:
        - If less than 8 characters, the result is empty.
        - If exactly 8 characters, no spaces are added.
        - If 9, 10, 11, or 13 characters, everything after the 8th character is removed.
        - Otherwise (12 or 14 characters), a space is added after the 8th character.

        Args:
            inputString (str): The string to be processed.

        Returns:
            str: The processed string according to the new rules.
        """
        # Ensure input is treated as a string, especially if it might be a non-string type like None or NaN
        if not isinstance(inputString, str):
            inputString = str(inputString)

        # Step 1: Remove all non-numerical characters
        numericalString = re.sub(r"[^0-9]", "", inputString)

        # Step 2: Cut off everything after the 14th character
        truncatedString = numericalString[:14]

        finalString = ""
        currentLength = len(truncatedString)

        # Step 3: Apply new conditional checks based on length
        if currentLength < 8:
            # If less than 8 characters, make the result empty
            finalString = "19700101_000000"  # Default value for empty strings
        elif currentLength == 8:
            # If exactly 8 characters, don't add any spaces
            finalString = truncatedString
        elif currentLength in [9, 10, 11, 13]:
            # If 9, 10, 11, or 13 characters, remove everything after the 8th character
            finalString = truncatedString[:8]
        else:  # This covers lengths 12 and 14 due to earlier truncation
            # Otherwise, add an underscore after the 8th character
            finalString = truncatedString[:8] + "_" + truncatedString[8:]

        print(f"Processed string: {finalString} from input: {inputString}")
        return finalString

## This function is used to get the creation and modified time of the file. It returns a tuple containing the creation time and modified time as strings in the 'YYYYMMDD_HHMMSS' format.
def getCreationModifiedTime(path: str) -> tuple[str, str]:
    fileCreation: str = time.strftime('%Y%m%d_%H%M%S', time.gmtime(os.path.getctime(path)))
    fileModified: str = time.strftime('%Y%m%d_%H%M%S', time.gmtime(os.path.getmtime(path)))
    fileRecorded: str = processString(os.path.basename(path))
    print(fileRecorded, "is the recorded time of the file.")

    return fileCreation, fileModified, fileRecorded

## This function is the main function of this module. It retrieves the regular meta data of a file, including the file path, file name, folder name, file type, file size, creation time, modified time, and app name. It returns a tuple containing the file path and a dictionary with the meta data.
def getRegularData(roots: str, file: str) -> tuple[str, dict[str: str]]:
    # Get the path of the file
    path: str = str(roots + "\\" + file)
    # Print the path of the file
    print(f"Retrieving metadata for file: {path}")

    # Get the creation and modified time of the file
    fileCreation, fileModified, fileRecorded = getCreationModifiedTime(path)
    # Get the app name from the file name
    _, fileApp = getFileStripped(file)
    
    # Create a dictionary with the regular metadata
    metaDataDictionary: dict[str : str] = {"path": path,
                                           "file": file,
                                           "folder": os.path.basename(roots),
                                           "type": os.path.splitext(file)[1],
                                           "filesize": os.path.getsize(path),
                                           "creation": fileCreation,
                                           "modified": fileModified,
                                           "recorded": fileRecorded,
                                           "indicated": None,  # This will be set later in the transformation module
                                           "app": fileApp}
    return path, metaDataDictionary

#### ####



#### EXIF DATA ####
## This module is used to extract the exif data from image files. It uses the PIL library to open the image file and get the exif data. The exif data is then stored in a dictionary with the exif tag names as keys and the file's metadata as values. This dictionary is previously created in the getRegularData function. The exif tag names are obtained from the PIL ExifTags module, which provides a mapping of exif tag IDs to human-readable names. The tag names are obtained from the PIL ExifTags module. This module only works for image files that have exif data, such as JPEG and PNG files. It does not work for video files or other types of files. If the file does not have exif data, the function will not add any exif data to the metadata dictionary. 

def getExifData(path: str, metaDataDictionary: dict) -> dict[str: str]:
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

#### ####



#### LIST OF METADATA DICTIONARIES ####
## This module is used to get a list of dictionaries containing the meta data of all files in a folder. It uses the os module to walk through the folder and its subfolders, and the getRegularData and getExifData functions to retrieve the regular and exif meta data of each file. The supported file types are specified as a list of tuples, where each tuple contains the file extension for image and video files respectively. The function returns a list of dictionaries containing the meta data of all files in the folder. This list of dictionaries can be used for further processing, such as filtering, sorting, or exporting to a CSV file, by making use of the pandas library.

def getDataDictionaryList(sourceFolder: str, supportedTypes: list[tuple]) -> list[dict]:
    print("INDICATED START OF MODULE METADATA")

    # Create an empty list to store the metadata dictionaries
    metaDataDictionaryList: list = []

    # Run through the source folder and its subfolders, and retrieve the metadata for each file
    for roots, _, files in os.walk(sourceFolder):
            print(f"\nRetrieving metadata for files in folder: {roots}\n")

            for file in files:
                if file.lower().endswith(supportedTypes[0]) == True: # For image files

                    ## Get the regular meta data of the file
                    path, metaDataDictionary = getRegularData(roots, file)
                    ## Get the exif data of the file and add it to the dictionary
                    metaDataDictionary: dict[str : str] = getExifData(path, metaDataDictionary)
                    ## Append the dictionary to the list
                    metaDataDictionaryList.append(metaDataDictionary)

                elif file.lower().endswith(supportedTypes[1]) == True: # For video files

                    ## Get the regular meta data of the file
                    _, metaDataDictionary = getRegularData(roots, file)
                    ## Append the dictionary to the list
                    metaDataDictionaryList.append(metaDataDictionary)
                                               
                else: # For other files
                     
                     print(f"Cannot access metadata for file: {file} - moving on...")

    # Return the list of metadata dictionaries

    print("INDICATED END OF MODULE METADATA")
    return metaDataDictionaryList

#### ####