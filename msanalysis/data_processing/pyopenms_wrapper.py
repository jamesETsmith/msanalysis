import numpy as np
from pyopenms import EmpiricalFormula, CoarseIsotopePatternGenerator
from pyopenms import MSSpectrum, MSExperiment, SavitzkyGolayFilter


def calculate_abundance(mol_formula: str) -> dict:
    """Calculate the isotopic abundance spectra for a give molecular formula.
    
    Parameters
    ----------
    mol_formula : str
        The molecular formula, e.g. "AlF3".
    
    Returns
    -------
    dict
        Where data["mz"] is an array of the mass/charge ratios and 
        data["intensity"] is an array of the intensities.
    
    Raises
    ------
    ValueError
        If input isn't a string.
    """

    if not isinstance(mol_formula, str):
        raise ValueError("mol_formula must be a string")

    # TODO add check that n_isotopes is enough
    n_isotopes = 20
    data_dict = {}

    wm = EmpiricalFormula(mol_formula)
    isotopes = wm.getIsotopeDistribution(CoarseIsotopePatternGenerator(n_isotopes))
    print("\nIsotopes for {}".format(mol_formula))
    for iso in isotopes.getContainer():
        print(iso.getMZ(), ":", iso.getIntensity())
    print()

    data_dict["mz"] = np.array([iso.getMZ() for iso in isotopes.getContainer()])
    data_dict["intensity"] = np.array(
        [iso.getIntensity() for iso in isotopes.getContainer()]
    )

    # Get rid of intensities = 0
    data_dict["mz"] = data_dict["mz"][np.argwhere(data_dict["intensity"] > 0)][:, 0]
    data_dict["intensity"] = data_dict["intensity"][
        np.argwhere(data_dict["intensity"] > 0)
    ][:, 0]

    return data_dict


def filter_spectrum(data_dict: dict, filtertype: str = "SavitzkyGolay") -> dict:

    # Convert to MSExperiment
    expt = MSExperiment()
    spectrum = MSSpectrum()
    spectrum.set_peaks([data_dict["mz"], data_dict["intensity"]])
    expt.addSpectrum(spectrum)

    # Apply filter
    filter = None
    if filtertype == "SavitzkyGolay":
        filter = SavitzkyGolayFilter()
    else:
        raise AssertionError("Filter type {} not implemented yet!".format(filtertype))

    filter.filterExperiment(expt)

    new_data_dict = {}
    new_data_dict["mz"] = [peak.getMZ() for peak in expt[0]]
    new_data_dict["intensity"] = [peak.getIntensity() for peak in expt[0]]
    return new_data_dict
