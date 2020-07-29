"""
Utilities for extracting data mostly from CDF files.
"""
import time
import os

import numpy as np
from pyopenms import MSExperiment, MzXMLFile


def convert_lines_to_np_array(lines: list, n_scans: int, scan_size: int):
    intensities = np.zeros((n_scans, scan_size))
    mz = np.zeros(scan_size)

    li = 1

    # Kept separate for speed to avoid
    for j in range(scan_size):
        mz[j] = float(lines[li].rsplit()[0])
        intensities[0, j] = float(lines[li].rsplit()[1])
        li += 1

    for i in range(1, n_scans):
        li += 1
        for j in range(scan_size):
            intensities[i, j] = float(lines[li].rsplit()[1])
            li += 1

    return mz, intensities


def read_exported_txt(filename: str, pts_per_amu=27, overwrite=False) -> tuple:
    """Reads the large text files exported by the merlin software and returns NumPy objects.

    Since the files can be large (> 1GB) and reading text files is slow, a binary version
    of the data is saved after the text file is parsed. If the function finds a binary
    file (look for .npz) extension, it will skip parsing the data from the text file and
    load it directly from the binary. This is typically one to two orders of magnitude faster.


    Parameters
    ----------
    filename : str
        The path to the txt datafile. This path is also used when saving
        the data in binary data. E.g. if filename is /path/to/file.txt the
        data will be saved as /path/to/file.npz for faster loading if the user
        wants to load it again.
    pts_per_amu: int, optional
        The number of points per mz unit, by default 27
    overwrite: bool, optional
        Whether to overwrite the compressed data (the npz file).

    Returns
    -------
    (np.ndarray, np.ndarray)
        A tuple where the first element is an array of the MZ values and
        the second are the intensities. The shape of intensities is
        (n_scans, scan_size).

    Raises
    ------
    AssertionError
        Raises assertion error if any incomplete scans are found.

    Examples
    --------
    >>> from msanalysis.data_extraction import read_exported_txt
    >>> from msanalysis.sample_data import get_txt_sample_path
    >>> mz, ints  = read_exported_txt(get_txt_sample_path())
    Time to read data from npz file 0.0083160400390625
    >>> mz, ints  = read_exported_txt(get_txt_sample_path())
    Time to read file: 0.008026361465454102
    Time to convert lines to np.array 0.032723188400268555
    Saving compressed binary version of data at /home/james/Insync/jasm3285@colorado.edu/Google Drive/research/projects/msanalysis/msanalysis/sample_data/TiCl4_SnF4.npz
    >>> _  = read_exported_txt(get_txt_sample_path())
    Time to read data from npz file 0.002399921417236328

    """

    npy_filename = filename[:-4] + ".npz"

    if os.path.exists(npy_filename) and overwrite == False:
        t0 = time.time()
        npzfile = np.load(npy_filename)
        mz, intensities = (npzfile["mz"], npzfile["intensities"])
        print(f"Time to read data from npz file {time.time()-t0}")
        return mz, intensities
    else:

        t0 = time.time()
        with open(filename, "r") as f:
            lines = f.readlines()
        t1 = time.time()
        print(f"Time to read file: {t1-t0}")

        scan_range = 1000 - 2
        scan_size = scan_range * pts_per_amu + 1
        n_scans = int(len(lines) / (scan_size + 1))
        if len(lines) % (scan_size + 1) != 0:
            raise AssertionError(f"Incomplete scans were found please check {filename}")

        t0 = time.time()
        mz, intensities = convert_lines_to_np_array(lines, n_scans, scan_size)
        print(f"Time to convert lines to np.array {time.time()-t0}")
        print(f"Saving compressed binary version of data at {npy_filename}")
        np.savez(npy_filename, mz=mz, intensities=intensities)
        return mz, intensities


def read_mzXML(filename: str) -> dict:

    exp = MSExperiment()
    t0 = time.time()
    MzXMLFile().load(filename, exp)
    print(f"Time to load mzXML file {time.time()-t0}")

    # Dump List of PyOpenMS::Spectra to one NumPy array for MZ and a 2D array for
    # intensities
    n = len(exp.getSpectra())
    mz = exp.getSpectra()[0].get_peaks()[0]
    n_pt_per_scan = mz.size
    intensities = np.zeros((n, n_pt_per_scan))
    times = np.array([spec.getRT() for spec in exp.getSpectra()])  # Now in seconds
    for i, s in enumerate(exp.getSpectra()):
        peaks = s.get_peaks()[1]
        if peaks.size == 0:
            print(f"Scan {i} (0-based indexing) is empty.")
            raise ValueError(f"One (or more) empty scans in {filename}, exiting!!")
        else:
            intensities[i] = peaks

    return {"mz": mz, "intensities": intensities, "times": times}
