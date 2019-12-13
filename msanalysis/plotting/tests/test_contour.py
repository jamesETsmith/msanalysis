import numpy as np
import pytest

from msanalysis.data_extraction import utils
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.plotting import contour

npt = np.testing


def test_tricontourf_def():
    # Test default settings
    times, spectra = utils.read_cdf(get_cdf_sample_path())
    x, y, z = contour.tricontourf(spectra, 50, 100)
    npt.assert_equal(510, x.size)


def test_tricontourf_keep():
    # Test different keep_ith_scan settings
    # If we keep twice as many scans we don't exactly double the number of points
    # in the contour plot b/c each scan doesn't have the same number of points.
    # That being said it should be roughly double and we see that it is.
    times, spectra = utils.read_cdf(get_cdf_sample_path())
    x, y, z = contour.tricontourf(spectra, 50, 100, keep_ith_scan=25)
    npt.assert_equal(1031, x.size)

