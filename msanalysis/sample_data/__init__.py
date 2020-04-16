"""
Directory for sample data sets and simple utilities to load them.

Author: James E. T. Smith <james.smith9113@gmail.com>
Date: 12/12/19
"""

import os

dir_path = os.path.dirname(os.path.abspath(__file__))


def get_txt_sample_path():
    return os.path.join(dir_path, "TiCl4_SnF4.txt")


def get_mzXML_sample_path():
    return os.path.join(dir_path, "test.mzXML")


def get_csv_sample_path():
    return os.path.join(dir_path, "test.csv")
