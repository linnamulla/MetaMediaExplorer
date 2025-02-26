from dateutil.parser import *
import os
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