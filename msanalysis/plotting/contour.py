"""
Data post-processing for matplotlib contour plots.
"""
import numpy as np

from msanalysis.plotting import select_mz_range


def contourf(
    mz: np.ndarray,
    intensities: np.ndarray,
    mz_lower: float,
    mz_upper: float,
    keep_ith_scan: int = 50,
):

    lb, ub = (mz_lower, mz_upper)
    indices = np.where((mz > lb) & (mz < ub))[0]
    trimmed_mz = mz[indices]
    trimmed_intensities = intensities[:, indices]

    Z = trimmed_intensities[::keep_ith_scan, :]
    y = np.arange(Z.shape[0])
    X, Y = np.meshgrid(y, trimmed_mz)

    return X, Y, Z.T
