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

