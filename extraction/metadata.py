import os
from PIL import Image, ExifTags
import re
from datetime import datetime

#### REGULAR DATA ####
"""
This module extracts regular metadata from image and video files. Regular metadata
includes the file path, file name, folder name, file type, file size, creation time,
and modified time. Creation and modified times are formatted as 'YYYYMMDD_HHMMSS' strings.
This module does not process files without regular metadata, like text files.
"""

NON_NUMERIC_PATTERN = re.compile(r"[^0-9]")

def processString(inputString: str | None) -> str:
    if inputString is None:
        return ""

    numericalString = NON_NUMERIC_PATTERN.sub("", str(inputString))
    truncatedString = numericalString[:14]
    currentLength = len(truncatedString)

    if currentLength < 8:
        return ""
    elif currentLength == 8:
        return truncatedString
    elif currentLength in [9, 10, 11, 13]:
        return truncatedString[:8]
    else:
        return f"{truncatedString[:8]}_{truncatedString[8:]}"


def getCreationModifiedTime(filePath: str) -> tuple[str, str, str]:
    try:
        creationTimestamp = os.path.getctime(filePath)
        modifiedTimestamp = os.path.getmtime(filePath)

        fileCreation = datetime.fromtimestamp(creationTimestamp).strftime("%Y%m%d_%H%M%S")
        fileModified = datetime.fromtimestamp(modifiedTimestamp).strftime("%Y%m%d_%H%M%S")
    except OSError:
        fileCreation = ""
        fileModified = ""

    fileRecorded = processString(os.path.basename(filePath))

    return fileCreation, fileModified, fileRecorded

def getRegularData(rootDirectory: str, fileName: str) -> tuple[str, dict[str, str | int | None]]:
    fullPath = os.path.join(rootDirectory, fileName)
    print(f"Retrieving metadata for file: {fullPath}")

    fileCreation, fileModified, fileRecorded = getCreationModifiedTime(fullPath)

    metaDataDictionary: dict[str, str | int | None] = {
        "path": fullPath,
        "file": fileName,
        "folder": os.path.basename(rootDirectory),
        "type": os.path.splitext(fileName)[1].lower(),
        "fileSize": os.path.getsize(fullPath) if os.path.exists(fullPath) else 0,
        "creation": fileCreation,
        "modified": fileModified,
        "recorded": fileRecorded,
        "indicated": None,
    }
    return fullPath, metaDataDictionary



#### EXIF DATA ####
"""
This module extracts EXIF data from image files using the PIL library. The EXIF data
is added to an existing metadata dictionary with human-readable tag names. This module
is specifically for image files with EXIF data (e.g., JPEG, PNG) and will not add
EXIF data if it's a video file or no EXIF data is present.
"""

def getExifData(filePath: str, metaDataDictionary: dict) -> dict[str, str | int | bytes | None]:
    try:
        with Image.open(filePath) as imageData:
            imageExifData = imageData.getexif()

            if imageExifData:
                for imageTagId, mediaMetaData in imageExifData.items():
                    imageTag = ExifTags.TAGS.get(imageTagId, imageTagId)

                    if isinstance(mediaMetaData, bytes):
                        try:
                            # Try decoding with UTF-8 first (most common)
                            mediaMetaData = mediaMetaData.decode("utf-8")
                        except UnicodeDecodeError:
                            try:
                                # Fallback to latin-1, common for EXIF text fields
                                mediaMetaData = mediaMetaData.decode("latin-1")
                            except UnicodeDecodeError:
                                # If even latin-1 fails, log and set to None
                                # This is the only UnicodeDecodeError warning we keep.
                                print(f"Warning: EXIF tag '{imageTag}' for '{filePath}' bytes could not be decoded (utf-8 & latin-1 failed). Setting to None.")
                                mediaMetaData = None
                            except Exception as e:
                                # Catch any other general exception for latin-1 decoding
                                print(f"Warning: Unexpected error during latin-1 decoding for EXIF tag '{imageTag}' in '{filePath}': {e}. Setting to None.")
                                mediaMetaData = None
                        except Exception as e:
                            # Catch any other general exception for utf-8 decoding
                            print(f"Warning: Unexpected error during utf-8 decoding for EXIF tag '{imageTag}' in '{filePath}': {e}. Setting to None.")
                            mediaMetaData = None

                    metaDataDictionary[imageTag] = mediaMetaData
    except Exception as e:
        print(f"Warning: Could not extract EXIF data from {filePath}: {e}")
    return metaDataDictionary



#### LIST OF METADATA DICTIONARIES ####
"""
This module compiles a list of dictionaries, each containing the metadata for a file
within a specified folder and its subfolders. It uses `os.walk` and the `getRegularData`
and `getExifData` functions. Supported file types are defined by a list of tuples
(e.g., image and video extensions). The resulting list of dictionaries can be
used for further data processing.
"""

def getDataDictionaryList(sourceFolder: str, supportedTypes: list[tuple[str, ...]]) -> list[dict]:
    """
    Collects metadata for all supported media files within a given source folder.

    Args:
        sourceFolder (str): The path to the root folder to scan.
        supportedTypes (list[tuple]): A list where each tuple contains file extensions
                                       for a specific media type (e.g., image, video).

    Returns:
        list[dict]: A list of dictionaries, each containing the metadata for a file.
    """
    metaDataDictionaryList: list[dict] = []

    imageExtensions = supportedTypes[0]
    videoExtensions = supportedTypes[1]

    for root, _, files in os.walk(sourceFolder):
        if files:
            print(f"\nProcessing files in folder: {root}\n")

        for fileName in files:
            # Get extension once
            _, fileExtension = os.path.splitext(fileName)
            fileExtensionLower = fileExtension.lower()

            # Call getRegularData once, as it's common for both
            # fullPath is retrieved here and can be used for getExifData
            fullPath, metaDataDict = getRegularData(root, fileName)

            if fileExtensionLower in imageExtensions:
                # Removed redundant os.path.exists check, rely on getExifData's error handling
                metaDataDict = getExifData(fullPath, metaDataDict)
                metaDataDictionaryList.append(metaDataDict)
            elif fileExtensionLower in videoExtensions:
                metaDataDictionaryList.append(metaDataDict)
            else:
                print(f"Skipping unsupported file: {fileName}")

    return metaDataDictionaryList