"""
Plotting wrappers for common data visualization.
"""
import numpy as np


def select_mz_range(lb: float, ub: float, m: np.ndarray, i: np.ndarray):
    """
    Takes a subset of mz and intensity arrays (for a single scan) based 
    on upper and lower bonds for M/Z.
        
    Parameters
    ----------
    lb : float
        Lower bound in M/Z units.
    ub : float
        Upper bound in M/Z units.
    m : np.ndarray
        Array of M/Z data for the scan.
    i : np.ndarray
        Array of inensity data for the scan.
    
    Returns
    -------
    tuple
        (np.ndarray, np.ndarray) of the subset of m/z and intensity data.
    """

    indices = np.where((m > lb) & (m < ub))
    return (m[indices], i[indices])
