"""
Data post-processing for matplotlib contour plots.
"""
import numpy as np

from msanalysis.plotting import select_mz_range


def tricontourf(
    spectra: list, mz_lower: float, mz_upper: float, scan_skip: int = 50, x_ax=None
):

    #
    # Convert data to three lists for tricontourf
    #

    x = []
    y = []
    z = []

    for i, spectra_i in enumerate(spectra):
        if i % scan_skip != 0:  # Controls spacing of scan #
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
