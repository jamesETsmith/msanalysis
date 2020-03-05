"""
This example shows how to calculate and plot the stick spectrum for the
isotopic abundance of molecule.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 1/20/20
"""

import matplotlib.pyplot as plt
import seaborn as sns

from msanalysis.data_processing import calculate_abundance

#
# Calculate Abundances for a Molecular Formula
#
data = calculate_abundance("Sn2C5H15")

#
# Plot
#

plt.figure()
sns.set_style("darkgrid")
plt.bar(data["mz"], data["intensity"], width=0.2)
plt.xlabel("M/Z")
plt.ylabel("Relative Fraction of Intensity")
plt.savefig("figures/ex6.png", dpi=600)
