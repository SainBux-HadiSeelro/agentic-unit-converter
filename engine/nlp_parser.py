"""
OmniConvert AI - Agentic Natural Language Understanding (NLU) Parser
Parses conversational intent, numerical values, and unit entities in English and Roman Urdu.
"""
import re
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any
from .converter import find_unit_category, convert, ConversionResult


@dataclass
class NLPParseResult:
    success: bool
    source_value: Optional[float]
    source_unit: Optional[str]
    target_unit: Optional[str]
    category: Optional[str]
    conversion_result: Optional[ConversionResult]
    confidence: float
    detected_language: str
    message: str


# Common unit aliases dictionary for NLP normalization
NLP_ALIAS_MAP: Dict[str, str] = {
    # Length
    "m": "meter", "meter": "meter", "meters": "meter", "metre": "meter",
    "km": "kilometer", "kilometer": "kilometer", "kilometers": "kilometer",
    "cm": "centimeter", "centimeters": "centimeter",
    "mm": "millimeter", "millimeters": "millimeter",
    "mi": "mile", "mile": "mile", "miles": "mile",
    "yd": "yard", "yards": "yard",
    "ft": "foot", "foot": "foot", "feet": "foot",
    "in": "inch", "inch": "inch", "inches": "inch",
    "nmi": "nautical_mile", "nautical mile": "nautical_mile",

    # Mass
    "kg": "kilogram", "kilo": "kilogram", "kilos": "kilogram", "kilogram": "kilogram", "kilograms": "kilogram",
    "g": "gram", "gm": "gram", "gram": "gram", "grams": "gram",
    "mg": "milligram", "milligrams": "milligram",
    "lb": "pound", "lbs": "pound", "pound": "pound", "pounds": "pound",
    "oz": "ounce", "ounce": "ounce", "ounces": "ounce",
    "ton": "metric_ton", "tonne": "metric_ton", "metric ton": "metric_ton",

    # Temperature
    "c": "celsius", "celsius": "celsius", "centigrade": "celsius", "deg c": "celsius", "degree c": "celsius",
    "f": "fahrenheit", "fahrenheit": "fahrenheit", "deg f": "fahrenheit", "degree f": "fahrenheit",
    "k": "kelvin", "kelvin": "kelvin",

    # Area
    "sqm": "square_meter", "sq m": "square_meter", "m2": "square_meter", "square meter": "square_meter",
    "sqkm": "square_kilometer", "sq km": "square_kilometer", "km2": "square_kilometer",
    "sqft": "square_foot", "sq ft": "square_foot", "ft2": "square_foot", "square feet": "square_foot",
    "acre": "acre", "acres": "acre",
    "hectare": "hectare", "hectares": "hectare",

    # Volume
    "l": "liter", "liter": "liter", "liters": "liter", "litre": "liter",
    "ml": "milliliter", "milliliters": "milliliter",
    "gal": "gallon_us", "gallon": "gallon_us", "gallons": "gallon_us",
    "cup": "cup_us", "cups": "cup_us",

    # Speed
    "mps": "meter_per_second", "m/s": "meter_per_second",
    "kph": "kilometer_per_hour", "kmh": "kilometer_per_hour", "km/h": "kilometer_per_hour",
    "mph": "mile_per_hour", "miles per hour": "mile_per_hour",
    "knot": "knot", "knots": "knot", "kn": "knot",

    # Time
    "s": "second", "sec": "second", "second": "second", "seconds": "second",
    "min": "minute", "minute": "minute", "minutes": "minute",
    "h": "hour", "hr": "hour", "hrs": "hour", "hour": "hour", "hours": "hour",
    "day": "day", "days": "day",
    "week": "week", "weeks": "week",
    "month": "month", "months": "month",
    "year": "year", "years": "year",

    # Digital Storage
    "b": "byte", "byte": "byte", "bytes": "byte",
    "kb": "kilobyte", "kilobytes": "kilobyte",
    "mb": "megabyte", "megabytes": "megabyte",
    "gb": "gigabyte", "gigabytes": "gigabyte",
    "tb": "terabyte", "terabytes": "terabyte",
    "kib": "kibibyte", "mib": "mebibyte", "gib": "gibibyte", "tib": "tebibyte",

    # Energy & Pressure
    "j": "joule", "joules": "joule", "kj": "kilojoule",
    "cal": "calorie", "calories": "calorie", "kcal": "kilocalorie",
    "kwh": "kilowatt_hour", "btu": "btu",
    "pa": "pascal", "kpa": "kilopascal", "bar": "bar", "psi": "psi", "atm": "atmosphere"
}


def normalize_unit_str(raw: str) -> str:
    """Cleans up and looks up a unit string in alias dictionary or unit finder."""
    clean = raw.strip().lower()
    clean = re.sub(r'^(into|to|in)\s+', '', clean)
    clean = clean.replace('°', '')
    
    if clean in NLP_ALIAS_MAP:
        return NLP_ALIAS_MAP[clean]
        
    found = find_unit_category(clean)
    if found:
        return found[1]
    return clean


def parse_conversion_query(query: str) -> NLPParseResult:
    """
    Agentic parser capable of extracting parameters from queries in English & Roman Urdu.
    """
    if not query or not query.strip():
        return NLPParseResult(
            success=False,
            source_value=None,
            source_unit=None,
            target_unit=None,
            category=None,
            conversion_result=None,
            confidence=0.0,
            detected_language="Unknown",
            message="Empty query received."
        )

    text = query.strip()
    is_roman_urdu = bool(re.search(r'\b(ko|me|mein|badlo|karo|kro|kitne|kitna|hote|hotee|hain|hai|batao)\b', text, re.IGNORECASE))
    lang = "Roman Urdu" if is_roman_urdu else "English"

    # Pattern 1: Roman Urdu patterns
    # e.g.: "100 meter ko feet me convert karo" or "50 miles ko km me badlo" or "500 gram kitne kg hote hain"
    m_urdu1 = re.search(
        r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+ko\s+([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+(?:me|mein)',
        text,
        re.IGNORECASE
    )
    if m_urdu1:
        val = float(m_urdu1.group(1))
        u_from = normalize_unit_str(m_urdu1.group(2))
        u_to = normalize_unit_str(m_urdu1.group(3))
        res = convert(val, u_from, u_to)
        return NLPParseResult(
            success=res.success,
            source_value=val,
            source_unit=res.source_unit if res.success else u_from,
            target_unit=res.target_unit if res.success else u_to,
            category=res.category if res.success else None,
            conversion_result=res,
            confidence=0.95,
            detected_language="Roman Urdu",
            message=f"Parsed Roman Urdu query: {val} {u_from} -> {u_to}"
        )

    m_urdu2 = re.search(
        r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+(?:kitne|kitna)\s+([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+(?:hote|hota|hoti)',
        text,
        re.IGNORECASE
    )
    if m_urdu2:
        val = float(m_urdu2.group(1))
        u_from = normalize_unit_str(m_urdu2.group(2))
        u_to = normalize_unit_str(m_urdu2.group(3))
        res = convert(val, u_from, u_to)
        return NLPParseResult(
            success=res.success,
            source_value=val,
            source_unit=res.source_unit if res.success else u_from,
            target_unit=res.target_unit if res.success else u_to,
            category=res.category if res.success else None,
            conversion_result=res,
            confidence=0.92,
            detected_language="Roman Urdu",
            message=f"Parsed Roman Urdu question: {val} {u_from} -> {u_to}"
        )

    # Pattern 2: English "convert X unit1 to/in/into unit2"
    m_eng1 = re.search(
        r'(?:convert\s+)?([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+(?:to|in|into)\s+([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)',
        text,
        re.IGNORECASE
    )
    if m_eng1:
        val = float(m_eng1.group(1))
        u_from = normalize_unit_str(m_eng1.group(2))
        u_to = normalize_unit_str(m_eng1.group(3))
        res = convert(val, u_from, u_to)
        return NLPParseResult(
            success=res.success,
            source_value=val,
            source_unit=res.source_unit if res.success else u_from,
            target_unit=res.target_unit if res.success else u_to,
            category=res.category if res.success else None,
            conversion_result=res,
            confidence=0.96,
            detected_language="English",
            message=f"Parsed English command: {val} {u_from} -> {u_to}"
        )

    # Pattern 3: "what is X unit1 in unit2" or "how many unit2 in X unit1"
    m_eng2 = re.search(
        r'how\s+many\s+([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)\s+(?:are\s+)?(?:in|inside)\s+([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Z°/\^23]+(?:\s+[a-zA-Z]+)?)',
        text,
        re.IGNORECASE
    )
    if m_eng2:
        u_to = normalize_unit_str(m_eng2.group(1))
        val = float(m_eng2.group(2))
        u_from = normalize_unit_str(m_eng2.group(3))
        res = convert(val, u_from, u_to)
        return NLPParseResult(
            success=res.success,
            source_value=val,
            source_unit=res.source_unit if res.success else u_from,
            target_unit=res.target_unit if res.success else u_to,
            category=res.category if res.success else None,
            conversion_result=res,
            confidence=0.90,
            detected_language="English",
            message=f"Parsed English 'how many' query: {val} {u_from} -> {u_to}"
        )

    # Fallback generic token scan
    # Look for a number and try to find two recognizable units
    num_match = re.search(r'([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)', text)
    if num_match:
        val = float(num_match.group(1))
        # Remove the number and split tokens
        rem = text.replace(num_match.group(1), ' ')
        tokens = re.findall(r'[a-zA-Z°/\^23]+', rem)
        recognized_units = []
        for t in tokens:
            u_norm = normalize_unit_str(t)
            cat = find_unit_category(u_norm)
            if cat:
                recognized_units.append(u_norm)
        
        if len(recognized_units) >= 2:
            u_from = recognized_units[0]
            u_to = recognized_units[1]
            res = convert(val, u_from, u_to)
            return NLPParseResult(
                success=res.success,
                source_value=val,
                source_unit=res.source_unit if res.success else u_from,
                target_unit=res.target_unit if res.success else u_to,
                category=res.category if res.success else None,
                conversion_result=res,
                confidence=0.75,
                detected_language=lang,
                message=f"Fallback token match: {val} {u_from} -> {u_to}"
            )

    return NLPParseResult(
        success=False,
        source_value=None,
        source_unit=None,
        target_unit=None,
        category=None,
        conversion_result=None,
        confidence=0.0,
        detected_language=lang,
        message=f"Could not automatically parse conversion intent from: '{query}'. Try formatting like '100 km to miles' or '50 kg ko lbs me badlo'."
    )
