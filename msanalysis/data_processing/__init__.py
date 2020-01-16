import numpy as np


def get_relative_abundance(spectra: list, species: list, bin_width: float = 0.45):

    abundances = []

    for sp_i in spectra:
        mz = sp_i["mz"]
        I = sp_i["intensity"]

        I_j = np.zeros(len(species))  # Intensities of each species in spectra sp_i

        # For each species of interest, bin and add the intensities
        for j, species_j in enumerate(species):
            indices = np.where(
                (mz > species_j - bin_width) & (mz < species_j - bin_width)
            )

            I_j[j] = np.sum(I[indices])

        abundances.append(I_j)

    return np.array(abundances)
