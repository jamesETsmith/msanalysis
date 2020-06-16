"""
This example shows how to read in MS spectra, get the relative abundances for
several M/Z of interest, and then plot these abundances.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 1/16/2020
Updated: 4/15/2020
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from msanalysis.data_extraction import read_mzXML
from msanalysis.data_processing import get_relative_abundance
from msanalysis.sample_data import get_mzXML_sample_path, get_csv_sample_path

#
# User specified variables
#

labview_file = get_csv_sample_path()
mzXML_file = get_mzXML_sample_path()
# Users can specify their own path like the lines below
# labview_file = "/home/james/Downloads/20200228_TP.csv"
# mzXML_file = "/home/james/Downloads/20200228_1175.mzXML"
# labview_file = "20200612_TP.csv"
# mzXML_file = "20200612_2735.mzXML"

#
# Read CSV Data from LabView
#
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv(labview_file, names=cols)
df["time"] -= df["time"][0]
last_lv_time = np.array(df["time"])[-1]

#
# Read in mzXML
#
data = read_mzXML(mzXML_file)
mz, intensities, times = data["mz"], data["intensities"], data["times"]
# Only go as far as LabView data (which we are assuming is always shut off after the mass spec)
subset = np.where(times <= last_lv_time)[0]
times = times[subset]
intensities = intensities[subset]

#
# Use timestamps from mzXML and Labview to interpolate temperature for each scan
#
temp_interp = np.interp(times, df["time"], df["temp"])

#
# Get abundances
#
mzs = [137, 157, 172]
abun = get_relative_abundance(mz, intensities, mzs)

#
# Plot
#
plt.figure()
sns.set_style("darkgrid")
labels = ["M/Z={}".format(mz) for mz in mzs]
for i, lab in enumerate(labels):
    plt.plot(temp_interp, abun[i], label=lab)
plt.xlabel("Temperature $^o$ C")
plt.ylabel("Intensity")
plt.legend()
plt.tight_layout()
plt.savefig("figures/ex5.png", dpi=600)
