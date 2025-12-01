"""Test configuration for local package imports."""

from pathlib import Path
import sys


# Ensure the project root (containing the `mortgage_oop` package) is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)
