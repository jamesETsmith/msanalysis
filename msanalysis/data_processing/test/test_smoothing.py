import numpy as np

from msanalysis.data_processing.smoothing import moving_average

npt = np.testing


def test_moving_average():
    n_scans, scan_size = (111, 222)
    intensities = np.zeros((n_scans, scan_size))

    for i in range(scan_size):
        intensities[:, i] = np.arange(n_scans)

    new_intensities = moving_average(intensities, 3)
    npt.assert_array_equal(new_intensities, intensities[1:-1, :])
