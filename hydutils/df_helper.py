from datetime import datetime
from typing import List, Optional
import pandas as pd

from hydutils.hydrology_constants import INTERVAL, TIMESERIES, TIMESTAMP


class MissingColumnsError(Exception):
    """Exception raised when required columns are missing from the DataFrame."""
    pass


class NullValuesError(Exception):
    """Exception raised when columns contain null values."""
    pass


def validate_columns_for_nulls(
        df: pd.DataFrame, columns: Optional[List[str]] = None, copy_df: bool = False
) -> pd.DataFrame:
    """
    Validate that specified columns exist in the DataFrame and do not contain null values.

    Parameters:
        df (pd.DataFrame): The DataFrame to validate.
        columns (Optional[List[str]]): List of columns to validate. If None, all columns are checked.
        copy_df (bool): Whether to create a copy of the DataFrame before validation.

    Returns:
        pd.DataFrame: The original or copied DataFrame if validation passes.

    Raises:
        MissingColumnsError: If specified columns are not found in the DataFrame.
        NullValuesError: If specified columns contain null values.
    """
    if copy_df:
        df = df.copy()

    if columns is None:
        columns = df.columns.tolist()

    # Check for missing columns
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        valid_columns = ', '.join(df.columns)
        raise MissingColumnsError(
            f"Columns not found in DataFrame: {', '.join(missing_columns)}.\n"
            f"Available columns: {valid_columns}"
        )

    # Check for null values in specified columns
    empty_columns = {
        col: df[df[col].isnull()].index.tolist()
        for col in columns
        if df[col].isnull().any()
    }
    if empty_columns:
        error_message = "Columns with null values:\n" + "\n".join(
            [f"- {col}: rows {rows}" for col, rows in empty_columns.items()]
        )
        raise NullValuesError(error_message)

    return df


class InvalidIntervalError(Exception):
    """Exception raised when intervals between datetime are inconsistent."""
    pass


def validate_interval(
        df: pd.DataFrame,
        interval: float,
        timestamp_column: str = TIMESTAMP,
        interval_column: Optional[str] = INTERVAL,
        copy_df: bool = False
) -> pd.DataFrame:
    """
    Validate that the intervals between consecutive datetime in a DataFrame are consistent.

    Parameters:
        df (pd.DataFrame): The DataFrame to validate.
        interval (float): Expected interval between consecutive datetime, in hours.
        timestamp_column (str): Column containing datetime values. Default is "Timeseries".
        interval_column (Optional[str]): Temporary column name to store interval differences. Default is "Interval".
        copy_df (bool): Whether to create a copy of the DataFrame before validation.

    Returns:
        pd.DataFrame: The original or copied DataFrame if validation passes.

    Raises:
        InvalidIntervalError: If intervals between consecutive datetime are inconsistent.
    """
    if copy_df:
        df = df.copy()

    if timestamp_column not in df.columns:
        raise KeyError(f"Column '{timestamp_column}' not found in DataFrame.")

    # Calculate interval differences
    df[interval_column] = df[timestamp_column].diff()
    interval_hours = pd.Timedelta(hours=interval)

    # Identify invalid intervals
    invalid_intervals = (df[interval_column] != interval_hours) & ~df[interval_column].isna()

    if invalid_intervals.any():
        # Get details of the first invalid row
        first_invalid_idx = invalid_intervals.idxmax()
        row_before = df.loc[first_invalid_idx - 1, timestamp_column]
        row_invalid = df.loc[first_invalid_idx, timestamp_column]
        invalid_value = df.loc[first_invalid_idx, interval_column]

        # Count total invalid rows
        total_invalid = invalid_intervals.sum()

        raise InvalidIntervalError(
            f"Inconsistent intervals detected starting from row {first_invalid_idx}. "
            f"Expected: {interval} hours, but got: {invalid_value}. "
            f"Datetime mismatch: {row_before} -> {row_invalid}. "
            f"Total invalid rows: {total_invalid}."
        )

    # Drop the temporary interval column
    df = df.drop(columns=[interval_column])

    return df


class InvalidTimeRangeError(Exception):
    """Exception raised for invalid start or end times in the timeseries filter."""
    pass


def filter_timeseries(
        df: pd.DataFrame,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timestamp_column: str = TIMESTAMP,
        copy_df: bool = False,
) -> pd.DataFrame:
    """
    Filter a DataFrame based on a time range.

    Parameters:
        df (pd.DataFrame): The DataFrame to filter.
        start (Optional[datetime]): The start time for filtering. Rows earlier than this time are excluded.
        end (Optional[datetime]): The end time for filtering. Rows later than this time are excluded.
        timestamp_column (str): The name of the column containing datetime values.
        copy_df (bool): Whether to create a copy of the DataFrame before filtering.

    Returns:
        pd.DataFrame: The filtered DataFrame.

    Raises:
        InvalidTimeRangeError: If the time range parameters are invalid or out of bounds.
        KeyError: If the specified timeseries column does not exist in the DataFrame.
        ValueError: If the timeseries column is not of datetime type.
    """
    if copy_df:
        df = df.copy()

    if timestamp_column not in df.columns:
        raise KeyError(f"Column '{timestamp_column}' not found in the DataFrame.")

    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_column]):
        raise ValueError(f"The column '{timestamp_column}' must be of datetime type.")

    # Get time range of the DataFrame
    min_time = df[timestamp_column].min()
    max_time = df[timestamp_column].max()

    # Validate 'start' and 'end' parameters
    if start is not None:
        if not isinstance(start, datetime):
            raise TypeError(f"The 'start' parameter must be a datetime object, got {type(start)}.")
        if start < min_time or start > max_time:
            raise InvalidTimeRangeError(
                f"The 'start' parameter ({start}) is out of bounds. DataFrame time range: {min_time} to {max_time}."
            )

    if end is not None:
        if not isinstance(end, datetime):
            raise TypeError(f"The 'end' parameter must be a datetime object, got {type(end)}.")
        if end < min_time or end > max_time:
            raise InvalidTimeRangeError(
                f"The 'end' parameter ({end}) is out of bounds. DataFrame time range: {min_time} to {max_time}."
            )

    if start is not None and end is not None and end < start:
        raise InvalidTimeRangeError(
            f"The 'end' parameter ({end}) cannot be earlier than the 'start' parameter ({start})."
        )

    # Apply filtering
    mask = pd.Series(True, index=df.index)
    if start is not None:
        mask &= df[timestamp_column] >= start
    if end is not None:
        mask &= df[timestamp_column] <= end

    return df[mask]
