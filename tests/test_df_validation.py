import pytest
import pandas as pd
from datetime import datetime, timedelta
from hydutils.hydrology_constants import INTERVAL, TIMESERIES
from hydutils.df_helper import validate_columns_for_nulls, validate_interval, filter_timeseries



def test_validate_columns_for_nulls():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, None], "c": [7, 8, 9]})

    # Test with no columns specified
    with pytest.raises(ValueError, match="Columns with empty data: b"):
        validate_columns_for_nulls(df)

    # Test with specific columns
    with pytest.raises(ValueError, match="Columns with empty data: b"):
        validate_columns_for_nulls(df, columns=["b"])

    # Test with missing columns
    with pytest.raises(ValueError, match="Columns not found in DataFrame: d"):
        validate_columns_for_nulls(df, columns=["d"])

    # Test with no nulls
    result = validate_columns_for_nulls(df, columns=["a", "c"])
    pd.testing.assert_frame_equal(result, df)


def test_validate_interval():
    df = pd.DataFrame({
        TIMESERIES: pd.date_range(start="2023-01-01", periods=5, freq="h")
    })

    # Test valid interval
    result = validate_interval(df, interval=1, copy_df=True)
    pd.testing.assert_frame_equal(result, df)

    # Test invalid interval
    df_invalid = df.copy()
    df_invalid.loc[2, TIMESERIES] += pd.Timedelta(minutes=30)
    with pytest.raises(ValueError, match="The intervals between datetimes are not consistent starting from row 2"):
        validate_interval(df_invalid, interval=1)


def test_filter_timeseries():
    df = pd.DataFrame({
        TIMESERIES: pd.date_range(start="2023-01-01", periods=5, freq="h")
    })

    # Test valid range
    start = datetime(2023, 1, 1, 1)
    end = datetime(2023, 1, 1, 3)
    result = filter_timeseries(df, start=start, end=end)
    expected = df[(df[TIMESERIES] >= start) & (df[TIMESERIES] <= end)]
    pd.testing.assert_frame_equal(result, expected)

    # Test start only
    result = filter_timeseries(df, start=start, end=None)
    expected = df[df[TIMESERIES] >= start]
    pd.testing.assert_frame_equal(result, expected)

    # Test end only
    result = filter_timeseries(df, start=None, end=end)
    expected = df[df[TIMESERIES] <= end]
    pd.testing.assert_frame_equal(result, expected)

    # Test invalid start
    with pytest.raises(ValueError, match="The 'start' parameter is out of the DataFrame's time range."):
        filter_timeseries(df, start=datetime(2022, 12, 31), end=end)

    # Test invalid end
    with pytest.raises(ValueError, match="The 'end' parameter is out of the DataFrame's time range."):
        filter_timeseries(df, start=start, end=datetime(2023, 1, 2))

    # Test start > end
    with pytest.raises(ValueError, match="The 'end' parameter cannot be earlier than the 'start' parameter."):
        filter_timeseries(df, start=end, end=start)
