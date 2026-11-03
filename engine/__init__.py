"""
OmniConvert Engine Package
Core mathematical definitions and unit transformation algorithms.
"""
from .converter import (
    UnitCategory,
    ConversionResult,
    convert,
    get_categories,
    get_units_for_category,
    get_all_units_flat,
    find_unit_category
)

__all__ = [
    "UnitCategory",
    "ConversionResult",
    "convert",
    "get_categories",
    "get_units_for_category",
    "get_all_units_flat",
    "find_unit_category"
]
