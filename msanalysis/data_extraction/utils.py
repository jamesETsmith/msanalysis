"""
Utilities for extracting data mostly from CDF files.
"""
import time
import os

import numpy as np
from numba import jit
import netCDF4


def read_cdf(filename: str):
    """Reads a MS CDF file and extracts the spectra.
    
    Parameters
    ----------
    filename : str
        Path to CDF data file.
    
    Returns
    -------
    tuple
        (acq_times, spectra) where acq_times is an `np.ndarray` and spectra is a list
        of dictionaries containing the m/z and intensity for each scan.


    Raises
    ------
    AssertionError
        If the size of acquisition times array and number of spectra don't match.
    """

    # Read in CDF Data
    f = netCDF4.Dataset(filename)

    intensity = np.array(f.variables["intensity_values"])
    mass = np.array(f.variables["mass_values"])
    scan_index = np.array(f.variables["scan_index"])
    acq_times = np.array(
        f.variables["scan_acquisition_time"][:]
        - f.variables["scan_acquisition_time"][0]
    )  # Shift so the time for the first scan is 0

    n_scans = f.variables["actual_scan_number"].shape[0]
    # print(f.variables.keys())

    spectra = []
    for i, _ in enumerate(scan_index):

        # A little bit of index juggling here because the data only keeps the intensity for the
        # exact MZ ratio rather than the rounded one
        start = scan_index[i]
        if i == len(scan_index) - 1:
            final_index = intensity.size - 1
        else:
            final_index = scan_index[i + 1]
        end = start + (final_index - scan_index[i]) // 2

        spectra_i = {"mz": mass[start:end], "intensity": intensity[start:end]}
        spectra.append(spectra_i)

    # Check that our data is same size
    if len(spectra) != acq_times.size:
        print("# spectra =", len(spectra))
        print("# of times =", acq_times.size)
        raise AssertionError(
            "The length of the time data and number of spectra didn't match."
        )

    # Check that we have the same number os scans as indicated in the CDF
    if len(spectra) != n_scans:
        print("# spectra =", len(spectra))
        print("n_scans from CDF =", n_scans)
        raise AssertionError(
            "Number of scans indicated by CDF doesn't match number of spectra found."
        )
    return (acq_times, spectra)


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


# From:
# https://github.com/scipy/scipy-cookbook/blob/master/ipython/SignalSmooth.ipynb
# def smooth(x, window_len=11, window="flat"):
#     """smooth the data using a window with requested size.

#     This method is based on the convolution of a scaled window with the signal.
#     The signal is prepared by introducing reflected copies of the signal
#     (with the window size) in both ends so that transient parts are minimized
#     in the begining and end part of the output signal.

#     input:
#         x: the input signal
#         window_len: the dimension of the smoothing window; should be an odd integer
#         window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
#             flat window will produce a moving average smoothing.

#     output:
#         the smoothed signal

#     example:

#     t=linspace(-2,2,0.1)
#     x=sin(t)+randn(len(t))*0.1
#     y=smooth(x)

#     see also:

#     numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
#     scipy.signal.lfilter

#     TODO: the window parameter could be the window itself if an array instead of a string
#     NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
#     """

#     if x.ndim != 1:
#         raise ValueError("smooth only accepts 1 dimension arrays.")

#     if x.size < window_len:
#         raise ValueError("Input vector needs to be bigger than window size.")

#     if window_len < 3:
#         return x

#     if not window in ["flat", "hanning", "hamming", "bartlett", "blackman"]:
#         raise ValueError(
#             "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
#         )

#     s = np.r_[x[window_len - 1 : 0 : -1], x, x[-2 : -window_len - 1 : -1]]
#     # print(len(s))
#     if window == "flat":  # moving average
#         w = np.ones(window_len, "d")
#     else:
#         w = eval("np." + window + "(window_len)")

#     y = np.convolve(w / w.sum(), s, mode="valid")
#     return y

