"""
This example shows how to find peaks from an artificially created spectrum.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 2/18/19
"""
import numpy as np
import matplotlib.pyplot as plt

from msanalysis.data_processing import find_ms_peaks
from msanalysis.data_processing import calculate_abundance


def gauss_conv(x, A, x0):
    y = np.zeros_like(x)
    for A_i, x0_i in zip(A, x0):
        y += A_i * np.exp(-0.5 * ((x - x0_i) / 0.1) ** 2)
    y += np.random.rand(x.size) * 0.02
    return y


#
# Create spectra from isotopic abundance
#
data = calculate_abundance("AlCl2Br")
x = np.linspace(150, 200, num=1000)
y = gauss_conv(x, data["intensity"], data["mz"])
scan0 = {}
scan0["mz"] = x
scan0["intensity"] = y

new_scan0 = find_ms_peaks(scan0, prominence=0.03)

#
# Plot
#
plt.figure()
# plt.plot(scan0["intensity"][::2])
plt.plot(scan0["mz"], scan0["intensity"], c="k", label="Unfiltered")
plt.bar(new_scan0["mz"], new_scan0["intensity"], label="Filtered")
plt.xlabel("M/Z")
plt.ylabel("Intensity")
plt.savefig("figures/ex8.png", dpi=600)
plt.show()
