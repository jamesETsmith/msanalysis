import warnings
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import nnls
from msanalysis.data_processing import calculate_abundance


def find_ms_peaks(data_dict: dict, **kwargs) -> dict:
    """Find mass spec peaks for a given spectra using using the SciPy `find_peaks`
    function.
    
    Parameters
    ----------
    data_dict : dict
        The real spectrum, where data["mz"] is an array of the mass/charge ratios
        and data["intensity"] is an array of the intensities.
    
    Returns
    -------
    dict
        The stick spectrum for the found peaks, where data["mz"] is an array of
        the mass/charge ratios and data["intensity"] is an array of the intensities.
    """

    peak_idx, _ = find_peaks(data_dict["intensity"], **kwargs)
    new_data_dict = {}
    new_data_dict["intensity"] = data_dict["intensity"][peak_idx]
    new_data_dict["mz"] = data_dict["mz"][peak_idx]
    return new_data_dict


def embed_spectrum(data_dict: dict, new_mz: np.ndarray) -> dict:
    new_data_dict = {}
    new_data_dict["mz"] = new_mz
    new_data_dict["intensity"] = []
    for i, mz in enumerate(new_mz):
        if mz in data_dict["mz"]:
            idx = np.argwhere(mz == data_dict["mz"])
            # print(data_dict["intensity"][idx][0, 0])
            new_data_dict["intensity"].append(data_dict["intensity"][idx][0, 0])
        else:
            new_data_dict["intensity"].append(0)

    new_data_dict["intensity"] = np.array(new_data_dict["intensity"])
    return new_data_dict


def deconvolute_spectrum(
    data_dict: dict, species: list, decimals: int = 0, return_embedded: bool = False
) -> (np.ndarray, list):
    """Disentangle spectrum in `data_dict` given that the chemical species in the list
    `species` are the only systems present in the current mass window.
    
    Parameters
    ----------
    data_dict : dict        
        The spectrum, where data["mz"] is an array of the mass/charge ratios
        and data["intensity"] is an array of the intensities.
    species : list
        A list of strings where each element is the chemical formula for a species
        present in the mass window. E.g.  ["AlF3", "AlOF2"].
    decimals : int, optional
        Species how decimals the ideal m/z for each species must match, by default 1
    return_embedded: bool, optional
        Return the scalled embedded spectra, mostly so you can stack the bar plots,
        by default `False`.
    
    Returns
    -------
    `np.ndarray`
        A list of the population ratios for each species normalized to the largest
        value.
    list
        A list of dictionaries where each element is a spectrum, where data["mz"] is
        an array of the mass/charge ratios and data["intensity"] is an array of the
        intensities.
    """
    # warnings.filterwarnings("ignore")  # some numpy decprecation warnings are raised

    # Round all m/z as soon as we see them
    species_spectra = [calculate_abundance(sp) for sp in species]
    for sp in species_spectra:
        sp["mz"] = np.round(sp["mz"], decimals=decimals)

    # Create intersection of mzs
    all_mz = species_spectra[0]["mz"]
    for i, sp in enumerate(species_spectra):
        if i == 0:
            continue
        all_mz = np.concatenate((all_mz, sp["mz"]))
    # all_mz = np.round(all_mz, decimals=decimals)
    unique_mz = np.unique(all_mz)

    # print(all_mz)
    print("Unique MZ")
    print(unique_mz)

    # Get peaks from spectra that are in our predicted abundance
    b_data = find_ms_peaks(data_dict, prominence=0.05)
    b_data["mz"] = np.round(b_data["mz"], decimals=decimals)
    print(b_data["mz"])
    b_idx = [i for i, mz in enumerate(b_data["mz"]) if mz in unique_mz]
    mz_b = b_data["mz"][b_idx]
    b = b_data["intensity"][b_idx]

    # Embed isotopic spectra in full set spectrum of mz
    e_spectra = [embed_spectrum(sp, mz_b) for sp in species_spectra]

    print("\nPeaks from given spectra")
    print(mz_b)
    # print(b_idx)

    # Get subset of unique mz in in b_data
    A = np.zeros((b.shape[0], len(species)))
    for i, sp in enumerate(e_spectra):
        A[:, i] = sp["intensity"]

    # Solve linear problem using non-negative least squares
    print("\nCoefficient Matrix A:")
    print(A)
    print("\nCondition Number of A {:.3f}".format(np.linalg.cond(A)))
    if np.linalg.cond(A) > 1000:
        warnings.warn("The coefficient matrix is ill-conditioned!!" "Check the ")
    x, R = nnls(A, b, maxiter=1000)

    x_norm = x / x.max()  # Normatlized to the largest value
    print("\nRatio of species\n================")
    for i, sp in enumerate(species):
        print(
            "Spcecies: {:18s}  Relative ratio: {:.3f}  Abs. ratio {:.3f}".format(
                sp, x_norm[i], x[i]
            )
        )
    print("\nError residual from fitting {:.4f}".format(R))

    # If any of the coefficients are 0, there are two possibilies
    # 1) That species wasn't in the mass window
    # 2) No peaks from that species were found in the spectrum
    if (x == 0).any():
        idx = np.argwhere(x == 0)
        for i in idx:
            i = i[0]
            print(
                "\nERROR: Species {} has a linear coefficient of 0".format(species[i])
            )
            print("This could mean one of two things:")
            print("1) That species wasn't in the mass window. Or")
            print("2) No peaks from that species were found in the spectrum\n")
            raise AssertionError

    # Scale abundances so their sum matches the realistic spectras
    if return_embedded:  # return scaled embedded spectra if requested
        species_spectra = e_spectra
    for i, sp in enumerate(species_spectra):
        sp["intensity"] *= x[i]
    return x_norm, species_spectra
