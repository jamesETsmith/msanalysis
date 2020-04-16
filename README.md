msanalysis
==============================
[//]: # (Badges)
|  OS   |                                                           Build Status                                                            |
| :---: | :-------------------------------------------------------------------------------------------------------------------------------: |
| Linux | [![Build Status](https://travis-ci.com/jamesETsmith/MSAnalysis.svg?branch=master)](https://travis-ci.com/jamesETsmith/MSAnalysis) |
|  OSX  | [![Build Status](https://travis-ci.com/jamesETsmith/MSAnalysis.svg?branch=master)](https://travis-ci.com/jamesETsmith/MSAnalysis) |

Python Versions Tested (other versions may work):
|  OS   |        3.5         |        3.6         |        3.7         |        3.8         |
| :---: | :----------------: | :----------------: | :----------------: | :----------------: |
| Linux | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
|  OSX  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |        :x:         |

<!-- |  |                                                              Windows                                                              | [![Build status](https://ci.appveyor.com/api/projects/status/onphhkq4828e2jiv/branch/master?svg=true)](https://ci.appveyor.com/project/jamesETsmith/msanalysis/branch/master) | | -->

[![codecov](https://codecov.io/gh/jamesETsmith/msanalysis/branch/master/graph/badge.svg)](https://codecov.io/gh/jamesETsmith/msanalysis)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/631fe5fec12f40c68a5336645e2ef56f)](https://app.codacy.com/manual/jamesETsmith/msanalysis?utm_source=github.com&utm_medium=referral&utm_content=jamesETsmith/msanalysis&utm_campaign=Badge_Grade_Dashboard)
<!-- [![Maintainability](https://api.codeclimate.com/v1/badges/2163494ecded7e51bb0d/maintainability)](https://codeclimate.com/github/jamesETsmith/msanalysis/maintainability) -->

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
