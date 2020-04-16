msanalysis
==============================
[//]: # (Badges)
[![Build Status](https://travis-ci.com/jamesETsmith/MSAnalysis.svg?branch=master)](https://travis-ci.com/jamesETsmith/MSAnalysis) [![codecov](https://codecov.io/gh/jamesETsmith/msanalysis/branch/master/graph/badge.svg)](https://codecov.io/gh/jamesETsmith/msanalysis)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/631fe5fec12f40c68a5336645e2ef56f)](https://app.codacy.com/manual/jamesETsmith/msanalysis?utm_source=github.com&utm_medium=referral&utm_content=jamesETsmith/msanalysis&utm_campaign=Badge_Grade_Dashboard)

`msanalysis` is a lightweight python package to read and process mass spectra, specifically those in the CDF format.


---
## Python Package Dependencies

- [pytest-cov](https://docs.pytest.org/en/latest/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [pandas](https://pandas.pydata.org/)
- [pyopenms](https://pyopenms.readthedocs.io/en/latest/)
- [black](https://black.readthedocs.io/en/stable/) (only required for contributors)


---
## Installation

Set up is meant to be easy! First we suggest installing all of prerequisites in a clean conda env (run this inside the main directory of the package):

```bash
conda env create -f devtools/conda-envs/msanalysis_env.yaml
```

Then install using pip and we're done!

```bash
python -m pip install -e .
```

If you aren't doing this in a conda env and don't have root user privileges use:

```bash
python -m pip install -e . --user
```

### Fresh install

```bash
git clone https://github.com/jamesETsmith/msanalysis.git
cd msanalysis
conda env create -f devtools/conda-envs/msanalysis_env.yaml
python -m pip install -e .
cd patches
python add_elements.py
```

### Patches

Currently there is one patch while we wait to hear back on an issue from `PyOpenMS`.
If you want to work with species like Indium, run the python script to patch up `msanalysis`.

```bash
cd patches
python add_elements.py
```

---
## Testing

To check that everything is working, run the following from the main project directory:

```bash
pytest -v msanalysis --cov=msanalysis
```

---
### Copyright

Copyright (c) 2019, James E. T. Smith/ CU Boulder


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
