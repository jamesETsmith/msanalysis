import numpy as np
import pytest

from msanalysis.data_extraction import read_mzXML
from msanalysis.sample_data import get_mzXML_sample_path
from msanalysis.plotting.contour import contourf

npt = np.testing


def test_contourf_def():
    # Test default settings
    data = read_mzXML(get_mzXML_sample_path())
    mz, intensities, times = data["mz"], data["intensities"], data["times"]
    n_scans = intensities.shape[0]
    X, Y, Z = contourf(mz, intensities, 50, 70, keep_ith_scan=1)
    npt.assert_equal(X.shape, Y.shape)
    npt.assert_equal(Y.shape, Z.shape)
    # print(intensities.shape, times.shape, X.shape)
    npt.assert_equal(X.shape[1], times.size)


def test_contourf_keep():
    # Test different keep_ith_scan settings
    # If we keep twice as many scans we don't exactly double the number of points
    # in the contour plot b/c each scan doesn't have the same number of points.
    # That being said it should be roughly double and we see that it is.
    # Test default settings
    data = read_mzXML(get_mzXML_sample_path())
    mz, intensities, times = data["mz"], data["intensities"], data["times"]
    X, Y, Z = contourf(mz, intensities, 50, 70, keep_ith_scan=2)
