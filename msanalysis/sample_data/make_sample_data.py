from pyopenms import MSExperiment, MzXMLFile
import pandas as pd

#
# Make smaller mzXML file to keep in repo
#
big_mzXMLfile = "/home/james/Downloads/20200228_1175.mzXML"
n_spectra_to_keep = 10

exp = MSExperiment()
MzXMLFile().load(big_mzXMLfile, exp)
print(f"Full size of experiment {len(exp.getSpectra())}")

spec = []
for i, s in enumerate(exp.getSpectra()):
    if i == n_spectra_to_keep:
        break
    spec.append(s)

exp.setSpectra(spec)
print(f"New size of experiment {len(exp.getSpectra())}")
MzXMLFile().store("test.mzXML", exp)


#
# Take subset of CSV LabView data
#
big_labview_file = "/home/james/Downloads/20200228_TP.csv"
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv(big_labview_file, names=cols)
df["time"] -= df["time"][0]
df = df[: n_spectra_to_keep * 2]


# Ideally we'd keep the header, but by not we show people how to enter the columns
df.to_csv("test.csv", header=False)
