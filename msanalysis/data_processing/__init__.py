import numpy as np
from .pyopenms_wrapper import calculate_abundance
from .pyopenms_wrapper import filter_spectrum
from .peak_detection import find_ms_peaks
from .peak_detection import deconvolute_spectrum
from .peak_detection import embed_spectrum
from .smoothing import moving_average


def get_relative_abundance(
    mz: np.ndarray, intensities: np.ndarray, species_mz: list, bin_width: float = 0.45
) -> np.ndarray:
    """Return `np.ndarray` of abundances of the MZs specified
    
    Parameters
    ----------
    mz : np.ndarray
        1D `np.ndarray` holding the mz values for the experiment.
    intensities: np.ndarray
        2D `np.ndarray` where the first axis is the scan number and the second one is
        the m/z axis.
    species_mz : list
        List of MZs of interest.
    bin_width : float, optional
        How far around the species_mz to collect intensities, by default 0.45
    
    Returns
    -------
    np.ndarray
        2D array (nspecies, nspectra). Abundances of species for all spectra given.
    """

    abundances = np.zeros((len(species_mz), intensities.shape[0]))

    # For each species_mz of interest, bin and add the intensities
    for i, species_mz_i in enumerate(species_mz):
        ub = species_mz_i + bin_width
        lb = species_mz_i - bin_width
        indices = np.where((mz > lb) & (mz < ub))
        abundances[i] = np.sum(intensities[:, indices[0]], axis=1)

    return abundances
