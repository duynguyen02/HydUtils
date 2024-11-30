from datetime import datetime
from typing import List, Optional
import pandas as pd

from hydutils.hyd_constants import INTERVAL, TIMESERIES


def validate_columns_for_nulls(
    df: pd.DataFrame, columns: Optional[List[str]] = None, copy_df: bool = False
):
    if copy_df:
        df = df.copy()

    if columns is None:
        columns = df.columns

    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Columns not found in DataFrame: {', '.join(missing_columns)}"
        )

    empty_columns = {
        col: df[df[col].isnull()].index.tolist()
        for col in columns
        if df[col].isnull().any()
    }
    if empty_columns:
        error_message = "Columns with null values:\n" + "\n".join(
            [f"- {col}: rows {rows}" for col, rows in empty_columns.items()]
        )
        raise ValueError(error_message)

    return df


def validate_interval(df: pd.DataFrame, interval: float, copy_df: bool = False):
    if copy_df:
        df = df.copy()

    df[INTERVAL] = df[TIMESERIES].diff()
    interval_hours = pd.Timedelta(hours=interval)

    invalid_intervals = df[INTERVAL] != interval_hours
    invalid_intervals = invalid_intervals & ~df[INTERVAL].isna()

    if invalid_intervals.any():
        first_invalid_idx = invalid_intervals.idxmax()
        row_before = df.loc[first_invalid_idx - 1, TIMESERIES]
        row_invalid = df.loc[first_invalid_idx, TIMESERIES]

        raise ValueError(
            f"The intervals between datetimes are not consistent starting from row {first_invalid_idx}. "
            f"Expected: {interval} hours, but got: {df.loc[first_invalid_idx, INTERVAL]}. "
            f"Datetime mismatch: {row_before} -> {row_invalid}."
        )

    df = df.drop(columns=[INTERVAL])

    return df


def filter_timeseries(
    df: pd.DataFrame,
    start: Optional[datetime],
    end: Optional[datetime],
    copy_df: bool = False,
):
    if copy_df:
        df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[TIMESERIES]):
        raise ValueError("The TIMESERIES column must be of datetime type.")

    min_time = df[TIMESERIES].min()
    max_time = df[TIMESERIES].max()

    if start is not None and (start < min_time or start > max_time):
        raise ValueError("The 'start' parameter is out of the DataFrame's time range.")

    if end is not None and (end < min_time or end > max_time):
        raise ValueError("The 'end' parameter is out of the DataFrame's time range.")

    if start is not None and end is not None and end < start:
        raise ValueError(
            "The 'end' parameter cannot be earlier than the 'start' parameter."
        )

    if start is None and end is None:
        return df
    elif start is None:
        return df[df[TIMESERIES] <= end]
    elif end is None:
        return df[df[TIMESERIES] >= start]
    else:
        return df[(df[TIMESERIES] >= start) & (df[TIMESERIES] <= end)]
