"""
This example shows how to read a large text file exported by the Merlin software
and make our contourf plots.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 3/7/2020
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from msanalysis.data_extraction import read_exported_txt
from msanalysis.plotting.contour import contourf
from msanalysis.data_processing.smoothing import moving_average


mz, intensities = read_exported_txt("/home/james/Downloads/TiCl4_SnF4.npz")
mz_lb, mz_ub = (60, 70)

keep_ith_scan = 10
X, Y, Z = contourf(mz, intensities, mz_lb, mz_ub, keep_ith_scan=keep_ith_scan)

#
# Plot
#
plt.figure()

# Plot with NO log scale and NO smoothing
plt.subplot(3, 1, 1)
plt.contourf(X * keep_ith_scan, Y, Z)
cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity (mV)", rotation=270, fontsize=12, labelpad=15)
plt.title("Regular Scale and No Smoothing")


# Plot with log scale and NO smoothing
plt.subplot(3, 1, 2)
plt.contourf(X * keep_ith_scan, Y, Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
cbar = plt.colorbar()
cbar.ax.set_ylabel("Log(Intensity)", rotation=270, fontsize=12)
plt.title("Log Scale and NO Smoothing")


# Plot with log scale AND smoothing
plt.subplot(3, 1, 3)
X, Y, Z = contourf(
    mz, moving_average(intensities, n=150), mz_lb, mz_ub, keep_ith_scan=keep_ith_scan
)
plt.contourf(X * keep_ith_scan, Y, Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()))
cbar = plt.colorbar()
cbar.ax.set_ylabel("Log(Intensity)", rotation=270, fontsize=12)
plt.title("Log Scaling and Smoothing")


plt.ylabel("MZ")
plt.xlabel("Scan Number")
plt.tight_layout()
plt.savefig("figures/ex10.png", dpi=600)
plt.show()

