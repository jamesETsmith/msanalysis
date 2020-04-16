"""
This example shows how to read a mzXML file and plot the first spectra using matplotlib.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import matplotlib.pyplot as plt
import seaborn as sns

from msanalysis.data_extraction import read_mzXML
from msanalysis.sample_data import get_mzXML_sample_path


#
# Read in CDF
#
data = read_mzXML(get_mzXML_sample_path())
mz, intensities, times = data["mz"], data["intensities"], data["times"]

#
# Plot
#
plt.figure()
sns.set_style("darkgrid")
plt.plot(mz, intensities[0], c="k")
plt.xlim((30, 125))
plt.xlabel("M/Z")
plt.ylabel("Intensity")
plt.tight_layout()
plt.savefig("figures/ex1.png", dpi=600)
