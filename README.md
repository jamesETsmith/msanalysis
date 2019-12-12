msanalysis
==============================
[//]: # (Badges)
[![Build Status](https://travis-ci.com/jamesETsmith/MSAnalysis.svg?branch=master)](https://travis-ci.com/jamesETsmith/MSAnalysis) [![codecov](https://codecov.io/gh/jamesETsmith/msanalysis/branch/master/graph/badge.svg)](https://codecov.io/gh/jamesETsmith/msanalysis)
<!-- [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true)](https://ci.appveyor.com/project/REPLACE_WITH_OWNER_ACCOUNT/msanalysis/branch/master) -->

`msanalysis` is a lightweight python package to read and process mass spectra, specifically those in the CDF format.


---
## Python Package Dependencies

- pytest
- pytest-cov
- codecov
- matplotlib
- seaborn
- netcdf4
- numpy
- scipy
- pandas
- black (only required for contributors)


---
## Installation

Set up is meant to be easy! First we suggest installing all of prerequisites in a clean conda env:

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


---
### Copyright

Copyright (c) 2019, James E. T. Smith/ CU Boulder


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
