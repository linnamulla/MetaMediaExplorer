from datetime import datetime
import pandas as pd
import numpy as np # Import numpy for np.nan

def filterDateTime(df: pd.DataFrame) -> None:
    """
    Cleans the 'recorded' column by setting values to None if their year
    is outside the 2000-current_year range or if the year cannot be parsed.

    Args:
        df (pd.DataFrame): The input DataFrame. Modified in place.
    """
    # Ensure 'recorded' column is string type for consistent slicing.
    # Convert existing None/NaN to string 'None'/'nan' for `astype(str)`.
    # This ensures that subsequent `.str[:4]` operations don't fail for non-string types.
    df["recorded"] = df["recorded"].astype(str)

    # Attempt to extract the first 4 characters and convert to numeric year.
    # `errors="coerce"` will turn any unparseable strings (like "None", "nan", or shorter strings) into NaN.
    yearsExtracted: int = pd.to_numeric(df["recorded"].str[:4], errors="coerce")
    # Get the current year for comparison.
    currentYear: int = datetime.now().year

    # Create a boolean mask for values that should be set to None:
    # 1. Where year extraction resulted in NaN (meaning invalid format/missing).
    # 2. Where the extracted year is outside the valid range ( > currentYear or < 2000).
    maskToNull: bool = yearsExtracted.isna() | ((yearsExtracted > currentYear) | (yearsExtracted < 2000))

    # Apply the mask to set the 'recorded' column values to None where conditions are met.
    # Using `None` will allow Pandas to represent missing values as `NaN` where appropriate,
    # and simplifies `pd.notna()` checks later.
    df.loc[maskToNull, "recorded"] = None

    print(f"Cleaned 'recorded' column. {maskToNull.sum()} entries were set to None.")


def selectDateTime(df: pd.DataFrame, dateTimeCol: str = "DateTime", recordedCol: str = "recorded",
                   modifiedCol: str = "modified", creationCol: str = "creation", newCol: str = "filtered") -> pd.DataFrame:
    """
    Selects the most appropriate date/time value for each row based on a set of rules
    and inserts it into a new column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        dateTimeCol (str): Name of the primary date/time column. Defaults to "DateTime".
        recordedCol (str): Name of the "recorded" date/time column. Defaults to "recorded".
        modifiedCol (str): Name of the "modified" date/time column. Defaults to "modified".
        creationCol (str): Name of the "creation" date/time column. Defaults to "creation".
        newCol (str): Name of the new column to insert. Defaults to "filtered".

    Returns:
        pd.DataFrame: The DataFrame with the new "filtered" and "indicated" columns.
    """

    # If dateTimeCol doesn't exist, default to creationCol
    if dateTimeCol not in df.columns:
        dateTimeCol: str = "creation"

    def _getYearFromColumn(rowVal) -> int | None:
        """
        Safely extracts the first 4 characters from a value and converts to an integer year.
        Returns None if the value is missing, not string-like, or year conversion fails.
        """
        if pd.notna(rowVal):
            sVal = str(rowVal)
            if len(sVal) >= 4:
                try:
                    return int(sVal[:4])
                except ValueError:
                    pass # Conversion failed, fall through to return None
        return None

    def _calculateFilteredValue(row) -> str | None:
        """
        Helper function to apply row-wise. Determines the "filtered" value for a single row.
        """
        # Safely get year integers for comparison
        dtYear: int = _getYearFromColumn(row.get(dateTimeCol))
        recYear: int = _getYearFromColumn(row.get(recordedCol))
        modYear: int = _getYearFromColumn(row.get(modifiedCol))
        creYear: int = _getYearFromColumn(row.get(creationCol))

        # Retrieve original string values (not years) for the final result
        dtValStr: str = row.get(dateTimeCol)
        recValStr: str = row.get(recordedCol)
        modValStr: str = row.get(modifiedCol)
        creValStr: str = row.get(creationCol)

        # --- Decision Logic based on original code ---
        if recYear is not None:
            if dtYear is not None:
                if dtYear < recYear:
                    return dtValStr
                elif dtYear > recYear:
                    return recValStr
                else: # dtYear == recYear or other comparison not met
                    return dtValStr # Original chose dateTimeVal if years were equal
            else: # dtYear is None but recYear is not None
                return recValStr
        elif modYear is not None and creYear is not None: # recYear is None
            if modYear <= creYear:
                return modValStr
            else:
                return creValStr
        elif modYear is not None: # recYear is None, creYear might be None or invalid year
            # Original code appended creationCol here. This is a potential point of review:
            # if modifiedVal exists but creationVal doesn't (or is invalid),
            # should it return modifiedVal or creationVal? Sticking to original:
            return creValStr
        else: # recYear is None, modYear is None (and creYear implicitly might be None or handled by outer except)
            return creValStr

    # Apply the helper function row-wise to create the new "filtered" Series.
    # This automatically ensures the Series has the same length and index as the DataFrame.
    filteredSeries: pd.Series = df.apply(_calculateFilteredValue, axis=1)

    # Insert the Series into the DataFrame at the specified location.
    # The .copy() is crucial here to ensure df is not modified in-place and to return a new DataFrame.
    # If the function is meant to modify in-place and return None, remove the .copy() and the return statement.
    # Given the return type hint `-> pd.DataFrame`, it's safer to return a copy.
    df.insert(6, newCol, filteredSeries)

    # Process the new "filtered" column to create "indicated"
    # Ensure to handle potential NaNs by converting to string first.
    df["indicated"] = df[newCol].astype(str).str.replace(":", "", regex=False).str.replace(" ", "_", regex=False)

    return df