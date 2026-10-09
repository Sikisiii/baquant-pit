"""Bootstrap packaging validation; no PIT implementation is exercised."""

from importlib.metadata import version

import baquant_pit


def test_package_import_and_version():
    assert baquant_pit.__version__ == "0.1.0"
    assert version("baquant-pit") == baquant_pit.__version__
