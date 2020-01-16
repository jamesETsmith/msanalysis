"""
This example shows how to read a CDF file and plot the all of spectra using matplotlib's contourf plots.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import matplotlib.pyplot as plt

from msanalysis.data_extraction import read_cdf
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.plotting import contour


#
# Read in CDF
#
times, spectra = read_cdf(get_cdf_sample_path())
scan0 = spectra[0]

#
# Plot
#

# It helps the tricontourf to space these larger then the window you
# actually want and then crop out the edges
mz_upper = 105
mz_lower = 45

plt.figure()
x, y, z = contour.tricontourf(spectra, mz_lower, mz_upper)
plt.tricontourf(x, y, z)
plt.colorbar()

plt.ylim(mz_lower + 5, mz_upper - 5)
plt.ylabel("M/Z")
plt.xlabel("Scan #")
plt.savefig("figures/ex2.png", dpi=600)

