"""
OmniConvert AI - Mathematical Conversion Engine
High-precision, multi-category unit conversion with step-by-step formula generation.
Conforms to NIST SP 811 & ISO 80000 standards.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import math


@dataclass
class UnitMetadata:
    name: str
    symbol: str
    factor_to_base: float  # Multiplier to reach the category's standard base unit
    category: str
    aliases: List[str]
    description: str = ""


@dataclass
class ConversionResult:
    success: bool
    source_value: float
    target_value: float
    source_unit: str
    target_unit: str
    source_symbol: str
    target_symbol: str
    category: str
    formula_latex: str
    step_by_step: str
    error_message: Optional[str] = None


class UnitCategory:
    LENGTH = "Length"
    MASS = "Weight & Mass"
    TEMPERATURE = "Temperature"
    AREA = "Area"
    VOLUME = "Volume"
    SPEED = "Speed"
    TIME = "Time"
    DIGITAL_STORAGE = "Digital Storage"
    ENERGY = "Energy & Work"
    PRESSURE = "Pressure"


CATEGORY_ICONS = {
    UnitCategory.LENGTH: "📏",
    UnitCategory.MASS: "⚖️",
    UnitCategory.TEMPERATURE: "🌡️",
    UnitCategory.AREA: "📐",
    UnitCategory.VOLUME: "🧪",
    UnitCategory.SPEED: "🚀",
    UnitCategory.TIME: "⏱️",
    UnitCategory.DIGITAL_STORAGE: "💾",
    UnitCategory.ENERGY: "⚡",
    UnitCategory.PRESSURE: "🌪️",
}

# Unit definitions mapped by category
# Base units:
# Length: meter (m)
# Mass: kilogram (kg)
# Temperature: Kelvin (K)
# Area: square meter (m²)
# Volume: liter (L)
# Speed: meter per second (m/s)
# Time: second (s)
# Digital Storage: byte (B)
# Energy: joule (J)
# Pressure: pascal (Pa)

UNIT_REGISTRY: Dict[str, Dict[str, UnitMetadata]] = {
    UnitCategory.LENGTH: {
        "meter": UnitMetadata("Meter", "m", 1.0, UnitCategory.LENGTH, ["meter", "meters", "metre", "metres", "m"], "SI base unit of length"),
        "kilometer": UnitMetadata("Kilometer", "km", 1000.0, UnitCategory.LENGTH, ["kilometer", "kilometers", "kilometre", "km"], "1,000 meters"),
        "centimeter": UnitMetadata("Centimeter", "cm", 0.01, UnitCategory.LENGTH, ["centimeter", "centimeters", "centimetre", "cm"], "1/100 of a meter"),
        "millimeter": UnitMetadata("Millimeter", "mm", 0.001, UnitCategory.LENGTH, ["millimeter", "millimeters", "millimetre", "mm"], "1/1,000 of a meter"),
        "micrometer": UnitMetadata("Micrometer", "µm", 1e-6, UnitCategory.LENGTH, ["micrometer", "micrometers", "micron", "um", "µm"], "10⁻⁶ meters"),
        "nanometer": UnitMetadata("Nanometer", "nm", 1e-9, UnitCategory.LENGTH, ["nanometer", "nanometers", "nm"], "10⁻⁹ meters"),
        "mile": UnitMetadata("Mile", "mi", 1609.344, UnitCategory.LENGTH, ["mile", "miles", "mi"], "Statute mile (5,280 feet)"),
        "yard": UnitMetadata("Yard", "yd", 0.9144, UnitCategory.LENGTH, ["yard", "yards", "yd"], "3 feet or 36 inches"),
        "foot": UnitMetadata("Foot", "ft", 0.3048, UnitCategory.LENGTH, ["foot", "feet", "ft", "'"], "12 inches"),
        "inch": UnitMetadata("Inch", "in", 0.0254, UnitCategory.LENGTH, ["inch", "inches", "in", "\""], "1/12 of a foot"),
        "nautical_mile": UnitMetadata("Nautical Mile", "NM", 1852.0, UnitCategory.LENGTH, ["nautical mile", "nautical miles", "nmi", "nm_sea"], "International maritime distance standard"),
    },
    UnitCategory.MASS: {
        "kilogram": UnitMetadata("Kilogram", "kg", 1.0, UnitCategory.MASS, ["kilogram", "kilograms", "kg", "kilos", "kilo"], "SI base unit of mass"),
        "gram": UnitMetadata("Gram", "g", 0.001, UnitCategory.MASS, ["gram", "grams", "g", "gm"], "1/1,000 of a kilogram"),
        "milligram": UnitMetadata("Milligram", "mg", 1e-6, UnitCategory.MASS, ["milligram", "milligrams", "mg"], "1/1,000,000 of a kilogram"),
        "microgram": UnitMetadata("Microgram", "µg", 1e-9, UnitCategory.MASS, ["microgram", "micrograms", "ug", "µg"], "10⁻⁹ kilograms"),
        "metric_ton": UnitMetadata("Metric Ton", "t", 1000.0, UnitCategory.MASS, ["ton", "tonne", "metric ton", "tonnes", "t"], "1,000 kilograms"),
        "pound": UnitMetadata("Pound", "lb", 0.45359237, UnitCategory.MASS, ["pound", "pounds", "lb", "lbs"], "Avoirdupois pound (16 ounces)"),
        "ounce": UnitMetadata("Ounce", "oz", 0.028349523125, UnitCategory.MASS, ["ounce", "ounces", "oz"], "1/16 of a pound"),
        "stone": UnitMetadata("Stone", "st", 6.35029318, UnitCategory.MASS, ["stone", "st"], "British imperial unit (14 pounds)"),
        "carat": UnitMetadata("Carat", "ct", 0.0002, UnitCategory.MASS, ["carat", "carats", "ct"], "Gemological unit (200 milligrams)"),
    },
    UnitCategory.TEMPERATURE: {
        "celsius": UnitMetadata("Celsius", "°C", 1.0, UnitCategory.TEMPERATURE, ["celsius", "centigrade", "c", "deg c", "degree c"], "Centigrade temperature scale"),
        "fahrenheit": UnitMetadata("Fahrenheit", "°F", 1.0, UnitCategory.TEMPERATURE, ["fahrenheit", "f", "deg f", "degree f"], "Imperial temperature scale"),
        "kelvin": UnitMetadata("Kelvin", "K", 1.0, UnitCategory.TEMPERATURE, ["kelvin", "k"], "Absolute thermodynamic temperature scale"),
        "rankine": UnitMetadata("Rankine", "°R", 1.0, UnitCategory.TEMPERATURE, ["rankine", "r", "deg r"], "Absolute Fahrenheit scale"),
    },
    UnitCategory.AREA: {
        "square_meter": UnitMetadata("Square Meter", "m²", 1.0, UnitCategory.AREA, ["square meter", "square meters", "sq m", "m2", "m^2"], "SI base unit of area"),
        "square_kilometer": UnitMetadata("Square Kilometer", "km²", 1e6, UnitCategory.AREA, ["square kilometer", "square kilometers", "sq km", "km2", "km^2"], "1,000,000 square meters"),
        "square_mile": UnitMetadata("Square Mile", "mi²", 2589988.110336, UnitCategory.AREA, ["square mile", "square miles", "sq mi", "mi2", "mi^2"], "640 acres"),
        "square_yard": UnitMetadata("Square Yard", "yd²", 0.83612736, UnitCategory.AREA, ["square yard", "square yards", "sq yd", "yd2"], "9 square feet"),
        "square_foot": UnitMetadata("Square Foot", "ft²", 0.09290304, UnitCategory.AREA, ["square foot", "square feet", "sq ft", "ft2", "ft^2"], "144 square inches"),
        "square_inch": UnitMetadata("Square Inch", "in²", 0.00064516, UnitCategory.AREA, ["square inch", "square inches", "sq in", "in2"], "6.4516 cm²"),
        "hectare": UnitMetadata("Hectare", "ha", 10000.0, UnitCategory.AREA, ["hectare", "hectares", "ha"], "10,000 square meters"),
        "acre": UnitMetadata("Acre", "ac", 4046.8564224, UnitCategory.AREA, ["acre", "acres", "ac"], "43,560 square feet"),
    },
    UnitCategory.VOLUME: {
        "liter": UnitMetadata("Liter", "L", 1.0, UnitCategory.VOLUME, ["liter", "liters", "litre", "litres", "l"], "SI metric volume baseline"),
        "milliliter": UnitMetadata("Milliliter", "mL", 0.001, UnitCategory.VOLUME, ["milliliter", "milliliters", "millilitre", "ml"], "1 cubic centimeter (cc)"),
        "cubic_meter": UnitMetadata("Cubic Meter", "m³", 1000.0, UnitCategory.VOLUME, ["cubic meter", "cubic meters", "m3", "m^3"], "1,000 liters"),
        "gallon_us": UnitMetadata("Gallon (US)", "gal", 3.785411784, UnitCategory.VOLUME, ["gallon", "gallons", "gal", "us gallon"], "US liquid gallon (231 cu in)"),
        "quart_us": UnitMetadata("Quart (US)", "qt", 0.946352946, UnitCategory.VOLUME, ["quart", "quarts", "qt"], "1/4 US gallon"),
        "pint_us": UnitMetadata("Pint (US)", "pt", 0.473176473, UnitCategory.VOLUME, ["pint", "pints", "pt"], "1/8 US gallon or 16 fl oz"),
        "cup_us": UnitMetadata("Cup (US)", "cup", 0.2365882365, UnitCategory.VOLUME, ["cup", "cups"], "8 US fluid ounces"),
        "fluid_ounce_us": UnitMetadata("Fluid Ounce (US)", "fl oz", 0.0295735295625, UnitCategory.VOLUME, ["fluid ounce", "fluid ounces", "fl oz", "floz"], "1/128 US gallon"),
        "tablespoon_us": UnitMetadata("Tablespoon (US)", "tbsp", 0.01478676478125, UnitCategory.VOLUME, ["tablespoon", "tablespoons", "tbsp"], "1/2 US fluid ounce"),
        "teaspoon_us": UnitMetadata("Teaspoon (US)", "tsp", 0.00492892159375, UnitCategory.VOLUME, ["teaspoon", "teaspoons", "tsp"], "1/3 US tablespoon"),
    },
    UnitCategory.SPEED: {
        "meter_per_second": UnitMetadata("Meters per Second", "m/s", 1.0, UnitCategory.SPEED, ["meter per second", "meters per second", "m/s", "mps"], "SI base unit of speed"),
        "kilometer_per_hour": UnitMetadata("Kilometers per Hour", "km/h", 1.0 / 3.6, UnitCategory.SPEED, ["kilometer per hour", "kilometers per hour", "km/h", "kmh", "kph"], "Standard vehicle metric speed"),
        "mile_per_hour": UnitMetadata("Miles per Hour", "mph", 0.44704, UnitCategory.SPEED, ["mile per hour", "miles per hour", "mph"], "US/UK road vehicle standard"),
        "knot": UnitMetadata("Knot", "kn", 1852.0 / 3600.0, UnitCategory.SPEED, ["knot", "knots", "kn", "kt"], "1 nautical mile per hour"),
        "foot_per_second": UnitMetadata("Feet per Second", "ft/s", 0.3048, UnitCategory.SPEED, ["foot per second", "feet per second", "ft/s", "fps"], "Imperial rate of motion"),
        "mach": UnitMetadata("Mach (at STP)", "Ma", 340.29, UnitCategory.SPEED, ["mach", "ma"], "Speed of sound in dry air at 15 °C"),
    },
    UnitCategory.TIME: {
        "second": UnitMetadata("Second", "s", 1.0, UnitCategory.TIME, ["second", "seconds", "sec", "s"], "SI base unit of duration"),
        "millisecond": UnitMetadata("Millisecond", "ms", 0.001, UnitCategory.TIME, ["millisecond", "milliseconds", "ms"], "1/1,000 of a second"),
        "microsecond": UnitMetadata("Microsecond", "µs", 1e-6, UnitCategory.TIME, ["microsecond", "microseconds", "us", "µs"], "10⁻⁶ seconds"),
        "nanosecond": UnitMetadata("Nanosecond", "ns", 1e-9, UnitCategory.TIME, ["nanosecond", "nanoseconds", "ns"], "10⁻⁹ seconds"),
        "minute": UnitMetadata("Minute", "min", 60.0, UnitCategory.TIME, ["minute", "minutes", "min", "m"], "60 seconds"),
        "hour": UnitMetadata("Hour", "h", 3600.0, UnitCategory.TIME, ["hour", "hours", "hr", "h"], "60 minutes"),
        "day": UnitMetadata("Day", "d", 86400.0, UnitCategory.TIME, ["day", "days", "d"], "24 hours"),
        "week": UnitMetadata("Week", "wk", 604800.0, UnitCategory.TIME, ["week", "weeks", "wk"], "7 days"),
        "month": UnitMetadata("Month (avg)", "mo", 2629800.0, UnitCategory.TIME, ["month", "months", "mo"], "Average solar calendar month (30.4375 days)"),
        "year": UnitMetadata("Year (Julian)", "yr", 31557600.0, UnitCategory.TIME, ["year", "years", "yr", "y"], "Astronomical Julian year (365.25 days)"),
    },
    UnitCategory.DIGITAL_STORAGE: {
        "byte": UnitMetadata("Byte", "B", 1.0, UnitCategory.DIGITAL_STORAGE, ["byte", "bytes", "b"], "Standard 8-bit digital storage atom"),
        "kilobyte": UnitMetadata("Kilobyte (decimal)", "KB", 1000.0, UnitCategory.DIGITAL_STORAGE, ["kilobyte", "kilobytes", "kb"], "1,000 bytes (SI decimal standard)"),
        "megabyte": UnitMetadata("Megabyte (decimal)", "MB", 1e6, UnitCategory.DIGITAL_STORAGE, ["megabyte", "megabytes", "mb"], "1,000,000 bytes"),
        "gigabyte": UnitMetadata("Gigabyte (decimal)", "GB", 1e9, UnitCategory.DIGITAL_STORAGE, ["gigabyte", "gigabytes", "gb"], "1,000,000,000 bytes"),
        "terabyte": UnitMetadata("Terabyte (decimal)", "TB", 1e12, UnitCategory.DIGITAL_STORAGE, ["terabyte", "terabytes", "tb"], "10¹² bytes"),
        "petabyte": UnitMetadata("Petabyte (decimal)", "PB", 1e15, UnitCategory.DIGITAL_STORAGE, ["petabyte", "petabytes", "pb"], "10¹⁵ bytes"),
        "kibibyte": UnitMetadata("Kibibyte (binary)", "KiB", 1024.0, UnitCategory.DIGITAL_STORAGE, ["kibibyte", "kibibytes", "kib"], "1,024 bytes (IEC binary)"),
        "mebibyte": UnitMetadata("Mebibyte (binary)", "MiB", 1048576.0, UnitCategory.DIGITAL_STORAGE, ["mebibyte", "mebibytes", "mib"], "1,024² bytes"),
        "gibibyte": UnitMetadata("Gibibyte (binary)", "GiB", 1073741824.0, UnitCategory.DIGITAL_STORAGE, ["gibibyte", "gibibytes", "gib"], "1,024³ bytes"),
        "tebibyte": UnitMetadata("Tebibyte (binary)", "TiB", 1099511627776.0, UnitCategory.DIGITAL_STORAGE, ["tebibyte", "tebibytes", "tib"], "1,024⁴ bytes"),
    },
    UnitCategory.ENERGY: {
        "joule": UnitMetadata("Joule", "J", 1.0, UnitCategory.ENERGY, ["joule", "joules", "j"], "SI base unit of energy/work"),
        "kilojoule": UnitMetadata("Kilojoule", "kJ", 1000.0, UnitCategory.ENERGY, ["kilojoule", "kilojoules", "kj"], "1,000 joules"),
        "calorie": UnitMetadata("Calorie (thermochemical)", "cal", 4.184, UnitCategory.ENERGY, ["calorie", "calories", "cal"], "Energy to heat 1g water by 1 °C"),
        "kilocalorie": UnitMetadata("Kilocalorie / Food Calorie", "kcal", 4184.0, UnitCategory.ENERGY, ["kilocalorie", "kilocalories", "kcal", "Calorie"], "1,000 calories (Dietary Cal)"),
        "watt_hour": UnitMetadata("Watt-hour", "Wh", 3600.0, UnitCategory.ENERGY, ["watt-hour", "watt hour", "wh"], "1 watt power over 1 hour"),
        "kilowatt_hour": UnitMetadata("Kilowatt-hour", "kWh", 3.6e6, UnitCategory.ENERGY, ["kilowatt-hour", "kilowatt hour", "kwh"], "Electrical billing standard (3.6 MJ)"),
        "electronvolt": UnitMetadata("Electronvolt", "eV", 1.602176634e-19, UnitCategory.ENERGY, ["electronvolt", "electronvolts", "ev"], "Particle physics quantum energy scale"),
        "btu": UnitMetadata("British Thermal Unit", "BTU", 1055.056, UnitCategory.ENERGY, ["btu", "british thermal unit"], "ISO British thermal unit"),
    },
    UnitCategory.PRESSURE: {
        "pascal": UnitMetadata("Pascal", "Pa", 1.0, UnitCategory.PRESSURE, ["pascal", "pascals", "pa"], "SI derived unit of pressure (N/m²)"),
        "kilopascal": UnitMetadata("Kilopascal", "kPa", 1000.0, UnitCategory.PRESSURE, ["kilopascal", "kilopascals", "kpa"], "1,000 pascals"),
        "bar": UnitMetadata("Bar", "bar", 100000.0, UnitCategory.PRESSURE, ["bar", "bars"], "100,000 pascals (approx atmospheric pressure)"),
        "psi": UnitMetadata("Pounds per Square Inch", "psi", 6894.757293168, UnitCategory.PRESSURE, ["psi", "pound per square inch", "pounds per square inch"], "Imperial standard pressure"),
        "atmosphere": UnitMetadata("Standard Atmosphere", "atm", 101325.0, UnitCategory.PRESSURE, ["atm", "atmosphere", "atmospheres"], "Mean sea level atmospheric pressure"),
        "torr": UnitMetadata("Torr / mmHg", "Torr", 133.322368421, UnitCategory.PRESSURE, ["torr", "mmhg"], "1/760 of an atmosphere"),
    }
}


def get_categories() -> List[str]:
    """Returns the ordered list of all supported unit categories."""
    return list(UNIT_REGISTRY.keys())


def get_units_for_category(category: str) -> Dict[str, UnitMetadata]:
    """Returns mapping of unit_key -> UnitMetadata for a given category."""
    return UNIT_REGISTRY.get(category, {})


def find_unit_category(unit_key_or_alias: str) -> Optional[Tuple[str, str]]:
    """
    Locates the category and normalized unit key for a given name or alias.
    Returns (category, unit_key) or None.
    """
    target = unit_key_or_alias.strip().lower()
    
    # Direct match first
    for cat, units in UNIT_REGISTRY.items():
        if target in units:
            return cat, target
            
    # Alias search
    for cat, units in UNIT_REGISTRY.items():
        for key, meta in units.items():
            if target in [a.lower() for a in meta.aliases]:
                return cat, key
                
    return None


def get_all_units_flat() -> List[Dict[str, Any]]:
    """Returns flat catalog of all units with metadata for agentic tooling."""
    catalog = []
    for cat, units in UNIT_REGISTRY.items():
        for key, meta in units.items():
            catalog.append({
                "category": cat,
                "key": key,
                "name": meta.name,
                "symbol": meta.symbol,
                "factor_to_base": meta.factor_to_base,
                "description": meta.description
            })
    return catalog


def convert_temperature(value: float, from_unit: str, to_unit: str) -> Tuple[float, str, str]:
    """
    Performs affine thermodynamic temperature transformations.
    Converts via Kelvin intermediate.
    """
    from_k = from_unit.lower()
    to_k = to_unit.lower()

    # Step 1: Convert from source to Kelvin
    if from_k in ("kelvin", "k"):
        kelvin_val = value
        to_kelvin_formula = f"K = {value}"
    elif from_k in ("celsius", "c"):
        kelvin_val = value + 273.15
        to_kelvin_formula = f"K = {value} + 273.15 = {kelvin_val:.4f}"
    elif from_k in ("fahrenheit", "f"):
        kelvin_val = (value - 32.0) * (5.0 / 9.0) + 273.15
        to_kelvin_formula = f"K = ({value} - 32) \\times \\frac{{5}}{{9}} + 273.15 = {kelvin_val:.4f}"
    elif from_k in ("rankine", "r"):
        kelvin_val = value * (5.0 / 9.0)
        to_kelvin_formula = f"K = {value} \\times \\frac{{5}}{{9}} = {kelvin_val:.4f}"
    else:
        raise ValueError(f"Unsupported temperature unit: '{from_unit}'")

    if kelvin_val < -1e-6:
        # Physical lower bound check
        pass  # We warn or allow theoretical negative temperatures in calculation

    # Step 2: Convert from Kelvin to target unit
    if to_k in ("kelvin", "k"):
        target_val = kelvin_val
        from_kelvin_formula = f"K = {kelvin_val:.4f}"
        latex_eq = f"T_{{K}} = {target_val:.4f}\\text{{ K}}"
    elif to_k in ("celsius", "c"):
        target_val = kelvin_val - 273.15
        from_kelvin_formula = f"°C = {kelvin_val:.4f} - 273.15 = {target_val:.4f}"
        latex_eq = f"T_{{°C}} = {value}\\text{{ [{from_unit}]}} \\rightarrow {target_val:.4f}\\text{{ °C}}"
    elif to_k in ("fahrenheit", "f"):
        target_val = (kelvin_val - 273.15) * (9.0 / 5.0) + 32.0
        from_kelvin_formula = f"°F = ({kelvin_val:.4f} - 273.15) \\times \\frac{{9}}{{5}} + 32 = {target_val:.4f}"
        latex_eq = f"T_{{°F}} = {value}\\text{{ [{from_unit}]}} \\rightarrow {target_val:.4f}\\text{{ °F}}"
    elif to_k in ("rankine", "r"):
        target_val = kelvin_val * (9.0 / 5.0)
        from_kelvin_formula = f"°R = {kelvin_val:.4f} \\times \\frac{{9}}{{5}} = {target_val:.4f}"
        latex_eq = f"T_{{°R}} = {value}\\text{{ [{from_unit}]}} \\rightarrow {target_val:.4f}\\text{{ °R}}"
    else:
        raise ValueError(f"Unsupported temperature unit: '{to_unit}'")

    step_text = (
        f"1. Convert '{from_unit}' to Kelvin (Absolute SI): {to_kelvin_formula}\n"
        f"2. Convert Kelvin to '{to_unit}': {from_kelvin_formula}"
    )
    return target_val, latex_eq, step_text


def convert(
    value: float,
    from_unit: str,
    to_unit: str,
    category: Optional[str] = None
) -> ConversionResult:
    """
    High-precision universal conversion function with full mathematical auditing.
    """
    # Normalize inputs
    from_loc = find_unit_category(from_unit)
    to_loc = find_unit_category(to_unit)

    if not from_loc:
        return ConversionResult(
            success=False,
            source_value=value,
            target_value=0.0,
            source_unit=from_unit,
            target_unit=to_unit,
            source_symbol="?",
            target_symbol="?",
            category="Unknown",
            formula_latex="",
            step_by_step="",
            error_message=f"Source unit '{from_unit}' is not recognized in the knowledge base."
        )

    if not to_loc:
        return ConversionResult(
            success=False,
            source_value=value,
            target_value=0.0,
            source_unit=from_unit,
            target_unit=to_unit,
            source_symbol="?",
            target_symbol="?",
            category="Unknown",
            formula_latex="",
            step_by_step="",
            error_message=f"Target unit '{to_unit}' is not recognized in the knowledge base."
        )

    from_cat, from_key = from_loc
    to_cat, to_key = to_loc

    # Verify category alignment
    if from_cat != to_cat:
        return ConversionResult(
            success=False,
            source_value=value,
            target_value=0.0,
            source_unit=from_unit,
            target_unit=to_unit,
            source_symbol="?",
            target_symbol="?",
            category=f"{from_cat} vs {to_cat}",
            formula_latex="",
            step_by_step="",
            error_message=(
                f"Dimensional mismatch: Cannot convert between '{from_cat}' ({from_unit}) "
                f"and '{to_cat}' ({to_unit}). Both units must belong to the same physical domain."
            )
        )

    matched_cat = from_cat
    from_meta = UNIT_REGISTRY[matched_cat][from_key]
    to_meta = UNIT_REGISTRY[matched_cat][to_key]

    # Same unit optimization
    if from_key == to_key:
        return ConversionResult(
            success=True,
            source_value=value,
            target_value=value,
            source_unit=from_meta.name,
            target_unit=to_meta.name,
            source_symbol=from_meta.symbol,
            target_symbol=to_meta.symbol,
            category=matched_cat,
            formula_latex=f"{value}\\text{{ {from_meta.symbol}}} = {value}\\text{{ {to_meta.symbol}}}",
            step_by_step=f"Source and target units are identical ({from_meta.name}). Ratio is exactly 1:1."
        )

    # Temperature branch (Affine transformation)
    if matched_cat == UnitCategory.TEMPERATURE:
        try:
            target_val, latex_eq, steps = convert_temperature(value, from_key, to_key)
            return ConversionResult(
                success=True,
                source_value=value,
                target_value=target_val,
                source_unit=from_meta.name,
                target_unit=to_meta.name,
                source_symbol=from_meta.symbol,
                target_symbol=to_meta.symbol,
                category=matched_cat,
                formula_latex=latex_eq,
                step_by_step=steps
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                source_value=value,
                target_value=0.0,
                source_unit=from_meta.name,
                target_unit=to_meta.name,
                source_symbol=from_meta.symbol,
                target_symbol=to_meta.symbol,
                category=matched_cat,
                formula_latex="",
                step_by_step="",
                error_message=str(e)
            )

    # Standard Linear / Ratio Branch
    # val_in_base = value * from_factor
    # target_val = val_in_base / to_factor
    from_factor = from_meta.factor_to_base
    to_factor = to_meta.factor_to_base

    ratio = from_factor / to_factor
    target_value = value * ratio

    # Format LaTeX formula and explanation
    if ratio >= 1.0:
        ratio_str = f"{ratio:g}"
    else:
        ratio_str = f"{ratio:.8g}"

    formula_latex = (
        f"{value}\\text{{ {from_meta.symbol}}} \\times "
        f"\\left( {ratio_str}\\ \\frac{{\\text{{{to_meta.symbol}}}}}{{\\text{{{from_meta.symbol}}}}} \\right) = "
        f"{target_value:.6g}\\text{{ {to_meta.symbol}}}"
    )

    steps = (
        f"1. Convert '{from_meta.name}' to base unit ({matched_cat}):\n"
        f"   {value} × {from_factor:g} = {value * from_factor:g} [Base]\n"
        f"2. Convert base unit to '{to_meta.name}':\n"
        f"   {value * from_factor:g} ÷ {to_factor:g} = {target_value:g} {to_meta.symbol}\n"
        f"3. Direct conversion factor: 1 {from_meta.symbol} = {ratio_str} {to_meta.symbol}"
    )

    return ConversionResult(
        success=True,
        source_value=value,
        target_value=target_value,
        source_unit=from_meta.name,
        target_unit=to_meta.name,
        source_symbol=from_meta.symbol,
        target_symbol=to_meta.symbol,
        category=matched_cat,
        formula_latex=formula_latex,
        step_by_step=steps
    )
