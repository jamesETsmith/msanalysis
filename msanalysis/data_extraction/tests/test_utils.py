import os
import pytest
import numpy as np

from msanalysis.data_extraction import read_cdf, read_exported_txt
from msanalysis.sample_data import get_cdf_sample_path, get_txt_sample_path

npt = np.testing


def test_read_cdf():
    times, spectra = read_cdf(get_cdf_sample_path())

    npt.assert_equal(times.size, len(spectra))

    # Check output datatypes
    npt.assert_equal(type(times), np.ndarray)
    npt.assert_equal(type(spectra), list)
    npt.assert_equal(type(spectra[0]), dict)

    # Check that individual spectra have desired keys
    npt.assert_equal(set(spectra[0].keys()), {"mz", "intensity"})


def test_read_exported_txt():
    npz_filepath = get_txt_sample_path()[:-3] + "npz"
    if os.path.exists(npz_filepath):
        os.remove(npz_filepath)

    # Read from file
    mz, intensities = read_exported_txt(get_txt_sample_path())
    npt.assert_equal((2, 26947), intensities.shape)
    npt.assert_equal(os.path.exists(npz_filepath), True)

    # Read from npz file
    mz, intensities = read_exported_txt(get_txt_sample_path())
    npt.assert_equal((2, 26947), intensities.shape)
    npt.assert_equal(os.path.exists(npz_filepath), True)
