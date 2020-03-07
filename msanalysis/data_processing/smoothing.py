import numpy as np


def moving_average(intensities: np.ndarray, n=50) -> np.ndarray:
    """Calculates the moving average along the n_scans axis of the intensities array.
    
    Adapted from https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy


    Parameters
    ----------
    intensities : np.ndarray
        (n_scans, scan_size) 2D numpy array.
    n : int, optional
        Width of the moving average, by default 50.
    
    Returns
    -------
    np.ndarray
        New intensities with shape (n_scans - n + 1, scan_size)
    """

    new_intensities = np.zeros((intensities.shape[0] - n + 1, intensities.shape[1]))

    # Iterate over each mz value
    for i in range(intensities.shape[1]):
        a = intensities[:, i]
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        new_intensities[:, i] = ret[n - 1 :] / n

    return new_intensities
