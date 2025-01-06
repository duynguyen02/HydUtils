import numpy as np

def mse(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates the Mean Squared Error (MSE) between two arrays.

    Parameters:
        x (np.ndarray): Predicted or simulated values.
        y (np.ndarray): Observed or actual values.

    Returns:
        float: The mean squared error.
    """
    return ((x - y) ** 2).mean()


def rmse(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates the Root Mean Squared Error (RMSE) between two arrays.

    Parameters:
        x (np.ndarray): Predicted or simulated values.
        y (np.ndarray): Observed or actual values.

    Returns:
        float: The root mean squared error.
    """
    return np.sqrt(mse(x, y))


def nse(sim: np.ndarray, obs: np.ndarray) -> float:
    """
    Calculates the Nash-Sutcliffe Efficiency (NSE) coefficient.

    Parameters:
        sim (np.ndarray): Simulated or predicted values.
        obs (np.ndarray): Observed or actual values.

    Returns:
        float: The NSE coefficient, where values close to 1 indicate better model performance.
    """
    obs_mean = obs.mean()
    return 1 - (np.square(obs - sim).sum() / np.square(obs - obs_mean).sum())


def r2(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates the coefficient of determination (R²) between two arrays.

    Parameters:
        x (np.ndarray): Independent variable or predictor.
        y (np.ndarray): Dependent variable or response.

    Returns:
        float: The R² value, where values closer to 1 indicate a better fit.
    """
    n = x.shape[0]
    numerator = (n * (x * y).sum() - x.sum() * y.sum()) ** 2
    denominator = ((n * (x**2).sum() - (x.sum())**2) * (n * (y**2).sum() - (y.sum())**2))
    return numerator / denominator


def pbias(obs: np.ndarray, sim: np.ndarray) -> float:
    """
    Calculates the Percentage Bias (PBIAS) between observed and simulated values.

    Parameters:
        obs (np.ndarray): Observed or actual values.
        sim (np.ndarray): Simulated or predicted values.

    Returns:
        float: The PBIAS value, where lower absolute values indicate better performance.
    """
    return (obs - sim).sum() * 100 / obs.sum()


def fbias(obs: np.ndarray, sim: np.ndarray) -> float:
    """
    Calculates the Fractional Bias (FBIAS) between observed and simulated values.

    Parameters:
        obs (np.ndarray): Observed or actual values.
        sim (np.ndarray): Simulated or predicted values.

    Returns:
        float: The FBIAS value, where values close to 0 indicate better performance.
    """
    return (sim.sum() - obs.sum()) / (0.5 * (sim.sum() + obs.sum()))
