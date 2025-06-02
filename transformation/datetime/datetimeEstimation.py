import pandas as pd
import re

def estimateStamp(sourceFolder: str) -> None:
    df: pd.DataFrame = pd.read_csv(sourceFolder + "\\.mediaMetaData.csv", sep = ";")
    def processString(inputString):
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
            finalString = ""
        elif currentLength == 8:
            # If exactly 8 characters, don't add any spaces
            finalString = truncatedString
        elif currentLength in [9, 10, 11, 13]:
            # If 9, 10, 11, or 13 characters, remove everything after the 8th character
            finalString = truncatedString[:8]
        else:  # This covers lengths 12 and 14 due to earlier truncation
            # Otherwise, add an underscore after the 8th character
            finalString = truncatedString[:8] + "_" + truncatedString[8:]

        return finalString

    df["recorded"] = df["file"].apply(processString)
    print(df)
    pd.DataFrame(df).to_csv(path_or_buf = (sourceFolder + "\\.mediaMetaData.csv"), sep = ";")

    return None