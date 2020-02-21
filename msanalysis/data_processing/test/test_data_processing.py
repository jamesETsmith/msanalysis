import pytest
import numpy as np

from msanalysis.data_extraction import read_cdf
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.data_processing import get_relative_abundance

npt = np.testing


@pytest.mark.parametrize("mzs", [([57, 71]), ([57, 64, 70, 71])])
def test_rel_abundance(mzs):

    times, spectra = read_cdf(get_cdf_sample_path())

    abun = get_relative_abundance(spectra, mzs)
    npt.assert_equal(abun.shape[0], len(mzs))
    npt.assert_equal(abun.shape[1], len(spectra))
