import pytest
import numpy as np

from msanalysis.data_processing import calculate_abundance

npt = np.testing


@pytest.mark.parametrize(
    "mol_formula, ans",
    # fmt: off
    [ 
        ("AlF3", {"mz": [83.97674829], "intensity": [1.0]}),
        ("AlCl3", {"mz": [131.88809666999998,133.8948063456 , 135.9015160212, 137.90822569679997 ], "intensity": [0.4348303973674774, 0.4173820912837982, 0.13354463875293732, 0.01424288097769022]}),
        ("Sn2C5H15", { "mz":[ 300.93, 302.94, 303.94, 304.95, 305.95, 306.95, 307.96, 308.96, 309.96, 310.97, 311.97, 312.97, 313.98, 314.98, 315.98, 316.99, 317.99, 318.99, 320.00, 321.00, 322.00, 323.01, 324.01], "intensity":[ 0.0001, 0.0027, 0.0016, 0.0064, 0.0038, 0.0297, 0.0254, 0.0790, 0.0653, 0.1627, 0.0960, 0.1748, 0.0696, 0.1411, 0.0237, 0.0561, 0.0125, 0.0383, 0.0021, 0.0051, 0.0003, 0.0032, 0.0002]}),
    ],
    # fmt: on
)
def test_abundance(mol_formula, ans):

    data = calculate_abundance(mol_formula)

    # Make sure our output data structure has all the parts we want
    npt.assert_equal(True, "mz" in data.keys())
    npt.assert_equal(True, "intensity" in data.keys())

    # Make sure the MZ and Intensity are correct
    npt.assert_equal(np.round(ans["mz"], decimals=2), np.round(data["mz"], decimals=2))
    npt.assert_equal(
        np.round(ans["intensity"], decimals=2), np.round(data["intensity"], decimals=2)
    )
    npt.assert_equal(data["intensity"].size, np.argwhere(data["intensity"] > 1e-4).size)

    new_tol = 1e-5
    data2 = calculate_abundance(mol_formula, tol=new_tol)
    npt.assert_equal(
        data2["intensity"].size, np.argwhere(data2["intensity"] > new_tol).size
    )

