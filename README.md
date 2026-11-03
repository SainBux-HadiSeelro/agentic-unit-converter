<div align="center">

# ⚡ OmniConvert AI
### *Autonomous Multilingual Unit Intelligence & 24/7 AI Copilot*

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Technical Spec](https://img.shields.io/badge/Architecture-SPEC.md-0A66C2?style=for-the-badge&logo=markdown&logoColor=white)](SPEC.md)
[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Agent Paradigm](https://img.shields.io/badge/Architecture-ReAct%20Tool--Calling-8A2BE2?style=for-the-badge&logo=openai&logoColor=white)](SPEC.md#3-cognitive-architecture--react-agent-loop)
[![Bilingual NLU](https://img.shields.io/badge/NLU-English%20%7C%20Roman%20Urdu-228B22?style=for-the-badge)](SPEC.md#4-multilingual-nlp--roman-urdu-semantic-engine)
[![Physics Standards](https://img.shields.io/badge/Standard-NIST%20SP%20811%20%7C%20ISO%2080000-FF8C00?style=for-the-badge)](SPEC.md#5-tiered-mathematical-conversion-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<br/>

**Architected & Developed by [Hadi Seelro](https://github.com/SainBux-HadiSeelro)**  
*Agentic AI Developer & Full-Stack Systems Engineer*

---

[🎮 Launch App](#-quickstart--local-run) • [📋 System Architecture & SPEC](SPEC.md) • [🧠 The Agentic Paradigm](#-why-this-stands-out-for-recruiters) • [🌟 Core Features](#-core-capabilities) • [🤖 247 Copilot](#-247-autonomous-ai-copilot-nova) • [🧪 Testing](#-test-suite--verification) • [👨‍💻 Developer Profile](#-about-the-developer)

---

</div>

## 💡 Why This Stands Out for Recruiters

Most beginner projects feature simple 30-line unit converters with hardcoded dictionaries that crash on unmapped units. **OmniConvert AI** transforms an ordinary utility into a **production-grade Agentic AI application**:

| Traditional Unit Converter | ⚡ OmniConvert AI (Agentic System) |
| :--- | :--- |
| Hardcoded pairwise dictionaries ($O(N^2)$ combinations) | **Canonical SI Base Normalization ($O(1)$ complexity)** |
| Crashes on same-unit or cross-domain conversions | **Strict Dimensional Homogeneity & Bounds Guardrails** |
| Rigid, click-only drop-downs | **Bilingual NLU (understands English & Roman Urdu prompts)** |
| Static black-box numerical output | **Step-by-Step LaTeX Derivations with NIST Standards** |
| No customer support or assistance | **24/7 Autonomous AI Copilot (Zero Downtime / Offline Ready)** |
| Ephemeral state | **Live Audit Trail with Instant CSV & JSON Data Export** |

---

## 🏗️ System Architecture

```text
               ┌────────────────────────────────────────────────────────┐
               │                  User Interaction                      │
               │   (Click UI  •  English Prompt  •  Roman Urdu Query)   │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │             Interaction Gateway (Streamlit)            │
               │       - Dark Glassmorphism Cyber Styling               │
               │       - Dynamic Category Tabs (10 Domains)             │
               │       - Live KaTeX Formula Rendering                   │
               └───────────────┬────────────────────────┬───────────────┘
                               │                        │
             Direct GUI Inputs │                        │ Natural Language
                               ▼                        ▼
     ┌───────────────────────────────────┐    ┌──────────────────────────────────┐
     │    Physical Mathematics Engine    │    │   Agentic NLU Intent Parser      │
     │  - SI Base Unit Normalization     │    │  - English & Roman Urdu regex    │
     │  - Affine Thermodynamic Calculus  │    │  - Entity extraction (val/units) │
     │  - Precision & Scientific Format  │    │  - ReAct Tool Dispatch           │
     └─────────────────┬─────────────────┘    └─────────────────┬────────────────┘
                       │                                        │
                       └───────────────────┬────────────────────┘
                                           ▼
                     ┌───────────────────────────────────────────┐
                     │     24/7 Autonomous AI Copilot (Nova)     │
                     │  - Zero-Downtime Deterministic Engine     │
                     │  - Real-Time Tool Calling (`convert`)     │
                     │  - Embedded Project & Portfolio KB        │
                     │  - Optional Gemini / OpenAI API Gateway   │
                     └─────────────────────┬─────────────────────┘
                                           ▼
                     ┌───────────────────────────────────────────┐
                     │            Auditable Outputs              │
                     │  (LaTeX Proof • CSV Export • JSON Trail)  │
                     └───────────────────────────────────────────┘
```

---

## 🌟 Core Capabilities

### 1. 📏 10 Comprehensive Physical Domains & 60+ Units
- **Length**: Meter, Kilometer, Centimeter, Millimeter, Micrometer, Nanometer, Mile, Yard, Foot, Inch, Nautical Mile.
- **Weight & Mass**: Kilogram, Gram, Milligram, Microgram, Metric Ton, Pound (lb), Ounce (oz), Stone, Carat.
- **Temperature**: Celsius, Fahrenheit, Kelvin (Absolute SI), Rankine.
- **Area**: Square Meter, Square Kilometer, Square Mile, Square Yard, Square Foot, Square Inch, Hectare, Acre.
- **Volume**: Liter, Milliliter, Cubic Meter, Gallon US, Quart, Pint, Cup, Fluid Ounce, Tablespoon, Teaspoon.
- **Speed**: Meters per Second, Kilometers per Hour, Miles per Hour, Knots, Feet per Second, Mach.
- **Time**: Second, Millisecond, Microsecond, Nanosecond, Minute, Hour, Day, Week, Month, Year.
- **Digital Storage**: Decimal (B, KB, MB, GB, TB, PB) and Binary IEC (KiB, MiB, GiB, TiB).
- **Energy & Work**: Joule, Kilojoule, Calorie, Kilocalorie, Watt-hour, Kilowatt-hour, Electronvolt, BTU.
- **Pressure**: Pascal, Kilopascal, Bar, PSI, Atmosphere, Torr / mmHg.

### 2. 🧠 Agentic Bilingual NLU (English & Roman Urdu)
Understands real-world colloquial prompts seamlessly:
- *"Convert 120 km/h to mph"* ➔ Auto-detects Speed domain, computes `74.5645 mph`.
- *"50 miles ko kilometer me badlo"* ➔ Detects Roman Urdu, extracts parameters, and converts to `80.4672 km`.
- *"500 gram kitne kg hote hain"* ➔ Computes `0.5 kg` with exact step-by-step ratio derivation.
- *"100 celsius ko fahrenheit me convert karo"* ➔ Executes thermodynamic affine transformation: $°F = (100 \times \frac{9}{5}) + 32 = 212°F$.

### 3. 🤖 24/7 Autonomous AI Copilot ("Nova")
- **Zero Downtime Guarantee**: Operates 24/7 without requiring paid external API keys via a deterministic cognitive ReAct engine.
- **Tool Calling**: Directly executes unit conversions and mathematical queries within the chat conversation.
- **Full Knowledge Base**: Equipped with complete project architecture, technical specifications, and developer credentials.
- **Multi-Provider Scaling**: Seamlessly plugs into **Google Gemini** or **OpenAI** if an API key is provided.

### 4. 📐 Auditable Step-by-Step LaTeX Derivations
Every conversion outputs the rigorous mathematical equation formatted in LaTeX:

$$\text{Value}_{\text{target}} = \text{Value}_{\text{source}} \times \left( \frac{\text{Base Factor}_{\text{source}}}{\text{Base Factor}_{\text{target}}} \right)$$

### 5. 🕒 Session Audit Trail & Instant Data Export
Every calculation is recorded in session state with a timestamp. Users can download their conversion history in **CSV** or **JSON** format with a single click.

---

## 🚀 Quickstart & Local Run

### Prerequisites
- Python 3.11 or 3.12 installed.

### 1. Clone the Repository
```bash
git clone https://github.com/SainBux-HadiSeelro/agentic-unit-converter.git
cd agentic-unit-converter
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*Or using UV:*
```bash
uv pip install -r requirements.txt
```

### 3. Run the Modern Web Application
```bash
streamlit run unit_converter.py
```
*(Or simply `streamlit run app.py`)*

The web application will launch in your browser at `http://localhost:8501`.

---

## 🐍 Programmatic Python SDK Usage

You can import and use the mathematical engine directly in your own Python projects:

```python
from engine.converter import convert

# Convert speed with NIST precision
result = convert(value=100.0, from_unit="mile_per_hour", to_unit="kilometer_per_hour")

if result.success:
    print(f"Target: {result.target_value:.2f} {result.target_symbol}")
    print(f"LaTeX Equation: {result.formula_latex}")
else:
    print(f"Error: {result.error_message}")
```

---

## 🧪 Test Suite & Verification

The project includes an automated test harness covering mathematical precision, affine temperature conversions, bilingual NLP queries, and agentic tool dispatch:

```bash
python -m pytest -v
```

### Test Results
```text
============================= test session starts =============================
tests/test_converter.py::TestMathematicalConverter::test_length_conversion PASSED
tests/test_converter.py::TestMathematicalConverter::test_same_unit_conversion PASSED
tests/test_converter.py::TestMathematicalConverter::test_mass_conversion PASSED
tests/test_converter.py::TestMathematicalConverter::test_temperature_affine_conversions PASSED
tests/test_converter.py::TestMathematicalConverter::test_digital_storage_decimal_and_binary PASSED
tests/test_converter.py::TestMathematicalConverter::test_dimensional_mismatch_error_handling PASSED
tests/test_converter.py::TestAgenticNLPParser::test_english_query_parsing PASSED
tests/test_converter.py::TestAgenticNLPParser::test_roman_urdu_conversion_query PASSED
tests/test_converter.py::TestAgenticNLPParser::test_roman_urdu_question_query PASSED
tests/test_converter.py::TestAgenticCopilot::test_chatbot_tool_execution PASSED
tests/test_converter.py::TestAgenticCopilot::test_chatbot_portfolio_query PASSED
tests/test_converter.py::TestAgenticCopilot::test_chatbot_faq_and_greetings PASSED

============================= 12 passed in 0.66s ==============================
```

---

## 👨‍💻 About the Developer

**Hadi Seelro** is an **Agentic AI Developer & Full-Stack Systems Engineer** focused on building production-grade autonomous agent systems, multi-agent orchestrations, LLM tool-calling architectures, and modern web applications.

- 🌐 **GitHub**: [@SainBux-HadiSeelro](https://github.com/SainBux-HadiSeelro)
- 💼 **Available for**: Agentic AI Consulting, Enterprise AI Tooling, Full-Stack Python Engineering.
- 📋 **System Specifications**: Check out [SPEC.md](SPEC.md) for full IEEE 830 architectural documentation.

---

<div align="center">
<b>OmniConvert AI • Designed for Production & Portfolio Excellence</b><br/>
Distributed under the MIT License.
</div>
