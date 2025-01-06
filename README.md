# HydUtils

![PyPI - Version](https://img.shields.io/pypi/v/hydutils)

**HydUtils** is a Python utility library designed for data handling and validation, especially for time series and
hydrological datasets. It provides several useful functions for working with time series data, including validation,
filtering, error metrics, and more, making it easier to handle and analyze hydrological and weather-related datasets.

## Installation

```bash
pip install hydutils
```

## Usage

### 1. Validate Columns for Nulls

The function `validate_columns_for_nulls` checks for columns that contain null values and raises an error if any are
found.

```python
from hydutils.df_helper import validate_columns_for_nulls
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
from hydutils.df_helper import validate_interval
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
from hydutils.df_helper import filter_timeseries
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

### 4. Error Metrics

The `hydutils.metrics` module includes several commonly used metrics to evaluate model performance. These include MSE,
RMSE, NSE, R², PBIAS, and FBIAS.

#### 4.1 Mean Squared Error (MSE)

The `mse` function calculates the Mean Squared Error between two arrays.

```python
from hydutils.statistical_metrics import mse
import numpy as np

simulated = np.array([3.0, 4.0, 5.0])
observed = np.array([2.9, 4.1, 5.0])

mse_value = mse(simulated, observed)
```

#### 4.2 Root Mean Squared Error (RMSE)

The `rmse` function calculates the Root Mean Squared Error.

```python
from hydutils.statistical_metrics import rmse

rmse_value = rmse(simulated, observed)
```

#### 4.3 Nash-Sutcliffe Efficiency (NSE)

The `nse` function calculates the Nash-Sutcliffe Efficiency coefficient.

```python
from hydutils.statistical_metrics import nse

nse_value = nse(simulated, observed)
```

#### 4.4 R² (Coefficient of Determination)

The `r2` function calculates the coefficient of determination, R².

```python
from hydutils.statistical_metrics import r2

r2_value = r2(simulated, observed)
```

#### 4.5 Percentage Bias (PBIAS)

The `pbias` function calculates the Percentage Bias between observed and simulated values.

```python
from hydutils.statistical_metrics import pbias

pbias_value = pbias(observed, simulated)
```

#### 4.6 Fractional Bias (FBIAS)

The `fbias` function calculates the Fractional Bias between observed and simulated values.

```python
from hydutils.statistical_metrics import fbias

fbias_value = fbias(observed, simulated)
```

## License

This library is released under the MIT License.
