import pytest
import numpy as np

from msanalysis.data_extraction import utils
from msanalysis.sample_data import get_cdf_sample_path

npt = np.testing


def test_read_cdf():
    times, spectra = utils.read_cdf(get_cdf_sample_path())

    npt.assert_equal(times.size, len(spectra))

    # Check output datatypes
    npt.assert_equal(type(times), np.ndarray)
    npt.assert_equal(type(spectra), list)
    npt.assert_equal(type(spectra[0]), dict)

    # Check that individual spectra have desired keys
    npt.assert_equal(set(spectra[0].keys()), {"mz", "intensity"})
