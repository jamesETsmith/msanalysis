"""
This example shows how to read an mzXML file exported by the Merlin software
and make a contourf plots.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 3/29/2020
"""
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors  # For log color scale
from pyopenms import MSExperiment, MzXMLFile

from msanalysis.plotting.contour import contourf

# Use PyOpenMS to read mzXML
exp = MSExperiment()
t0 = time.time()
MzXMLFile().load("/home/james/Downloads/20200310_70.mzXML", exp)
print(f"Time to load file {time.time()-t0}")

# Dump List of PyOpenMS::Spectra to one NumPy array for MZ and a 2D array for
# intensities
n = len(exp.getSpectra())
intensities = np.zeros((n, 12097))
mz = exp.getSpectra()[0].get_peaks()[0]

for i, s in enumerate(exp.getSpectra()):
    intensities[i] = s.get_peaks()[1]

# Select a subset of MZ range and plot intensities as a contour plot
mz_lb, mz_ub = (60, 280)
keep_ith_scan = 1
X, Y, Z = contourf(mz, intensities, mz_lb, mz_ub, keep_ith_scan=keep_ith_scan)

#
# Plot
#
plt.figure()
plt.plot(exp.getSpectra()[5000].get_peaks()[0], exp.getSpectra()[5000].get_peaks()[1])
plt.xlim((190, 220))
plt.ylabel("Intensitiy (UNITS UNKNOWN)")
plt.xlabel("MZ")
plt.savefig("figures/ex11_single.png")

plt.figure()
plt.contourf(X * keep_ith_scan, Y, Z)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity (UNITS UNKNOWN)", rotation=270, fontsize=12, labelpad=15)
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex11_contour.png")

plt.figure()
# print(Z.min())
Z += 1e-5
plt.contourf(X * keep_ith_scan, Y, Z, norm=colors.LogNorm(vmin=1e-3, vmax=Z.max()))
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity (UNITS UNKNOWN)", rotation=270, fontsize=12, labelpad=15)
plt.title("Regular Scale and No Smoothing")
plt.savefig("figures/ex11_contour_logscale.png")
