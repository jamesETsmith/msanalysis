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

from msanalysis.plotting.contour import contourf

#
# Read CSV Data from LabView
#
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv("/home/james/Downloads/20200228_TP.csv", names=cols)
df["time"] -= df["time"][0]

#
# Use PyOpenMS to read mzXML
#
exp = MSExperiment()
t0 = time.time()
MzXMLFile().load("/home/james/Downloads/20200228_1175.mzXML", exp)
print(f"Time to load file {time.time()-t0}")

# Dump List of PyOpenMS::Spectra to one NumPy array for MZ and a 2D array for
# intensities
n = len(exp.getSpectra())
mz = exp.getSpectra()[0].get_peaks()[0]
n_pt_per_scan = mz.size
intensities = np.zeros((n, n_pt_per_scan))
times = np.array([spec.getRT() / 1000 for spec in exp.getSpectra()])  # Now in seconds
for i, s in enumerate(exp.getSpectra()):
    intensities[i] = s.get_peaks()[1]

#
# Use timestamps from mzXML and Labview to interpolate temperature for each scan
#
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
keep_ith_scan = 100
X, Y, Z = contourf(mz, intensities, mz_lb, mz_ub, keep_ith_scan=keep_ith_scan)
print(X.shape, Y.shape, Z.shape)

#
# Plot
#

plt.figure()
plt.contourf(X * keep_ith_scan, Y, Z)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity (UNITS UNKNOWN)", rotation=270, fontsize=12, labelpad=15)

# I'm playing some tricks here, and just relabeling the ticks on the x-axis
ax1 = plt.gca()
xticks = np.array(ax1.get_xticks(), dtype=np.int)

# This catch is necessary because sometimes the last tick is out of bonds for our
# interpreted temp data
if xticks[-1] > temp_interp[-1]:
    xticks = xticks[:-1]
ax1.set_xticklabels(["{:.0f}".format(t) for t in temp_interp[xticks]])
plt.xlabel("Temperature $^o$ C")
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex11_contour.png")

#
#
#
plt.figure()
# print(Z.min())
Z += 1e-5
plt.contourf(X * keep_ith_scan, Y, Z, norm=colors.LogNorm(vmin=1e-3, vmax=Z.max()))
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity (UNITS UNKNOWN)", rotation=270, fontsize=12, labelpad=15)
# I'm playing some tricks here, and just relabeling the ticks on the x-axis
ax1 = plt.gca()
xticks = np.array(ax1.get_xticks(), dtype=np.int)

# This catch is necessary because sometimes the last tick is out of bonds for our
# interpreted temp data
if xticks[-1] > temp_interp[-1]:
    xticks = xticks[:-1]
ax1.set_xticklabels(["{:.0f}".format(t) for t in temp_interp[xticks]])

plt.xlabel("Temperature $^o$ C")
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex11_contour_logscale.png")
