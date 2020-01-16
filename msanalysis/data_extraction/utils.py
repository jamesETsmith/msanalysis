"""
Utilities for extracting data mostly from CDF files.
"""
import numpy as np

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

