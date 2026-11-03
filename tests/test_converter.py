"""
OmniConvert AI - Automated Verification & Test Suite
Validates mathematical accuracy, temperature transformations, NLP parsing, and 24/7 Agentic Copilot.
"""
import pytest
from engine.converter import convert, UnitCategory, find_unit_category
from engine.nlp_parser import parse_conversion_query
from agent.chatbot import OmniAgentChatbot


class TestMathematicalConverter:
    """Tests core mathematical accuracy and dimensional homogeneity."""

    def test_length_conversion(self):
        # 1 kilometer = 1000 meters
        res = convert(1.0, "kilometer", "meter")
        assert res.success is True
        assert res.target_value == pytest.approx(1000.0, rel=1e-6)

        # 1 mile = 1609.344 meters
        res_mi = convert(1.0, "mile", "meter")
        assert res_mi.success is True
        assert res_mi.target_value == pytest.approx(1609.344, rel=1e-6)

    def test_same_unit_conversion(self):
        # Converting meter to meter should succeed with ratio 1.0
        res = convert(42.5, "meter", "meter")
        assert res.success is True
        assert res.target_value == pytest.approx(42.5)

    def test_mass_conversion(self):
        # 1 kg = 1000 g
        res = convert(2.5, "kilogram", "gram")
        assert res.success is True
        assert res.target_value == pytest.approx(2500.0, rel=1e-6)

        # 1 lb ~ 0.45359237 kg
        res_lb = convert(10.0, "pound", "kilogram")
        assert res_lb.success is True
        assert res_lb.target_value == pytest.approx(4.5359237, rel=1e-5)

    def test_temperature_affine_conversions(self):
        # 0 °C = 32 °F
        res_c_to_f = convert(0.0, "celsius", "fahrenheit")
        assert res_c_to_f.success is True
        assert res_c_to_f.target_value == pytest.approx(32.0, rel=1e-5)

        # 100 °C = 212 °F
        res_boil = convert(100.0, "celsius", "fahrenheit")
        assert res_boil.success is True
        assert res_boil.target_value == pytest.approx(212.0, rel=1e-5)

        # -40 °C = -40 °F (The intersection point)
        res_neg = convert(-40.0, "celsius", "fahrenheit")
        assert res_neg.success is True
        assert res_neg.target_value == pytest.approx(-40.0, rel=1e-5)

        # 0 °C = 273.15 K
        res_k = convert(0.0, "celsius", "kelvin")
        assert res_k.success is True
        assert res_k.target_value == pytest.approx(273.15, rel=1e-5)

    def test_digital_storage_decimal_and_binary(self):
        # 1 GB = 1000 MB (decimal)
        res_gb = convert(1.0, "gigabyte", "megabyte")
        assert res_gb.success is True
        assert res_gb.target_value == pytest.approx(1000.0, rel=1e-6)

        # 1 GiB = 1024 MiB (binary)
        res_gib = convert(1.0, "gibibyte", "mebibyte")
        assert res_gib.success is True
        assert res_gib.target_value == pytest.approx(1024.0, rel=1e-6)

    def test_dimensional_mismatch_error_handling(self):
        # Length to Mass is physically invalid
        res = convert(10.0, "meter", "kilogram")
        assert res.success is False
        assert "Dimensional mismatch" in res.error_message


class TestAgenticNLPParser:
    """Tests the Natural Language Understanding parser in English and Roman Urdu."""

    def test_english_query_parsing(self):
        query = "convert 100 meters to feet"
        result = parse_conversion_query(query)
        assert result.success is True
        assert result.source_value == 100.0
        assert result.detected_language == "English"
        assert result.conversion_result.target_value == pytest.approx(328.084, rel=1e-3)

    def test_roman_urdu_conversion_query(self):
        query = "50 miles ko kilometer me convert karo"
        result = parse_conversion_query(query)
        assert result.success is True
        assert result.source_value == 50.0
        assert result.detected_language == "Roman Urdu"
        assert result.conversion_result.target_value == pytest.approx(80.4672, rel=1e-3)

    def test_roman_urdu_question_query(self):
        query = "500 gram kitne kg hote hain"
        result = parse_conversion_query(query)
        assert result.success is True
        assert result.source_value == 500.0
        assert result.conversion_result.target_value == pytest.approx(0.5, rel=1e-4)


class TestAgenticCopilot:
    """Tests the 24/7 autonomous chatbot and tool calling capabilities."""

    def test_chatbot_tool_execution(self):
        bot = OmniAgentChatbot()
        response = bot.process_message("Convert 250 km/h to mph")
        assert response["tool_called"] is True
        assert response["tool_result"] is not None
        assert response["tool_result"].target_value == pytest.approx(155.342, rel=1e-3)
        assert "Real-Time Conversion Result" in response["response"]

    def test_chatbot_portfolio_query(self):
        bot = OmniAgentChatbot()
        response = bot.process_message("Who is the developer of this project?")
        assert "Hadi Seelro" in response["response"]
        assert "https://github.com/SainBux-HadiSeelro" in response["response"]

    def test_chatbot_faq_and_greetings(self):
        bot = OmniAgentChatbot()
        response = bot.process_message("salam kaise ho")
        assert "Nova" in response["response"]
        assert "OmniConvert AI" in response["response"]
