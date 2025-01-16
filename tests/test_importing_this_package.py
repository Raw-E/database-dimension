"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for test_importing_this_package.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
import importlib
from importlib.util import find_spec

# Third-Party Imports
import pytest


# Main Functions
def test_importing_this_package():
    spec = find_spec("database_dimension")
    assert spec is not None, "Package 'database_dimension' not found!"

    try:
        importlib.import_module("database_dimension")
    except ImportError as e:
        pytest.fail(f"Failed to import 'database_dimension' package: {e}")
