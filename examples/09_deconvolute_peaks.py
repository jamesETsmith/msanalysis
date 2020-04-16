"""
This example shows how to deconvolute two isotopic abundances combined in an artificial spectra.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 2/18/19
"""
import numpy as np
import matplotlib.pyplot as plt

from msanalysis.data_processing import calculate_abundance, deconvolute_spectrum

npt = np.testing

#
# Helper functions
#


def gauss_conv(x, A, x0, noise=True):
    y = np.zeros_like(x)
    for A_i, x0_i in zip(A, x0):
        y += A_i * np.exp(-0.5 * ((x - x0_i) / 0.1) ** 2)
    if noise:
        y += np.random.rand(x.size) * 0.02
    return y


#
# Choose your adventure!
# Here are some examples ranging from no overlap in the isotopic envelop to a lot of overlap.
# Uncomment the example you want to try below
#
# species, ratio = (["InCl", "InCl2", "InC2H6"], [2, 35, 6])
species, ratio = (["MoF2Cl2", "MoO6", "MoO2Cl2"], [1.5, 2.5, 4.7])
# species, ratio = (["MoF2Cl2", "MoF2HCl2", "MoO4Cl"], [29, 3100, 30])
# species, ratio = (["MoF2HCl2", "MoO4Cl"], [3100, 31])
# species, ratio = (["CO", "CN"], [17, 41])
# species, ratio = (["CO", "CN", "B2H", "O2"], [20, 40, 37, 12])
# species, ratio = (["FeS", "MnO2", "VF2", "GaNH2"], [45, 63, 21, 17])


#
# Set up data and deconvolute
#

data = [calculate_abundance(sp) for sp in species]
xmin = np.min([np.min(d["mz"]) for d in data]) * 0.95
xmax = np.max([np.max(d["mz"]) for d in data]) * 1.025
x = np.linspace(xmin, xmax, num=2000)
print(xmin, xmax)
y = [gauss_conv(x, d["intensity"], d["mz"], noise=False) for d in data]

scan = {}
scan["mz"] = x
scan["intensity"] = np.zeros_like(x)
for i, r in enumerate(ratio):
    scan["intensity"] += y[i] * r

calc_ratio, species_spectra = deconvolute_spectrum(scan, species, return_embedded=True)


# Create reconstructed spectra
y_final = np.zeros_like(x)
for sp in species_spectra:
    intensity = sp["intensity"]
    mz = sp["mz"]
    y_final += gauss_conv(x, intensity, mz, noise=False)
# print(np.linalg.norm(y_final - scan["intensity"]))

fig = plt.figure()

# Artificial "Real" Spectrum
plt.subplot(2, 2, 1)
plt.title("Real Spectrum")
plt.plot(scan["mz"], scan["intensity"])
plt.xlim(x[0], x[-1])

# Isolated Isotopic Abundances
plt.subplot(2, 2, 2)
plt.title("Isolated Isotopic Abund.")
for i, d in enumerate(data):
    plt.bar(d["mz"], d["intensity"], label=species[i])
plt.legend()
plt.xlim(x[0], x[-1])

# Scaled isotopic abundances
plt.subplot(2, 2, 3)
plt.title("Scaled Isotopic Spectra (Stacked)")
plt.bar(species_spectra[0]["mz"], species_spectra[0]["intensity"], label=species[i])
for i, sp in enumerate(species_spectra):
    if i == 0:
        continue
    plt.bar(
        sp["mz"],
        sp["intensity"],
        bottom=species_spectra[i - 1]["intensity"],
        label=species[i],
    )
plt.xlim(x[0], x[-1])
plt.legend()

# Reconstructed spectra made from convoluting gaussian with scaled isotopic abundances
plt.subplot(2, 2, 4)
plt.title("Reconstructed Spectrum")
plt.plot(x, y_final, label="Recon. Spectrum")
# plt.plot(x + 0.1, np.abs(y_final - scan["intensity"]), label="Error")
plt.xlim(x[0], x[-1])
# plt.legend()

plt.tight_layout()
plt.savefig("figures/ex9.png", dpi=600)
plt.show()
