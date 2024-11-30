import numpy as np


def mse(x: np.ndarray, y: np.ndarray):
    return ((x - y) ** 2).mean()


def rmse(x: np.ndarray, y: np.ndarray):
    return np.sqrt(mse(x, y))


def nse(sim: np.ndarray, obs: np.ndarray):
    obs_mean = obs.mean()
    return 1 - (np.square(obs - sim).sum() / np.square(obs - obs_mean).sum())


def r2(x: np.ndarray, y: np.ndarray):
    n = x.shape[0]

    nu = (n * ((x * y).sum()) - (x.sum()) * (y.sum())) ** 2
    de = (n * ((x**2).sum()) - (x.sum()) ** 2) * (n * ((y**2).sum()) - (y.sum()) ** 2)

    return nu / de


def pbias(obs: np.ndarray, sim: np.ndarray):
    return (obs - sim).sum() * 100 / obs.sum()


def fbias(obs: np.ndarray, sim: np.ndarray):
    return (sim.sum() - obs.sum()) / (0.5 * (sim.sum() + obs.sum()))
