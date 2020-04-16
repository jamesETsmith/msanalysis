"""
This example shows how to read an mzXML file exported by the Merlin software
and make a contourf plots where we skip certain ranges in MZ.

Based on https://matplotlib.org/examples/pylab_examples/broken_axis.html

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 4/10/2020
"""
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as colors  # For log color scale

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
# Plot
#

fig, axes = plt.subplots(2, 1, sharex=True)

# Without Log Scale
m = axes[0].contourf(X * keep_ith_scan, Y, Z)
axes[1].contourf(X * keep_ith_scan, Y, Z)

# With Log Scale
# m = axes[0].contourf(X * keep_ith_scan, Y, Z + 1e-4, norm=colors.LogNorm(vmin=1e-3, vmax=Z.max()))
# axes[1].contourf(X * keep_ith_scan, Y, Z + 1e-4, norm=colors.LogNorm(vmin=1e-3, vmax=Z.max()))

# Setting Ranges for each section
axes[1].set_ylim(70, 80)
axes[0].set_ylim(125, 140)

# Playing with Ticks
axes[0].spines["top"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[0].xaxis.tick_top()
axes[0].tick_params(labeltop=False, top=False)  # don't put tick labels at the top

# Make the pretty slashes
d = 0.015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=axes[0].transAxes, color="k", clip_on=False)
axes[0].plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
axes[0].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=axes[1].transAxes)  # switch to the bottom axes
axes[1].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
axes[1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal


cbar = fig.colorbar(m, ax=axes)
cbar.ax.set_ylabel("Intensity", rotation=270, fontsize=12, labelpad=15)
add_custom_ticks(plt.gca(), temp_interp)
plt.xlabel("Temperature $^o$ C")
plt.ylabel("M/Z")
axes[0].set_title("Split MZ Scale Contour Plots")
plt.savefig("figures/ex3.png", dpi=600)
