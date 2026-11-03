"""
OmniConvert AI - Main Application Entrypoint
Universal launcher for unit_converter.py
"""
import runpy
from pathlib import Path

target = Path(__file__).parent / "unit_converter.py"
runpy.run_path(str(target), run_name="__main__")
