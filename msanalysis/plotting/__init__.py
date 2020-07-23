"""
Plotting wrappers for common data visualization.
"""
import matplotlib.pyplot as plt
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


#
# Convenience Function
#
def add_custom_ticks(ax: plt.Axes, tick_interp: np.ndarray):
    # I'm playing some tricks here, and just relabeling the ticks on the x-axis
    xticks = np.array(ax.get_xticks(), dtype=np.int)

    # This catch is necessary because sometimes the last tick is out of bonds for our
    # interpreted temp data
    if xticks[-1] > tick_interp[-1].size:
        xticks = xticks[:-1]
    ax.set_xticklabels(["{:.0f}".format(t) for t in tick_interp[xticks]])
