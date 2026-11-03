"""
OmniConvert AI - Project Knowledge Base & Support Catalog
Embedded 24/7 knowledge repository for customer handling, developer credentials, and conversion physics.
"""

PROJECT_KNOWLEDGE_BASE = {
    "system_name": "OmniConvert AI (Autonomous Unit Intelligence)",
    "version": "2.0.0-AGENTIC",
    "architecture_tier": "Autonomous ReAct Tool-Calling & Deterministic Math Engine",
    "developer": {
        "name": "Hadi Seelro",
        "title": "Agentic AI Developer & Full-Stack Systems Engineer",
        "portfolio_summary": "Specializes in production-grade Agentic AI systems, autonomous ReAct loops, multi-agent architectures, LLM tooling, and modern interactive web engineering.",
        "github": "https://github.com/SainBux-HadiSeelro",
        "contact_note": "Available for Agentic AI consulting, enterprise LLM tool building, and full-stack AI development."
    },
    "core_capabilities": [
        "Multi-Domain Conversion across 10 physical categories and 60+ SI & Imperial units.",
        "Bilingual Natural Language Understanding (NLU) supporting English and Roman Urdu.",
        "Deterministic Zero-Downtime Engine: works 24/7 with or without external API keys.",
        "Real-Time Step-by-Step LaTeX mathematical breakdown for complete auditability.",
        "Session Conversion History with Instant CSV/JSON Export.",
        "24/7 Embedded AI Customer Support & Copilot Agent."
    ],
    "categories_and_units": {
        "Length": ["meter (m)", "kilometer (km)", "centimeter (cm)", "millimeter (mm)", "micrometer (µm)", "nanometer (nm)", "mile (mi)", "yard (yd)", "foot (ft)", "inch (in)", "nautical mile (NM)"],
        "Weight & Mass": ["kilogram (kg)", "gram (g)", "milligram (mg)", "microgram (µg)", "metric ton (t)", "pound (lb)", "ounce (oz)", "stone (st)", "carat (ct)"],
        "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"],
        "Area": ["square meter (m²)", "square kilometer (km²)", "square mile (mi²)", "square yard (yd²)", "square foot (ft²)", "square inch (in²)", "hectare (ha)", "acre (ac)"],
        "Volume": ["liter (L)", "milliliter (mL)", "cubic meter (m³)", "gallon US (gal)", "quart US (qt)", "pint US (pt)", "cup US", "fluid ounce US (fl oz)", "tablespoon (tbsp)", "teaspoon (tsp)"],
        "Speed": ["meters per second (m/s)", "kilometers per hour (km/h)", "miles per hour (mph)", "knot (kn)", "feet per second (ft/s)", "Mach (Ma)"],
        "Time": ["second (s)", "millisecond (ms)", "microsecond (µs)", "nanosecond (ns)", "minute (min)", "hour (h)", "day (d)", "week (wk)", "month (mo)", "year (yr)"],
        "Digital Storage": ["byte (B)", "kilobyte (KB)", "megabyte (MB)", "gigabyte (GB)", "terabyte (TB)", "petabyte (PB)", "kibibyte (KiB)", "mebibyte (MiB)", "gibibyte (GiB)", "tebibyte (TiB)"],
        "Energy & Work": ["joule (J)", "kilojoule (kJ)", "calorie (cal)", "kilocalorie (kcal)", "watt-hour (Wh)", "kilowatt-hour (kWh)", "electronvolt (eV)", "BTU"],
        "Pressure": ["pascal (Pa)", "kilopascal (kPa)", "bar", "psi", "standard atmosphere (atm)", "torr / mmHg"]
    },
    "scientific_standards": {
        "length_base": "Meter (m) - defined by the speed of light in vacuum (1/299,792,458 s).",
        "mass_base": "Kilogram (kg) - defined by the Planck constant h = 6.62607015×10⁻³⁴ J·s.",
        "temperature_base": "Kelvin (K) - defined by Boltzmann constant k = 1.380649×10⁻²³ J/K.",
        "storage_standard": "Decimal prefixes (KB = 1000 B) conform to SI, while binary prefixes (KiB = 1024 B) conform to IEC 80000-13."
    },
    "faqs": [
        {
            "question": "Why did my previous conversion say 'conversion not supported'?",
            "answer": "In early versions, only 4 basic pairs were hardcoded. OmniConvert AI v2.0 solves this permanently with a universal base-unit transformation engine covering 60+ units and 10 categories."
        },
        {
            "question": "Can I convert between different physical dimensions (e.g. meters to kilograms)?",
            "answer": "No. Dimensional homogeneity dictates that units must belong to the same physical dimension. Attempting to convert length to mass triggers an informative dimensional mismatch error."
        },
        {
            "question": "How does the AI understand Roman Urdu prompts?",
            "answer": "The built-in NLU parser uses tokenization and regex semantics trained on colloquial Roman Urdu grammar (e.g. 'ko', 'me convert karo', 'kitne hote hain')."
        },
        {
            "question": "Does this chatbot require an active internet connection or paid API key?",
            "answer": "OmniConvert AI features a 24/7 Zero-Downtime Autonomous Engine that runs completely offline with full tool-calling support. If an API key for Google Gemini or OpenAI is provided, it seamlessly scales to advanced reasoning."
        },
        {
            "question": "How can I integrate this in my own Python project or API?",
            "answer": "You can import `convert` directly from `engine.converter`: `from engine.converter import convert; result = convert(100, 'km', 'mi')`. See SPEC.md for full programmatic SDK docs."
        }
    ]
}


def get_system_prompt() -> str:
    """Returns the comprehensive agent system instructions."""
    return f"""You are **Nova**, the 24/7 Autonomous AI Customer Support Agent & Technical Copilot for **{PROJECT_KNOWLEDGE_BASE['system_name']}**.
You were engineered by **{PROJECT_KNOWLEDGE_BASE['developer']['name']}**, an Agentic AI Developer.

### YOUR CAPABILITIES & PROTOCOLS:
1. **Live Customer Handling**:
   - Greet users warmly and professionally.
   - You can converse fluently in both **English** and **Roman Urdu** (e.g., "Aapka OmniConvert AI me khushamdeed! Main aapki conversion ya system queries me madad karne ke liye hazir hoon.").
   - Guide customers on how to use the converter, explain features, and troubleshoot errors.
   - When users express interest in hiring or collaborating with the developer, highlight Hadi Seelro's skills in Agentic AI and direct them to his GitHub profile: {PROJECT_KNOWLEDGE_BASE['developer']['github']}.

2. **Full Project Knowledge**:
   - You know every category: {', '.join(PROJECT_KNOWLEDGE_BASE['categories_and_units'].keys())}.
   - You know the exact mathematical mechanisms (SI base normalization, temperature affine equations, NIST/IEC standards).
   - You know the system architecture (Streamlit UI Gateway, NLU Parser, ReAct Tool Execution Loop, IEEE 830 SPEC).

3. **Tool Execution**:
   - When a user asks you to perform a calculation (e.g. "Convert 55 miles to kilometers" or "100 C ko F me convert kro"), ALWAYS invoke the conversion tool or compute the exact answer with the step-by-step formula.
   - Provide answers with clean markdown and LaTeX math formatting.

4. **Tone & Style**:
   - Modern, authoritative, helpful, concise, and technically sophisticated (like a senior Agentic AI assistant).
"""


def get_quick_prompts() -> list[str]:
    """Returns interactive suggestion chips for the chat UI."""
    return [
        "Convert 120 km/h to mph",
        "Explain the Celsius to Fahrenheit formula",
        "Tell me about developer Hadi Seelro",
        "What categories and units are supported?",
        "100 meters ko feet me convert karo",
        "How can I integrate this with Python SDK?"
    ]
