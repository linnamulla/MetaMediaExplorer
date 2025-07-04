from datetime import datetime
import pandas as pd
import numpy as np # Import numpy for np.nan

def filterDateTime(df: pd.DataFrame, columnName: str = "recorded", yearLimit: int = 2000) -> None:
    """
    Cleans the 'recorded' column in the DataFrame by setting values to None if their year is outside a specified range
    or if the year cannot be parsed. This function modifies the DataFrame in place.

    Args:
        df (pd.DataFrame): The input DataFrame. Modified in place.
        columnName (str): The name of the column to clean. Defaults to "recorded".
    """
    # Ensure 'recorded' column is string type for consistent slicing.
    # Convert existing None/NaN to string 'None'/'nan' for `astype(str)`.
    # This ensures that subsequent `.str[:4]` operations don't fail for non-string types.
    df[columnName] = df[columnName].astype(str)

    # Attempt to extract the first 4 characters and convert to numeric year.
    # `errors="coerce"` will turn any unparseable strings (like "None", "nan", or shorter strings) into NaN.
    yearsExtracted: int = pd.to_numeric(df[columnName].str[:4], errors="coerce")
    # Get the current year for comparison.
    currentYear: int = datetime.now().year

    # Create a boolean mask for values that should be set to None:
    # 1. Where year extraction resulted in NaN (meaning invalid format/missing).
    # 2. Where the extracted year is outside the valid range ( > currentYear or < 2000).
    maskToNull: bool = yearsExtracted.isna() | ((yearsExtracted > currentYear) | (yearsExtracted < yearLimit))

    # Apply the mask to set the 'recorded' column values to None where conditions are met.
    # Using `None` will allow Pandas to represent missing values as `NaN` where appropriate,
    # and simplifies `pd.notna()` checks later.
    df.loc[maskToNull, columnName] = None

    print(f"Cleaned {columnName} column. {maskToNull.sum()} entries were set to None, because they were either invalid or outside the range {yearLimit} - {currentYear}.\n")

def selectDateTime(df: pd.DataFrame, dateTimeCol: str = "DateTime", recordedCol: str = "recorded",
                   modifiedCol: str = "modified", creationCol: str = "creation", newColumn: str = "filtered") -> pd.DataFrame:
    """
    Selects the most appropriate date/time value for each row based on a set of rules
    and inserts it into a new column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        dateTimeCol (str): Name of the primary date/time column. Defaults to "DateTime".
        recordedCol (str): Name of the "recorded" date/time column. Defaults to "recorded".
        modifiedCol (str): Name of the "modified" date/time column. Defaults to "modified".
        creationCol (str): Name of the "creation" date/time column. Defaults to "creation".
        newColumn (str): Name of the new column to insert. Defaults to "filtered".

    Returns:
        pd.DataFrame: The DataFrame with the new "filtered" and "indicated" columns.
    """

    # If dateTimeCol doesn't exist, default to creationCol
    if dateTimeCol not in df.columns:
        dateTimeCol: str = "creation"

    def _getYearFromColumn(rowVal) -> int | None:
        """
        Safely extracts the first 4 characters from a value and converts to an integer year.
        Returns None if the value is missing, not string-like, or year conversion fanewColils.
        """
        if pd.notna(rowVal):
            sVal = str(rowVal)
            if len(sVal) >= 4:
                try:
                    return int(sVal[:4])
                except ValueError:
                    pass # Conversion failed, fall through to return None
        return None

    # --- Optimized Helper Function (from our previous discussion) ---
    def get_filtered_value_lambda_optimized(recordedYear, dateTimeYear, modifiedYear, creationYear,
                                            recordedValue, dateTimeValue, modifiedValue, creationValue) -> str | None:
        """
        Determines the filtered value based on the provided years and associated values,
        optimized for efficiency using a lambda function.

        Args:
            recordedYear (int/None): The year of the recorded value.
            dateTimeYear (int/None): The year of the datetime value.
            modifiedYear (int/None): The year of the modified value.
            creationYear (int/None): The year of the creation value.
            recordedValue: The value associated with recordedYear.
            dateTimeValue: The value associated with dateTimeYear.
            modifiedValue: The value associated with modifiedYear.
            creationValue: The value associated with creationYear.

        Returns:
            The filtered value based on the logic.
            Exits the program if no valid date/time values are found.
        """
        available_dates = []
        if recordedYear is not None:
            available_dates.append((recordedYear, recordedValue))
        if dateTimeYear is not None:
            available_dates.append((dateTimeYear, dateTimeValue))
        if modifiedYear is not None:
            available_dates.append((modifiedYear, modifiedValue))
        if creationYear is not None:
            available_dates.append((creationYear, creationValue))

        if not available_dates:
            print("No valid date/time values found for row. Exiting program to prevent issues.")
            exit()

        min_date_tuple = min(available_dates, key=lambda x: x[0])
        return min_date_tuple[1]

    # --- Your _calculateFilteredValue function, now using the optimized helper ---
    def _calculateFilteredValue(row: dict) -> str | None:
        """
        Helper function to apply row-wise. Determines the "filtered" value for a single row.
        """
        # Safely get year integers for comparison
        # Important: Ensure _getYearFromColumn can handle None and returns int | None
        dateTimeYear: int | None = _getYearFromColumn(row.get(dateTimeCol))
        recordedYear: int | None = _getYearFromColumn(row.get(recordedCol))
        modifiedYear: int | None = _getYearFromColumn(row.get(modifiedCol))
        creationYear: int | None = _getYearFromColumn(row.get(creationCol))

        # Retrieve original string values (not years) for the final result
        dateTimeValue: str | None = row.get(dateTimeCol)
        recordedValue: str | None = row.get(recordedCol)
        modifiedValue: str | None = row.get(modifiedCol)
        creationValue: str | None = row.get(creationCol)

        # Call the optimized helper function
        return get_filtered_value_lambda_optimized(
            recordedYear, dateTimeYear, modifiedYear, creationYear,
            recordedValue, dateTimeValue, modifiedValue, creationValue
        )

    # Apply the helper function row-wise to create the new "filtered" Series.
    # This automatically ensures the Series has the same length and index as the DataFrame.
    filteredSeries: pd.Series = df.apply(_calculateFilteredValue, axis=1)

    # Insert the Series into the DataFrame at the specified location.
    # The .copy() is crucial here to ensure df is not modified in-place and to return a new DataFrame.
    # If the function is meant to modify in-place and return None, remove the .copy() and the return statement.
    # Given the return type hint `-> pd.DataFrame`, it's safer to return a copy.
    df.insert(6, newColumn, filteredSeries)

    # Process the new "filtered" column to create "indicated"
    # Ensure to handle potential NaNs by converting to string first.
    df["indicated"] = df[newColumn].astype(str).str.replace(":", "", regex=False).str.replace(" ", "_", regex=False)

    return df