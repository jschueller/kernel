"""Append salome prefix to sys.path."""
import sys
from pathlib import Path

SALOME_PREFIX = "salome"
sys.path.append(f"{Path(__file__).parent / SALOME_PREFIX}")
