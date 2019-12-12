"""
Unit and regression test for the msanalysis package.
"""

# Import package, test suite, and other packages as needed
import msanalysis
import pytest
import sys

def test_msanalysis_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "msanalysis" in sys.modules
