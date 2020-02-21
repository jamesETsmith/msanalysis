import numpy as np
import pytest
from msanalysis.data_processing import (
    calculate_abundance,
    deconvolute_spectrum,
    embed_spectrum,
    find_ms_peaks,
)

npt = np.testing

#
# Helper functions
#


def gauss_conv(x, A, x0, noise=True):
    y = np.zeros_like(x)
    for A_i, x0_i in zip(A, x0):
        y += A_i * np.exp(-0.5 * ((x - x0_i) / 0.1) ** 2)
    if noise:
        y += np.random.rand(x.size) * 0.02
    return y


#
# Tests
#
# fmt: off
case1 = ("MoF2HCl2",[200.8491468319,202.8558565075,203.8592113453,204.8625661831,205.86592102089998,206.86927585869998,208.87598553429999])

# fmt: on
@pytest.mark.parametrize("mol_formula, ans_peaks", [case1])
def test_find_ms_peaks(mol_formula, ans_peaks):

    d = calculate_abundance(mol_formula)
    x = np.linspace(np.min(d["mz"]) * 0.95, np.max(d["mz"]) * 1.05, num=1000)
    y = gauss_conv(x, d["intensity"], d["mz"], noise=False)

    nw = find_ms_peaks({"mz": x, "intensity": y}, prominence=0.05)

    err = np.linalg.norm(nw["mz"] - ans_peaks)
    npt.assert_equal(err < 0.1, True)


def test_embed_spectrum():
    N = 10
    d = {}
    d["mz"] = np.linspace(0, 10, num=N)
    d["intensity"] = np.arange(N) * 100

    extra_mz = np.array([1.334, 3.71])
    new_mz = np.concatenate((d["mz"], extra_mz))
    nd = embed_spectrum(d, new_mz)

    # Check output types/sizes
    npt.assert_equal(type(nd["mz"]), np.ndarray)
    npt.assert_equal(type(nd["intensity"]), np.ndarray)
    npt.assert_equal(nd["intensity"].shape, (N + extra_mz.size,))

    # Check that the length has changed
    npt.assert_equal(nd["mz"].size, N + 2)

    # Check new intensities
    npt.assert_equal(nd["intensity"][np.argwhere(nd["mz"] == extra_mz[0])[0, 0]], 0)
    npt.assert_equal(nd["intensity"][np.argwhere(nd["mz"] == extra_mz[1])[0, 0]], 0)


@pytest.mark.parametrize(
    "species, ratio",
    [
        (["ZrF2Cl2", "ZrCl3"], [3.5, 2.0]),
        (["MoF2Cl2", "MoCl3", "MoOFCl2"], [1.5, 2.5, 4.7]),
        (["MoF2Cl2", "MoOFCl2"], [1.5, 4.7]),
        (["CO", "CN", "B2H", "O2"], [20, 40, 37, 12]),
        (["CO", "CN"], [17, 41]),
    ],
)
def test_deconvolute_spectrum(species, ratio):

    data = [calculate_abundance(sp) for sp in species]
    x = np.linspace(
        np.min([np.min(d["mz"]) for d in data]) * 0.95,
        np.max([np.max(d["mz"]) for d in data]) * 1.05,
        num=2000,
    )
    y = [gauss_conv(x, d["intensity"], d["mz"], noise=False) for d in data]

    scan = {}
    scan["mz"] = x
    scan["intensity"] = np.zeros_like(x)
    for i, r in enumerate(ratio):
        scan["intensity"] += y[i] * r

    calc_ratio, species_spectra = deconvolute_spectrum(scan, species)

    # Check Ratios
    print(ratio / np.max(ratio), calc_ratio)
    npt.assert_almost_equal(ratio / np.max(ratio), calc_ratio, decimal=2)
    # npt.assert_approx_equal(ratio / np.max(ratio), calc_ratio, significant=2)

    # Check reconstructed spectra
    y_final = np.zeros_like(x)
    for sp in species_spectra:
        intensity = sp["intensity"]
        mz = sp["mz"]
        y_final += gauss_conv(x, intensity, mz, noise=False)
    err_norm = np.linalg.norm(scan["intensity"] - y_final)
    # npt.assert_equal(err_norm < 5, True)
    # npt.assert_almost_equal(scan["intensity"], y_final, decimal=2)
    # npt.assert_approx_equal(scan["intensity"], y_final, significant=2)

