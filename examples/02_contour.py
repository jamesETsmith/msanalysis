"""
This example shows how to read an mzXML file exported by the Merlin software
and make a contourf plots.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 3/29/2020
"""
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as colors  # For log color scale
from pyopenms import MSExperiment, MzXMLFile

from msanalysis.data_extraction import read_mzXML
from msanalysis.plotting.contour import contourf
from msanalysis.sample_data import get_mzXML_sample_path, get_csv_sample_path

#
# User specified variables
#

labview_file = get_csv_sample_path()
mzXML_file = get_mzXML_sample_path()
# Users can specify their own path like the lines below
# labview_file = "/home/james/Downloads/20200228_TP.csv"
# mzXML_file = "/home/james/Downloads/20200228_1175.mzXML"


#
# Read CSV Data from LabView
#
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv(labview_file, names=cols)
df["time"] -= df["time"][0]

#
# Use PyOpenMS to read mzXML
#
data = read_mzXML(mzXML_file)
mz, intensities, times = data["mz"], data["intensities"], data["times"]

#
# Use timestamps from mzXML and Labview to interpolate temperature for each scan
#
times /= 1000  # Only using this because I have old mzXML files
temp_interp = np.interp(times, df["time"], df["temp"])
last_lv_time = np.array(df["time"])[-1]

# Only go as far as LabView data
subset = np.where(times < last_lv_time)[0]
times = times[subset]
intensities = intensities[subset, :]

#
# Select a subset of MZ range and plot intensities as a contour plot
#
mz_lb, mz_ub = (60, 280)
keep_ith_scan = 1
X, Y, Z = contourf(mz, intensities, mz_lb, mz_ub, keep_ith_scan=keep_ith_scan)
print(X.shape, Y.shape, Z.shape)


#
# Convenience Function
#
def add_custom_ticks(ax: plt.Axes, tick_interp: np.ndarray):
    # I'm playing some tricks here, and just relabeling the ticks on the x-axis
    xticks = np.array(ax.get_xticks(), dtype=np.int)

    # This catch is necessary because sometimes the last tick is out of bonds for our
    # interpreted temp data
    if xticks[-1] > tick_interp[-1]:
        xticks = xticks[:-1]
    ax.set_xticklabels(["{:.0f}".format(t) for t in tick_interp[xticks]])


#
# Plot contour
#

plt.figure()
plt.contourf(X * keep_ith_scan, Y, Z)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity", rotation=270, fontsize=12, labelpad=15)
add_custom_ticks(plt.gca(), temp_interp)
plt.xlabel("Temperature $^o$ C")
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex2_contour.png")

#
# Plot contour with log scale
#
plt.figure()
Z += 1e-5
plt.contourf(X * keep_ith_scan, Y, Z, norm=colors.LogNorm(vmin=1e-3, vmax=Z.max()))
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity", rotation=270, fontsize=12, labelpad=15)
add_custom_ticks(plt.gca(), temp_interp)
plt.xlabel("Temperature $^o$ C")
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex2_contour_logscale.png")
