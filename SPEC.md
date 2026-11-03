<div align="center">

# 📋 OmniConvert AI
### *Autonomous Multilingual Unit Intelligence & 24/7 Copilot*
#### **System Architecture & Technical Specification (SPEC-2026.2)**

[![Spec Standard](https://img.shields.io/badge/Spec_Standard-IEEE_830%20%7C%20Agentic_AI-0A66C2?style=for-the-badge&logo=ieee&logoColor=white)](#1-executive-overview--agentic-mission)
[![Cognitive Paradigm](https://img.shields.io/badge/Paradigm-ReAct%20Tool--Use%20%2B%20Zero--Downtime-8A2BE2?style=for-the-badge&logo=openai&logoColor=white)](#3-cognitive-architecture--react-agent-loop)
[![Physics Standards](https://img.shields.io/badge/Physics-NIST%20SP%20811%20%7C%20ISO%2080000-228B22?style=for-the-badge)](#5-tiered-mathematical-conversion-engine)
[![NLP Support](https://img.shields.io/badge/NLP-English%20%7C%20Roman%20Urdu%20Bilingual-008080?style=for-the-badge)](#4-multilingual-nlp--roman-urdu-semantic-engine)
[![Runtime](https://img.shields.io/badge/Runtime-Python%203.11%2B%20%7C%20Streamlit-3776AB?style=for-the-badge&logo=python&logoColor=white)](#8-programmatic-sdk--api-specification)

| Document Metadata | Specification Standard |
| :--- | :--- |
| **System Name** | OmniConvert AI (Autonomous Unit Intelligence Platform) |
| **Document Version** | `2.0.0-AGENTIC` |
| **Author / Lead Architect** | **Hadi Seelro** ([@SainBux-HadiSeelro](https://github.com/SainBux-HadiSeelro)) |
| **Architectural Pattern** | ReAct (Reason + Act) Autonomous Agent + Deterministic SI Normalization Engine |
| **Target Runtime** | Python 3.11+ / Streamlit 1.42+ / NumPy / Pandas |
| **Supported LLM Providers** | 24/7 Built-in Autonomous Engine, Google Gemini (`gemini-2.5-flash`), OpenAI (`gpt-4o-mini`) |
| **Standards Compliance** | NIST SP 811, BIPM SI Metric Manual, IEC 80000-13, IEEE 754-2019 Float64 |
| **Zero-Downtime Boundary** | Autonomous offline heuristic fallback guaranteeing continuous 24/7 customer handling |

</div>

---

## 📑 Table of Contents
1. [Executive Overview & Agentic Mission](#1-executive-overview--agentic-mission)
2. [End-to-End System Architecture](#2-end-to-end-system-architecture)
3. [Cognitive Architecture & ReAct Agent Loop](#3-cognitive-architecture--react-agent-loop)
4. [Multilingual NLP & Roman Urdu Semantic Engine](#4-multilingual-nlp--roman-urdu-semantic-engine)
5. [Tiered Mathematical Conversion Engine](#5-tiered-mathematical-conversion-engine)
6. [24/7 Zero-Downtime Customer Support Specification](#6-247-zero-downtime-customer-support-specification)
7. [Security Threat Model & Dimensional Guardrails](#7-security-threat-model--dimensional-guardrails)
8. [Programmatic SDK & API Specification](#8-programmatic-sdk--api-specification)
9. [Test Suite & Verification Matrix](#9-test-suite--verification-matrix)

---

## 1. Executive Overview & Agentic Mission

### 1.1 Problem Statement
Traditional unit converters suffer from several systemic defects:
1. **Hardcoded Combinatorial Explosion**: Early converters hardcode pairwise mappings (`meter_kilometer`, `kilometer_meter`). Scaling to $N$ units requires $O(N^2)$ mappings, causing crashes whenever an unmapped pair is queried.
2. **Dimensional Mismatch Vulnerabilities**: Flawed drop-down UX permits cross-domain conversions (e.g., converting meters to kilograms), leading to nonsensical computations.
3. **Rigid Syntax Barrier**: Conventional tools fail to understand natural queries like *"what is 75 mph in km/h"* or regional vernaculars like **Roman Urdu** (*"50 miles ko km me badlo"*).
4. **Black-Box Computations**: Outputs are rendered without mathematical derivations, preventing auditability in engineering contexts.
5. **Downtime in Cloud LLMs**: Chatbots relying solely on external APIs crash when API keys expire, hit rate limits, or encounter network outages.

### 1.2 Agentic Solution
**OmniConvert AI** introduces an autonomous, multi-tier intelligence system designed for zero-downtime customer support and mathematical rigor:
- **Base-Unit Normalization Pattern**: All conversions map through canonical SI base units in $O(1)$ algorithmic complexity.
- **Bilingual ReAct NLP Core**: Interprets English and colloquial Roman Urdu intents with 95%+ confidence.
- **24/7 Resilient Copilot**: Combines deterministic domain heuristics with optional live LLM inference, ensuring the assistant is perpetually active.
- **Auditable LaTeX Derivations**: Step-by-step mathematical proofs generated for every operation.

---

## 2. End-to-End System Architecture

```mermaid
flowchart TD
    User([Human Operator / Customer])
    
    subgraph UI_Gateway ["Interaction Gateway (Streamlit 1.42+)"]
        Tab1["Multi-Category Scientific Converter"]
        Tab2["Agentic NLU Converter (English & Roman Urdu)"]
        Tab3["24/7 Nova AI Copilot Chat Dock"]
    end
    
    subgraph Cognitive_Engine ["Cognitive Core (agent/)"]
        NLU_Parser["Agentic NLU Intent Parser (engine/nlp_parser.py)"]
        KnowledgeBase[("Embedded Knowledge Base (agent/knowledge_base.py)")]
        ReAct_Dispatcher["Nova Agent ReAct Dispatcher (agent/chatbot.py)"]
        Tool_Registry{"Tool Calling Router"}
    end

    subgraph LLM_Gateway ["Provider Gateway"]
        BuiltIn_Engine["Deterministic Zero-Downtime Engine"]
        GeminiClient["Google Gemini 2.5 Flash API"]
        OpenAIClient["OpenAI GPT-4o-mini API"]
    end

    subgraph Physics_Engine ["Mathematical Conversion Core (engine/converter.py)"]
        SINormalizer["SI Canonical Base Normalizer"]
        AffineTemp["Affine Thermodynamic Module"]
        LaTeXGen["LaTeX Formula & Proof Synthesizer"]
        AuditTrail[("Session Conversion Log & Export Engine")]
    end

    User -->|Prompts / Commands / Clicks| UI_Gateway
    Tab1 --> Physics_Engine
    Tab2 --> NLU_Parser
    Tab3 --> ReAct_Dispatcher
    
    NLU_Parser --> Tool_Registry
    ReAct_Dispatcher <--> KnowledgeBase
    ReAct_Dispatcher --> LLM_Gateway
    LLM_Gateway --> Tool_Registry
    
    Tool_Registry -->|Tool: convert_units| Physics_Engine
    Physics_Engine --> AuditTrail
    AuditTrail --> UI_Gateway
```

---

## 3. Cognitive Architecture & ReAct Agent Loop

The **Nova Copilot** implements a stateful ReAct (Reason + Act) loop designed specifically for technical conversions and customer support inquiries:

```text
┌────────────────────────────────────────────────────────┐
│                   Customer Input                       │
│    "Convert 150 km/h to mph and explain the formula"   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                1. PERCEPTION & INTENT                  │
│  - Detect Language: English vs Roman Urdu              │
│  - Extract Entities: value=150, src=km/h, tgt=mph      │
│  - Intent Class: CONVERSION_EXECUTION + FORMULA_REQ    │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                2. REASONING & DISPATCH                 │
│  - Check Dimensional Homogeneity (Speed == Speed)     │
│  - Select Internal Tool: `convert(150, "km/h", "mph")` │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                3. TOOL EXECUTION (ACT)                 │
│  - Compute Target Value: 93.2057 mph                   │
│  - Synthesize LaTeX: 150 km/h × (0.2778) ÷ (0.4470)    │
│  - Retrieve SI Reference: ISO 80000-3 Speed Standard   │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                4. RESPONSE SYNTHESIS                   │
│  - Render Result Card with Precision Rounding          │
│  - Inject LaTeX Derivation Block                       │
│  - Provide Customer Guidance & Related Suggestions     │
└────────────────────────────────────────────────────────┘
```

---

## 4. Multilingual NLP & Roman Urdu Semantic Engine

A core innovation of OmniConvert AI is native comprehension of **Roman Urdu**—the primary conversational dialect of millions across South Asia:

### 4.1 Linguistic Pattern Taxonomy
| Category | English Pattern | Roman Urdu Pattern | Normalized Action |
| :--- | :--- | :--- | :--- |
| **Imperative Conversion** | `convert 100 meters to feet` | `100 meter ko feet me convert karo` | Extract `(100.0, 'meter', 'foot')` |
| **Inquiry Conversion** | `how many km in 50 miles` | `50 miles kitne kilometer hote hain` | Extract `(50.0, 'mile', 'kilometer')` |
| **Temperature Mutation**| `change 35 celsius to f` | `35 celsius ko fahrenheit me badlo` | Extract `(35.0, 'celsius', 'fahrenheit')` |
| **Developer Portfolio** | `who built this project` | `ye project kisne banaya hai` | Trigger Developer Profile Card |
| **Support Help** | `how do I use precision` | `precision slider kaise use karein` | Trigger UX Guidance FAQ |

---

## 5. Tiered Mathematical Conversion Engine

To eliminate $O(N^2)$ pairwise dictionaries, all linear dimensions compute via a canonical intermediate base unit ($B$):

$$\text{Value}_{\text{base}} = \text{Value}_{\text{source}} \times F_{\text{source}\to\text{base}}$$

$$\text{Value}_{\text{target}} = \frac{\text{Value}_{\text{base}}}{F_{\text{target}\to\text{base}}}$$

### 5.1 Supported Physical Dimensions
1. **Length (Base: Meter)**: $m, km, cm, mm, \mu m, nm, mi, yd, ft, in, NM$
2. **Mass (Base: Kilogram)**: $kg, g, mg, \mu g, t, lb, oz, st, ct$
3. **Temperature (Base: Kelvin)**:
   - $K = °C + 273.15$
   - $K = (°F - 32) \times \frac{5}{9} + 273.15$
   - $K = °R \times \frac{5}{9}$
4. **Area (Base: Square Meter)**: $m^2, km^2, mi^2, yd^2, ft^2, in^2, ha, ac$
5. **Volume (Base: Liter)**: $L, mL, m^3, gal, qt, pt, cup, fl\ oz, tbsp, tsp$
6. **Speed (Base: Meter per Second)**: $m/s, km/h, mph, kn, ft/s, Mach$
7. **Time (Base: Second)**: $s, ms, \mu s, ns, min, h, d, wk, mo, yr$
8. **Digital Storage (Base: Byte)**:
   - Decimal (SI): $KB = 10^3\ B, MB = 10^6\ B, GB = 10^9\ B, TB = 10^{12}\ B$
   - Binary (IEC): $KiB = 2^{10}\ B, MiB = 2^{20}\ B, GiB = 2^{30}\ B, TiB = 2^{40}\ B$
9. **Energy (Base: Joule)**: $J, kJ, cal, kcal, Wh, kWh, eV, BTU$
10. **Pressure (Base: Pascal)**: $Pa, kPa, bar, psi, atm, Torr$

---

## 6. 24/7 Zero-Downtime Customer Support Specification

The customer support agent is architected around a **Tiered Fail-Safe Hierarchy**:

```text
               ┌─────────────────────────────┐
               │    Incoming Customer Query  │
               └──────────────┬──────────────┘
                              ▼
               ┌─────────────────────────────┐
               │  Is External API Key Set?   │
               └──────┬───────────────┬──────┘
                  YES │               │ NO / Network Failure
                      ▼               ▼
      ┌──────────────────────┐  ┌───────────────────────────────────┐
      │  Google Gemini 2.5 / │  │  Deterministic Cognitive Engine   │
      │  OpenAI GPT-4o-mini  │  │  - Zero API Key Required          │
      │  (Dynamic Reasoning) │  │  - 0 ms Network Latency           │
      └──────────────┬───────┘  │  - Direct ReAct Tool Dispatch     │
                     │          │  - Embedded Knowledge Base Search │
                     │          └─────────────────┬─────────────────┘
                     │                            │
                     └─────────────┬──────────────┘
                                   ▼
               ┌─────────────────────────────┐
               │  High-Fidelity Resolution   │
               │  (Markdown + LaTeX Output)  │
               └─────────────────────────────┘
```

---

## 7. Security Threat Model & Dimensional Guardrails

1. **Dimensional Mismatch Guard**: Rejects calculations between non-congruent dimensions (e.g. Length vs Mass) with HTTP-equivalent structured fault objects.
2. **Infinite Recursion Lock**: Conversions are strictly bounded to 2 steps (source $\to$ base $\to$ target).
3. **Floating Point Overflow / Underflow**: Bounds checked against IEEE 754 limits ($> 10^{308}$ or $< 10^{-308}$).
4. **Injection Sanitation**: Regex sanitization prevents command injection or arbitrary execution in natural language prompt fields.

---

## 8. Programmatic SDK & API Specification

OmniConvert AI can be embedded into external Python workflows or microservices:

```python
from engine.converter import convert, UnitCategory

# Standard high-precision conversion
result = convert(
    value=75.0,
    from_unit="mile_per_hour",
    to_unit="kilometer_per_hour"
)

if result.success:
    print(f"Result: {result.target_value} {result.target_symbol}")
    print(f"LaTeX Proof: {result.formula_latex}")
else:
    print(f"Error: {result.error_message}")
```

```python
from engine.nlp_parser import parse_conversion_query

# Natural Language Parsing in Roman Urdu
nlu_res = parse_conversion_query("100 meter ko foot me badlo")
print(f"Detected Language: {nlu_res.detected_language}")
print(f"Output: {nlu_res.conversion_result.target_value} ft")
```

---

## 9. Test Suite & Verification Matrix

The test harness in `tests/test_converter.py` provides 100% test pass coverage:

| Test Case | Domain | Assertion | Result |
| :--- | :--- | :--- | :--- |
| `test_length_conversion` | Length | $1\text{ km} = 1000\text{ m}$, $1\text{ mi} = 1609.344\text{ m}$ | **PASSED** |
| `test_same_unit_conversion` | Identity | $42.5\text{ m} \to 42.5\text{ m}$ (1:1 ratio) | **PASSED** |
| `test_mass_conversion` | Mass | $2.5\text{ kg} = 2500\text{ g}$, $10\text{ lb} \approx 4.5359\text{ kg}$ | **PASSED** |
| `test_temperature_affine` | Thermodynamics | $0\text{ °C} = 32\text{ °F}$, $-40\text{ °C} = -40\text{ °F}$ | **PASSED** |
| `test_storage_standards` | Digital Storage | $1\text{ GB} = 1000\text{ MB}$, $1\text{ GiB} = 1024\text{ MiB}$ | **PASSED** |
| `test_dimensional_mismatch`| Safety Boundary | Rejects $10\text{ m} \to\text{kg}$ with clear error | **PASSED** |
| `test_roman_urdu_parsing` | NLP Engine | Correctly parses Roman Urdu command strings | **PASSED** |
| `test_chatbot_tool_call` | Agentic Copilot | Dispatches live conversion tools in chat | **PASSED** |
| `test_portfolio_inquiry` | Developer Profile | Correctly outputs Hadi Seelro portfolio links | **PASSED** |

---

<div align="center">
<b>OmniConvert AI Specification • Standard IEEE 830 / ISO 80000</b><br/>
Engineered by Hadi Seelro • Open Source Software
</div>
