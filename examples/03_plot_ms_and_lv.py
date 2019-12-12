"""
This example shows how to read a CDF file, plot the all of spectra using 
matplotlib's contourf plots, and then change the x axis be temperature.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from msanalysis.data_extraction import utils
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.sample_data import get_labview_sample_path
from msanalysis.plotting import contour


#
# Read in CDF
#
times, spectra = utils.read_cdf(get_cdf_sample_path())
scan0 = spectra[0]

#
# Read in LabView Data
#
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv(get_labview_sample_path(), names=cols)
df["time"] -= df["time"][0]

#
# Interpolate LabView Data
#

# temp_interp = np.arange(times.size)
temp_interp = np.interp(times, df["time"], df["temp"])
last_lv_time = np.array(df["time"])[-1]

# Only go as far as LabView data
subset = np.where(times < last_lv_time)[0]
times = times[subset]
spectra = [spectra[i] for i in subset]

# Uncomment this to check that the interpolation looks good
# plt.figure()
# plt.plot(df["time"], df["temp"])
# plt.plot(times, temp_interp[: times.size])
# plt.show()

#
# Plot
#

# It helps the tricontourf to space these larger then the window you
# actually want and then crop out the edges
mz_upper = 105
mz_lower = 45


plt.figure()
plt.ylim(mz_lower + 5, mz_upper - 5)

# Use the interpolated temp values here is a bad idea because they aren't monotonically increasing
x, y, z = contour.tricontourf(spectra, mz_lower, mz_upper)
plt.tricontourf(x, y, z)
plt.colorbar()

# I'm playing some tricks here, and just relabeling the ticks on the x-axis
ax1 = plt.gca()
xticks = np.array(ax1.get_xticks(), dtype=np.int)
ax1.set_xticklabels(["{:.2f}".format(t) for t in temp_interp[xticks]])


plt.xlabel("Temperature of Probe ($^o$ C)")
plt.savefig("figures/ex3.png", dpi=600)

