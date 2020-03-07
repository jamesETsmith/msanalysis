"""
Data post-processing for matplotlib contour plots.
"""
import numpy as np

from msanalysis.plotting import select_mz_range


def tricontourf(
    spectra: list, mz_lower: float, mz_upper: float, keep_ith_scan: int = 50, x_ax=None
):

    print(
        "Suggestion: Choose a larger window than you want and then resize your plot to the desired window size"
    )

    # Convert data to three arrays for tricontourf
    x = []
    y = []
    z = []

    for i, spectra_i in enumerate(spectra):
        if i % keep_ith_scan != 0:  # Controls spacing of scan #
            continue

        mass_i, intensity_i = select_mz_range(
            mz_lower, mz_upper, spectra_i["mz"], spectra_i["intensity"]
        )

        n_y = mass_i.size

        y += mass_i.tolist()
        z += intensity_i.tolist()

        if x_ax is None:
            x += [i] * n_y
        else:
            x += [x_ax[i]] * n_y

    return (np.array(x), np.array(y), np.array(z))


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
