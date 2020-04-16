import os
import pytest
import numpy as np

from msanalysis.data_extraction import read_mzXML, read_exported_txt
from msanalysis.sample_data import get_mzXML_sample_path, get_txt_sample_path

npt = np.testing


def test_read_mzXML():
    data = read_mzXML(get_mzXML_sample_path())
    mz, intensities, times = data["mz"], data["intensities"], data["times"]
    npt.assert_equal(len(intensities.shape), 2)
    npt.assert_equal(times.size, intensities.shape[0])
    npt.assert_equal(mz.size, intensities.shape[1])


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
