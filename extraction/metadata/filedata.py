import os
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
    elif currentLength in [9, 10, 11, 12, 13]:
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