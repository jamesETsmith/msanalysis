"""
This example shows how to read a CDF file and plot the all of spectra using matplotlib's contourf plots.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import matplotlib.pyplot as plt

from msanalysis.data_extraction import utils
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.plotting import contour


#
# Read in CDF
#
times, spectra = utils.read_cdf(get_cdf_sample_path())
scan0 = spectra[0]

#
# Plot
#
plt.figure()
# plt.plot(scan0["mz"], scan0["intensity"], c="k")
contour.tricontourf(plt.gca(), spectra, 50, 100)
plt.xlabel("Scan #")
plt.ylabel("Intensity")
plt.savefig("figures/ex2.png", dpi=600)

