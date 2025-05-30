from dateutil.parser import *
import os
import time

# Get the stripped file name and app name from the file name
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
    
# Get the recorded time of the file
def getRecordedTime(fileStripped: str) -> str:
    try:
        fileRecorded: str = parse(timestr = fileStripped, yearfirst = True, fuzzy = True).strftime('%Y:%m:%d %H:%M:%S')
    except:
        fileRecorded: str = None
    return fileRecorded

# Get the creation and modified time of the file
def getCreationModifiedTime(path: str) -> tuple[str, str]:
    fileCreation: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(os.path.getctime(path)))
    fileModified: str = time.strftime('%Y:%m:%d %H:%M:%S', time.gmtime(os.path.getmtime(path)))

    return fileCreation, fileModified

# Get the regular meta data of the file
## For image and video files
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
                                           "file": file,
                                           "fileStripped": fileStripped,
                                           "folder": os.path.basename(roots),
                                           "type": os.path.splitext(file)[1],
                                           "filesize": os.path.getsize(path),
                                           "creation": fileCreation,
                                           "modified": fileModified,
                                           "recorded": fileRecorded,
                                           "app": fileApp}
    
    return path, metaDataDictionary