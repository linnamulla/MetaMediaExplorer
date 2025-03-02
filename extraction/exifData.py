from PIL import Image
from PIL.ExifTags import TAGS

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