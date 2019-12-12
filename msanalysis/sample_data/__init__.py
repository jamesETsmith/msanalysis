"""
Directory for sample data sets and simple utilities to load them.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import os

dir_path = os.path.dirname(os.path.abspath(__file__))


def get_cdf_sample_path():
    return os.path.join(dir_path, "ms_data.cdf")


def get_labview_sample_path():
    return os.path.join(dir_path, "labview_data.csv")
