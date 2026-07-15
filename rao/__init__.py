"""Compatibility package for running this checkout as ``rao``.

The original sources import modules as ``rao.*``.  This repository may be
checked out under another directory name, so this package points Python's
submodule lookup at the repository root.
"""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent)]
