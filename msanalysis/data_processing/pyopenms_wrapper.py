import numpy as np
from pyopenms import EmpiricalFormula, CoarseIsotopePatternGenerator


def calculate_abundance(mol_formula: str) -> dict:

    if not isinstance(mol_formula, str):
        raise ValueError("mol_formula must be a string")

    # TODO add check that n_isotopes is enough
    n_isotopes = 20
    data_dict = {}

    wm = EmpiricalFormula(mol_formula)
    isotopes = wm.getIsotopeDistribution(CoarseIsotopePatternGenerator(n_isotopes))
    for iso in isotopes.getContainer():
        print(iso.getMZ(), ":", iso.getIntensity())

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
