from PIL import Image, ExifTags

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