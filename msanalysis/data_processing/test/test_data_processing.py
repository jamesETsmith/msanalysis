import pytest
import numpy as np

from msanalysis.data_extraction import read_mzXML
from msanalysis.sample_data import get_mzXML_sample_path
from msanalysis.data_processing import get_relative_abundance

npt = np.testing


@pytest.mark.parametrize("mzs", [([57, 71]), ([57, 64, 70, 71])])
def test_rel_abundance(mzs):

    data = read_mzXML(get_mzXML_sample_path())
    mz, intensities, times = data["mz"], data["intensities"], data["times"]

    abun = get_relative_abundance(mz, intensities, mzs)
    npt.assert_equal(abun.shape[0], len(mzs))
    npt.assert_equal(abun.shape[1], intensities.shape[0])
