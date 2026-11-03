"""
OmniConvert AI - 24/7 Autonomous Customer Support Copilot
Provides zero-downtime deterministic tool calling and multi-provider LLM integration.
"""
import os
import re
from typing import List, Dict, Any, Optional
from engine.converter import (
    convert,
    get_categories,
    get_units_for_category,
    find_unit_category,
    ConversionResult
)
from engine.nlp_parser import parse_conversion_query
from .knowledge_base import PROJECT_KNOWLEDGE_BASE, get_system_prompt


class OmniAgentChatbot:
    """
    24/7 Resilient Agentic Chatbot for Customer Support and Conversion Tool-Calling.
    Guarantees continuous 24/7 live operation with an internal cognitive fallback
    and optional Google Gemini / OpenAI scaling.
    """

    def __init__(self, provider: str = "auto", api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.system_prompt = get_system_prompt()
        self.knowledge = PROJECT_KNOWLEDGE_BASE

    def process_message(
        self,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Main dispatch entrypoint for user messages.
        Returns a dictionary with:
        - 'response': str (Markdown/LaTeX message)
        - 'tool_called': bool
        - 'tool_result': Optional[ConversionResult]
        - 'provider_used': str
        """
        msg_clean = user_message.strip()
        if not msg_clean:
            return {
                "response": "Hello! I am **Nova**, your 24/7 OmniConvert AI Copilot. How can I assist you with unit conversions, customer support, or system specs today?",
                "tool_called": False,
                "tool_result": None,
                "provider_used": "Built-in 24/7 Engine"
            }

        # Check if the user is asking to convert a unit directly
        nlp_res = parse_conversion_query(msg_clean)
        if nlp_res.success and nlp_res.conversion_result:
            conv = nlp_res.conversion_result
            reply = (
                f"### 🎯 Real-Time Conversion Result\n\n"
                f"**{conv.source_value:g} {conv.source_unit} ({conv.source_symbol})** is equal to:\n\n"
                f"## `{conv.target_value:.6g} {conv.target_symbol}` ({conv.target_unit})\n\n"
                f"**Mathematical Formula:**\n"
                f"$${conv.formula_latex}$$\n\n"
                f"**Calculation Steps:**\n```text\n{conv.step_by_step}\n```\n"
                f"Is there anything else you would like me to convert or explain?"
            )
            return {
                "response": reply,
                "tool_called": True,
                "tool_result": conv,
                "provider_used": "OmniEngine ReAct Parser"
            }

        # If LLM API key is present and requested, attempt Live LLM call
        if self.api_key and self.provider in ("gemini", "openai", "auto"):
            llm_result = self._try_llm_response(msg_clean, chat_history)
            if llm_result:
                return llm_result

        # Fallback to Built-in Zero-Downtime Cognitive Engine
        return self._built_in_cognitive_response(msg_clean)

    def _try_llm_response(
        self,
        user_message: str,
        chat_history: Optional[List[Dict[str, str]]]
    ) -> Optional[Dict[str, Any]]:
        """Attempts to call Gemini or OpenAI API safely."""
        try:
            # Check for OpenAI or Gemini
            if (self.provider == "gemini" or self.provider == "auto") and (os.getenv("GEMINI_API_KEY") or self.api_key):
                # Try google-genai / openai client
                key = self.api_key or os.getenv("GEMINI_API_KEY")
                from openai import OpenAI
                # Use Gemini's OpenAI-compatible endpoint
                client = OpenAI(
                    api_key=key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                messages = [{"role": "system", "content": self.system_prompt}]
                if chat_history:
                    for h in chat_history[-6:]:  # Keep recent context bounded
                        messages.append({"role": h["role"], "content": h["content"]})
                messages.append({"role": "user", "content": user_message})

                resp = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=600
                )
                return {
                    "response": resp.choices[0].message.content,
                    "tool_called": False,
                    "tool_result": None,
                    "provider_used": "Google Gemini 2.5 Flash (Live)"
                }
        except Exception:
            pass  # Seamlessly fall back to built-in engine if network/quota fails

        try:
            if (self.provider == "openai" or self.provider == "auto") and (os.getenv("OPENAI_API_KEY") or self.api_key):
                from openai import OpenAI
                key = self.api_key or os.getenv("OPENAI_API_KEY")
                client = OpenAI(api_key=key)
                messages = [{"role": "system", "content": self.system_prompt}]
                if chat_history:
                    for h in chat_history[-6:]:
                        messages.append({"role": h["role"], "content": h["content"]})
                messages.append({"role": "user", "content": user_message})

                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=600
                )
                return {
                    "response": resp.choices[0].message.content,
                    "tool_called": False,
                    "tool_result": None,
                    "provider_used": "OpenAI GPT-4o-mini (Live)"
                }
        except Exception:
            pass

        return None

    def _built_in_cognitive_response(self, text: str) -> Dict[str, Any]:
        """
        Deterministic, 24/7 high-fidelity customer support handler.
        Understands intent in English and Roman Urdu.
        """
        low = text.lower()

        # 1. Developer / Portfolio / Creator queries
        if any(w in low for w in ["who made", "developer", "creator", "portfolio", "hadi", "seelro", "author", "hire"]):
            dev = self.knowledge["developer"]
            reply = (
                f"### 👨‍💻 Developer & Architectural Profile\n\n"
                f"**{self.knowledge['system_name']}** was architected and built by **{dev['name']}**.\n\n"
                f"- **Role**: {dev['title']}\n"
                f"- **Specialization**: {dev['portfolio_summary']}\n"
                f"- **GitHub Profile**: [{dev['github']}]({dev['github']})\n\n"
                f"**Portfolio Highlights in this Project:**\n"
                f"1. **Agentic ReAct Architecture**: Deterministic tool execution with math proofs.\n"
                f"2. **24/7 Zero-Downtime Copilot**: Autonomous customer support that never crashes.\n"
                f"3. **Bilingual NLU**: English & Roman Urdu natural language understanding.\n"
                f"4. **High-Precision Physics**: Conforms to NIST SP 811 & ISO 80000 standards.\n\n"
                f"Feel free to check out his other autonomous agents on GitHub or discuss custom AI projects!"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # 2. Greetings
        if any(w in low for w in ["hi", "hello", "hey", "salam", "assalam", "adaab", "kaise ho", "kya haal"]):
            reply = (
                f"### 👋 Greetings! I'm Nova, your 24/7 AI Copilot.\n\n"
                f"Welcome to **{self.knowledge['system_name']}**! Main aapko 10 categories me 60+ physical units convert karne, formulas samajhne aur support queries solve karne me guide kar sakti hoon.\n\n"
                f"**Popular Actions you can try:**\n"
                f"- *'Convert 100 meters to feet'* ya *'50 km ko miles me badlo'*\n"
                f"- *'Explain the temperature conversion formula'*\n"
                f"- *'What units are supported in Digital Storage?'*\n"
                f"- *'How can I integrate this in Python?'*\n\n"
                f"Aap mujhse English ya Roman Urdu kisi me bhi baat kar sakte hain. How can I help you today?"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # 3. Categories & Supported Units
        if any(w in low for w in ["category", "categories", "supported units", "units list", "kya kya convert", "list units"]):
            lines = []
            for cat, units in self.knowledge["categories_and_units"].items():
                lines.append(f"- **{cat}**: {', '.join(units[:5])}...")
            cats_formatted = "\n".join(lines)
            reply = (
                f"### 📚 Supported Physical Categories & Units\n\n"
                f"OmniConvert AI supports **10 comprehensive domains**:\n\n"
                f"{cats_formatted}\n\n"
                f"You can choose any category from the top tabs in the main converter or simply ask me to convert in plain text!"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # 4. Temperature formula explanation
        if "temperature" in low or "celsius" in low or "fahrenheit" in low or "formula" in low:
            reply = (
                f"### 🌡️ Temperature Conversion Mathematical Principles\n\n"
                f"Unlike standard linear units where a simple multiplier suffices, temperature scales have distinct zero points and degree intervals:\n\n"
                f"1. **Celsius to Fahrenheit**:\n"
                f"   $$°F = (°C \\times \\frac{{9}}{{5}}) + 32$$\n\n"
                f"2. **Fahrenheit to Celsius**:\n"
                f"   $$°C = (°F - 32) \\times \\frac{{5}}{{9}}$$\n\n"
                f"3. **Celsius to Kelvin (Absolute SI)**:\n"
                f"   $$K = °C + 273.15$$\n\n"
                f"4. **Fahrenheit to Kelvin**:\n"
                f"   $$K = (°F - 32) \\times \\frac{{5}}{{9}} + 273.15$$\n\n"
                f"*Try asking me: 'Convert 98.6 fahrenheit to celsius' to see the exact numbers in action!*"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # 5. Python SDK / API integration
        if any(w in low for w in ["api", "sdk", "python", "code", "integrate", "import"]):
            reply = (
                f"### 🐍 Programmatic Integration & Python SDK\n\n"
                f"You can easily embed OmniConvert AI's calculation engine in any Python backend:\n\n"
                f"```python\n"
                f"from engine.converter import convert\n\n"
                f"# High-precision conversion with formula verification\n"
                f"result = convert(150.0, from_unit='kilometer_per_hour', to_unit='mile_per_hour')\n\n"
                f"if result.success:\n"
                f"    print(f'Converted: {result.target_value:.2f} {result.target_symbol}')\n"
                f"    print(f'Formula: {result.formula_latex}')\n"
                f"else:\n"
                f"    print(f'Error: {result.error_message}')\n"
                f"```\n\n"
                f"Check **SPEC.md** for complete class definitions and IEEE 830 architectural contracts!"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # 6. Customer Support / Bug / Help
        if any(w in low for w in ["support", "help", "bug", "issue", "contact", "problem", "feedback", "masla"]):
            reply = (
                f"### 🛡️ 24/7 Customer Care & Support\n\n"
                f"I am active 24/7 to resolve any issues:\n\n"
                f"1. **Dimensional Mismatch**: Ensure you are not converting between incompatible physical dimensions (e.g. Length to Mass).\n"
                f"2. **Precision Customization**: In the main web view, use the **Precision Slider** to increase decimal places up to 10 or switch to Scientific Notation.\n"
                f"3. **Missing Unit Request**: If you need specialized units (e.g. Astronomical Units or Crypto currency rates), open an issue on the repository: [{self.knowledge['developer']['github']}]({self.knowledge['developer']['github']}).\n\n"
                f"Can you describe your issue in detail so I can help?"
            )
            return {"response": reply, "tool_called": False, "tool_result": None, "provider_used": "Built-in 24/7 Copilot"}

        # Default helpful guide
        reply = (
            f"I have received your query: *\"{text}\"*.\n\n"
            f"As your **OmniConvert AI Copilot**, I can:\n"
            f"- 🔄 **Execute Real-time Conversions**: e.g., *'Convert 500 MB to GB'* or *'35 celsius ko fahrenheit me badlo'*.\n"
            f"- 📐 **Explain Math**: Ask for step-by-step mathematical proofs and LaTeX formulas.\n"
            f"- 💡 **System Architecture**: Inquire about the Agentic ReAct loop, NIST standards, or Python SDK.\n"
            f"- 👨‍💻 **Developer Credentials**: Ask about **Hadi Seelro** and his Agentic AI portfolio.\n\n"
            f"What would you like to explore next?"
        )
        return {
            "response": reply,
            "tool_called": False,
            "tool_result": None,
            "provider_used": "Built-in 24/7 Copilot"
        }
