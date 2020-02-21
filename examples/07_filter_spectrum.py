"""
This example shows how to filter an individual spectra.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 2/18/19
"""
import numpy as np
import matplotlib.pyplot as plt

from msanalysis.data_extraction import read_cdf
from msanalysis.sample_data import get_cdf_sample_path
from msanalysis.data_processing import filter_spectrum
from msanalysis.data_processing import calculate_abundance


def gauss_conv(x, A, x0):
    y = np.zeros_like(x)
    for A_i, x0_i in zip(A, x0):
        y += A_i * np.exp(-0.5 * ((x - x0_i) / 0.1) ** 2)
    y += np.random.rand(x.size) * 0.05
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

#
#
#
new_scan0 = filter_spectrum(scan0)

#
# Plot
#
plt.figure()
plt.plot(scan0["mz"], scan0["intensity"], "o", c="k", label="Unfiltered")
plt.plot(new_scan0["mz"], new_scan0["intensity"], c="b", label="Filtered")
plt.xlabel("M/Z")
plt.ylabel("Intensity")
plt.savefig("figures/ex7.png", dpi=600)
plt.show()
