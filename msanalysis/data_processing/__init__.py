import numpy as np
from .pyopenms_wrapper import calculate_abundance
from .pyopenms_wrapper import filter_spectrum
from .peak_detection import find_ms_peaks
from .peak_detection import deconvolute_spectrum
from .peak_detection import embed_spectrum


def get_relative_abundance(
    spectra: list, species_mz: list, bin_width: float = 0.45
) -> np.ndarray:
    """Return `np.ndarray` of abundances of the MZs specified
    
    Parameters
    ----------
    spectra : list
        List of spectra where each spectrum, call is data has two keys: data["mz"]
        is an array of the mass/charge ratios and data["intensity"] is an array of
        the intensities.
    species_mz : list
        List of MZs of interest.
    bin_width : float, optional
        How far around the species_mz to collect intensities, by default 0.45
    
    Returns
    -------
    np.ndarray
        2D array (nspecies, nspectra). Abundances of species for all spectra given.
    """

    abundances = []

    for sp_i in spectra:
        mz = sp_i["mz"]
        I = sp_i["intensity"]

        I_j = np.zeros(
            len(species_mz)
        )  # Intensities of each species_mz in spectra sp_i

        # For each species_mz of interest, bin and add the intensities
        for j, species_mz_j in enumerate(species_mz):
            ub = species_mz_j + bin_width
            lb = species_mz_j - bin_width
            indices = np.where((mz > lb) & (mz < ub))
            I_j[j] = np.sum(I[indices])

        abundances.append(I_j)

    return np.array(abundances).T
