import os

from extraction.metadata.filedata import getRegularData
from extraction.metadata.exifdata import getExifData

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