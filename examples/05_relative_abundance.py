"""
This example shows how to read in MS spectra, get the relative abundances for
several M/Z of interest, and then plot these abundances.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 1/16/2020
Updated: 4/15/2020
"""
import matplotlib.pyplot as plt
import seaborn as sns

from msanalysis.data_extraction import read_mzXML
from msanalysis.data_processing import get_relative_abundance
from msanalysis.sample_data import get_mzXML_sample_path

#
# Read in CDF
#
data = read_mzXML(get_mzXML_sample_path())
mz, intensities, times = data["mz"], data["intensities"], data["times"]

#
# Get abundances
#
mzs = [57, 71]
abun = get_relative_abundance(mz, intensities, mzs)

#
# Plot
#
plt.figure()
sns.set_style("darkgrid")
labels = ["M/Z={}".format(mz) for mz in mzs]
for i, lab in enumerate(labels):
    plt.plot(times, abun[i], label=lab)
plt.xlabel("Time")
plt.ylabel("Intensity")
plt.legend()
plt.tight_layout()
plt.savefig("figures/ex5.png")
