from pyopenms import MSExperiment, MzXMLFile
import pandas as pd

labview_file = "/home/james/Downloads/20200124_TP_2.csv"
mzXML_file = "/home/james/Downloads/20200124_17645.mzXML"

#
# Make smaller mzXML file to keep in repo
#
n_spectra_to_keep = 20

exp = MSExperiment()
MzXMLFile().load(mzXML_file, exp)
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
cols = ["time", "b", "temp", "d", "e", "f", "g", "h"]
df = pd.read_csv(labview_file, names=cols)
df["time"] -= df["time"][0]
df = df[: n_spectra_to_keep * 2 + 2]


# Ideally we'd keep the header, but by not we show people how to enter the columns
df.to_csv("test.csv", header=False)
