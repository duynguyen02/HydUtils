# HydUtils

![PyPI - Version](https://img.shields.io/pypi/v/hydutils)

**HydUtils** is a Python utility library designed for data handling and validation, especially for time series and hydrological datasets. It provides several useful functions for working with time series data, including validation, filtering, and checking for missing values.

This library helps ensure data integrity and consistency, making it easier to work with time-based datasets.

## Installation

```bash
pip install hydutils
```

## Usage

### 1. Validate Columns for Nulls

The function `validate_columns_for_nulls` checks for columns that contain null values and raises an error if any are found.

```python
from hydutils.df_validation import validate_columns_for_nulls
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, None], "c": [7, 8, 9]})

# Validate for null values in any column
validate_columns_for_nulls(df)

# Specify columns to check
validate_columns_for_nulls(df, columns=["b"])

# Handling missing columns
validate_columns_for_nulls(df, columns=["d"])  # This will raise an error if column "d" is missing
```

### 2. Validate Time Series Interval

The `validate_interval` function checks that the time intervals between rows in the time series are consistent.

```python
from hydutils.df_validation import validate_interval
import pandas as pd

df = pd.DataFrame({
    "time": pd.date_range(start="2023-01-01", periods=5, freq="h")
})

# Check if the time intervals are consistent
validate_interval(df, interval=1)
```

### 3. Filter Time Series

The `filter_timeseries` function allows you to filter your time series DataFrame based on a start and/or end date.

```python
from hydutils.df_validation import filter_timeseries
import pandas as pd
from datetime import datetime

df = pd.DataFrame({
    "time": pd.date_range(start="2023-01-01", periods=5, freq="h")
})

# Filter data between a start and end date
start = datetime(2023, 1, 1, 1)
end = datetime(2023, 1, 1, 3)
filtered_data = filter_timeseries(df, start=start, end=end)
```

## License

This library is released under the MIT License.

