import pytest
import numpy as np

from msanalysis.data_processing import calculate_abundance

npt = np.testing


@pytest.mark.parametrize(
    "mol_formula, ans",
    # fmt: off
    [ 
        ("AlF3", {"mz": [83.97674829], "intensity": [1.0]}),
        ("AlCl3", {"mz": [131.88809666999998,133.8948063456 , 135.9015160212, 137.90822569679997 ], "intensity": [0.4348303973674774, 0.4173820912837982, 0.13354463875293732, 0.01424288097769022]})
    ],
    # fmt: on
)
def test_abundance(mol_formula, ans):

    data = calculate_abundance(mol_formula)

    # Make sure our output data structure has all the parts we want
    npt.assert_equal(True, "mz" in data.keys())
    npt.assert_equal(True, "intensity" in data.keys())

    # Make sure the MZ and Intensity are correct
    npt.assert_equal(ans["mz"], data["mz"])
    npt.assert_equal(ans["intensity"], data["intensity"])
