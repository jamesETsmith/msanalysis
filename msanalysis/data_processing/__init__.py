import numpy as np
from .pyopenms_wrapper import calculate_abundance


def get_relative_abundance(spectra: list, species: list, bin_width: float = 0.45):

    abundances = []

    for sp_i in spectra:
        mz = sp_i["mz"]
        I = sp_i["intensity"]

        I_j = np.zeros(len(species))  # Intensities of each species in spectra sp_i

        # For each species of interest, bin and add the intensities
        for j, species_j in enumerate(species):
            ub = species_j + bin_width
            lb = species_j - bin_width
            indices = np.where((mz > lb) & (mz < ub))
            I_j[j] = np.sum(I[indices])

        abundances.append(I_j)

    return np.array(abundances)
