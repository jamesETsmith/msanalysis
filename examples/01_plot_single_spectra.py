"""
This example shows how to read a CDF file and plot the first spectra using matplotlib.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import matplotlib.pyplot as plt

from msanalysis.data_extraction import utils
from msanalysis.sample_data import get_cdf_sample_path


#
# Read in CDF
#
times, spectra = utils.read_cdf(get_cdf_sample_path())
scan0 = spectra[0]

#
# Plot
#
plt.figure()
# plt.plot(scan0["intensity"][::2])
plt.plot(scan0["mz"], scan0["intensity"], c="k")
plt.xlabel("M/Z")
plt.ylabel("Intensity")
plt.savefig("figures/ex1.png", dpi=600)

