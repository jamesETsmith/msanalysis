"""
This example demonstrates how to switch the contourf plots to a log scale so that
smaller peaks show up on the same contourf plot.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 1/7/20
"""


import matplotlib.pyplot as plt
import matplotlib.colors as colors  # For log color scale
import pandas as pd
import numpy as np

from msanalysis.data_extraction import read_cdf
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.sample_data import get_labview_sample_path
from msanalysis.plotting import contour


#
# Read in CDF
#
times, spectra = read_cdf(get_cdf_sample_path())
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
mz_upper = 225
mz_lower = 100


plt.figure()
plt.ylim(mz_lower + 5, mz_upper - 5)

# Use the interpolated temp values here is a bad idea because they aren't monotonically increasing
# norm=... in tricontourf() changes the colorscale to log
x, y, z = contour.tricontourf(spectra, mz_lower, mz_upper)
plt.tricontourf(x, y, z, norm=colors.LogNorm(vmin=z.min(), vmax=z.max()))
plt.colorbar()

# I'm playing some tricks here, and just relabeling the ticks on the x-axis
ax1 = plt.gca()
xticks = np.array(ax1.get_xticks(), dtype=np.int)

# This catch is necessary because sometimes the last tick is out of bonds for our
# interpreted temp data
if xticks[-1] > temp_interp[-1]:
    xticks = xticks[:-1]
ax1.set_xticklabels(["{:.0f}".format(t) for t in temp_interp[xticks]])


plt.xlabel("Temperature of Probe ($^o$ C)")
plt.savefig("figures/ex4.png", dpi=600)
plt.show()
