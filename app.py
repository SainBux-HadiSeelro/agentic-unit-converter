"""
OmniConvert AI - Fast, High-Precision Unit Intelligence & 24/7 AI Copilot
Conforms to NIST SP 811, BIPM SI & ISO 80000 physical standards.
"""
import streamlit as st
import json
import csv
import io
from datetime import datetime
from typing import Optional, List, Dict, Any

from engine.converter import (
    convert,
    get_categories,
    get_units_for_category,
    CATEGORY_ICONS,
    UnitCategory,
    find_unit_category
)
from engine.nlp_parser import parse_conversion_query
from agent.chatbot import OmniAgentChatbot
from agent.knowledge_base import PROJECT_KNOWLEDGE_BASE, get_quick_prompts

# -----------------------------------------------------------------------------
# Fast In-Memory Helpers & Resource Caches (Zero-Lag Execution)
# -----------------------------------------------------------------------------
@st.cache_resource
def get_ai_copilot() -> OmniAgentChatbot:
    """Caches 24/7 AI Copilot in memory to eliminate instantiation overhead."""
    return OmniAgentChatbot(provider="auto")

def export_history_csv(history: list) -> bytes:
    """Fast, zero-overhead CSV generation using Python standard library."""
    data = history if history else [{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": "Length",
        "From": "1 km",
        "To": "1000 m",
        "Formula": "1 km = 1000 m"
    }]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Timestamp", "Category", "From", "To", "Formula"])
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue().encode("utf-8")

def export_history_json(history: list) -> bytes:
    """Fast, zero-overhead JSON serialization."""
    data = history if history else [{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": "Length",
        "From": "1 km",
        "To": "1000 m",
        "Formula": "1 km = 1000 m"
    }]
    return json.dumps(data, indent=2).encode("utf-8")

# -----------------------------------------------------------------------------
# 1. Page Configuration & Guaranteed Visibility Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OmniConvert AI | Smart Unit Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
/* =========================================================================
   1. UNIVERSAL ROOT & APP BACKGROUND
   ========================================================================= */
html, body, [class*="css"], .stApp {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    background-color: #0b0f19 !important;
    color: #ffffff !important;
}

/* =========================================================================
   2. SIDEBAR - DEEP DARK & 100% PURE WHITE TEXT
   ========================================================================= */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
div[data-testid="stSidebarUserContent"] {
    background-color: #0d1322 !important;
    background: #0d1322 !important;
    border-right: 2px solid #1e293b !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* =========================================================================
   3. BASEWEB SELECTBOX & DROPDOWN - FIXED INVISIBLE LABELS & OPTIONS
   ========================================================================= */
div[data-baseweb="select"] > div {
    background-color: #162032 !important;
    border: 1.5px solid #3b82f6 !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Dropdown popover menu and option items */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background-color: #111827 !important;
    background: #111827 !important;
    color: #ffffff !important;
}

li[role="option"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

li[role="option"]:hover,
li[aria-selected="true"] {
    background-color: #0284c7 !important;
    color: #ffffff !important;
}

/* =========================================================================
   4. INPUT FIELDS (QUANTITY & TEXT)
   ========================================================================= */
div[data-baseweb="input"] {
    background-color: #162032 !important;
    border: 1.5px solid #3b82f6 !important;
    border-radius: 10px !important;
}

div[data-baseweb="input"] input {
    color: #ffffff !important;
    background-color: transparent !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

label, p, span, strong, b {
    color: #f1f5f9 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

.stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label {
    color: #ffffff !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    -webkit-text-fill-color: #ffffff !important;
    margin-bottom: 6px !important;
}

/* =========================================================================
   5. BUTTONS & DOWNLOAD BUTTONS
   ========================================================================= */
.stButton > button {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover {
    background-color: #0284c7 !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
}

.stButton > button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* DOWNLOAD BUTTONS */
.stDownloadButton > button,
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    padding: 12px 24px !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.45) !important;
}

.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    background: #0ea5e9 !important;
    border-color: #ffffff !important;
    color: #ffffff !important;
    box-shadow: 0 6px 22px rgba(56, 189, 248, 0.6) !important;
}

.stDownloadButton > button *,
[data-testid="stDownloadButton"] > button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* =========================================================================
   6. AESTHETIC ANIMATED FLOATING BUTTON (CYBER SHIMMER + RADAR PULSE + BOUNCE)
   ========================================================================= */

/* Floating Launcher in Bottom-Right Corner */
.st-key-fab_chat_trigger,
div.st-key-fab_chat_trigger,
div[data-testid="stButton"].st-key-fab_chat_trigger {
    position: fixed !important;
    bottom: 40px !important;
    right: 24px !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
}

.st-key-fab_chat_trigger button,
.st-key-fab_chat_trigger > button,
div.st-key-fab_chat_trigger button {
    background: linear-gradient(
        115deg,
        #0284c7 0%,
        #6366f1 22%,
        #ec4899 45%,
        rgba(255, 255, 255, 0.95) 52%,
        #a855f7 60%,
        #06b6d4 82%,
        #0284c7 100%
    ) !important;
    background-size: 280% 100% !important;
    color: #ffffff !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 9999px !important;
    padding: 14px 28px !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.4px !important;
    cursor: pointer !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    box-shadow: 0 10px 35px rgba(99, 102, 241, 0.6), 0 0 20px rgba(56, 189, 248, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.65) !important;
    animation: shimmerStreak 2.6s linear infinite, bounceFloat 2.2s ease-in-out infinite, radarPulse 2s ease-out infinite, borderFlash 3s ease infinite !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.st-key-fab_chat_trigger button *,
.st-key-fab_chat_trigger > button *,
div.st-key-fab_chat_trigger button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.02rem !important;
    letter-spacing: 0.4px !important;
    text-shadow: 0 0 8px rgba(255, 255, 255, 0.8), 0 0 16px rgba(56, 189, 248, 0.8) !important;
    animation: textGlowPulse 2s ease-in-out infinite alternate !important;
}

.st-key-fab_chat_trigger button:hover,
.st-key-fab_chat_trigger > button:hover,
div.st-key-fab_chat_trigger button:hover {
    transform: translateY(-8px) scale(1.08) !important;
    border-color: #ffffff !important;
    box-shadow: 0 22px 55px rgba(99, 102, 241, 0.9), 0 0 35px rgba(236, 72, 153, 0.85), inset 0 1px 4px rgba(255, 255, 255, 1) !important;
    animation: shimmerStreak 1.4s linear infinite, radarPulse 1.2s ease-out infinite, borderFlash 1.5s ease infinite !important;
}

.st-key-fab_chat_trigger button:active,
.st-key-fab_chat_trigger > button:active,
div.st-key-fab_chat_trigger button:active {
    transform: translateY(2px) scale(0.95) !important;
}

@keyframes shimmerStreak {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

@keyframes bounceFloat {
    0%, 100% {
        transform: translateY(0px) scale(1);
    }
    50% {
        transform: translateY(-10px) scale(1.04);
    }
}

@keyframes radarPulse {
    0% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.85),
                    0 0 0 0 rgba(236, 72, 153, 0.7),
                    0 8px 30px rgba(99, 102, 241, 0.6);
    }
    60% {
        box-shadow: 0 0 0 18px rgba(56, 189, 248, 0),
                    0 0 0 32px rgba(236, 72, 153, 0),
                    0 14px 45px rgba(99, 102, 241, 0.85);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0),
                    0 0 0 0 rgba(236, 72, 153, 0),
                    0 8px 30px rgba(99, 102, 241, 0.6);
    }
}

@keyframes borderFlash {
    0%, 100% { border-color: #38bdf8; }
    33% { border-color: #c084fc; }
    66% { border-color: #f472b6; }
}

@keyframes textGlowPulse {
    0% {
        text-shadow: 0 0 6px rgba(255, 255, 255, 0.6), 0 0 12px rgba(56, 189, 248, 0.7);
    }
    100% {
        text-shadow: 0 0 14px rgba(255, 255, 255, 0.95), 0 0 24px rgba(236, 72, 153, 0.9);
    }
}

/* SIDE CHAT WIDGET CARD (OPENS ABOVE THE BUTTON ON THE RIGHT CORNER) */
.st-key-side_chat_card {
    position: fixed !important;
    bottom: 118px !important;
    right: 24px !important;
    width: 410px !important;
    max-width: calc(100vw - 32px) !important;
    height: 530px !important;
    max-height: calc(100vh - 140px) !important;
    background: #0d1322 !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9), 0 0 30px rgba(56, 189, 248, 0.35) !important;
    z-index: 999998 !important;
    padding: 16px !important;
    display: flex !important;
    flex-direction: column !important;
    animation: slideInCorner 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

@keyframes slideInCorner {
    from {
        opacity: 0;
        transform: translateY(25px) scale(0.96);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* =========================================================================
   TWO-SIDED CHAT BUBBLES WITH DISTINCT COLORS & SIDES
   ========================================================================= */

/* USER BUBBLE: RIGHT-ALIGNED (ROYAL BLUE GRADIENT) */
.chat-row-user {
    display: flex;
    justify-content: flex-end;
    width: 100%;
    margin-bottom: 10px;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: 16px 16px 3px 16px !important;
    padding: 10px 14px !important;
    max-width: 84% !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
    text-align: left !important;
}

.chat-bubble-user * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* AGENT BUBBLE: LEFT-ALIGNED (DARK SLATE WITH CYAN BORDER) */
.chat-row-agent {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    margin-bottom: 10px;
}

.chat-bubble-agent {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    color: #f8fafc !important;
    border: 1.5px solid #38bdf8 !important;
    border-radius: 16px 16px 16px 3px !important;
    padding: 12px 16px !important;
    max-width: 88% !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
    text-align: left !important;
}

.chat-bubble-agent strong {
    color: #38bdf8 !important;
    -webkit-text-fill-color: #38bdf8 !important;
}

.chat-bubble-agent div {
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}

/* Hero & Results Card */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(14, 165, 233, 0.25);
    border: 1px solid #38bdf8;
    color: #38bdf8 !important;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.live-indicator-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px #10b981;
}

.result-card-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid #38bdf8;
    border-radius: 18px;
    padding: 24px 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    margin-top: 6px;
}

.result-card-label {
    font-size: 0.9rem;
    color: #38bdf8 !important;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.result-card-value {
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff !important;
    line-height: 1.15;
    margin: 6px 0 12px 0;
    word-break: break-word;
}

.result-card-badge {
    display: inline-block;
    background: #0284c7;
    color: #ffffff !important;
    padding: 8px 22px;
    border-radius: 9999px;
    font-size: 1.15rem;
    font-weight: 800;
}

/* Tabs Styling */
button[data-baseweb="tab"] {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #cbd5e1 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = [
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": "Length",
            "From": "1 km",
            "To": "1000 m",
            "Formula": "1 km = 1000 m"
        }
    ]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Hello! I am Nova, your 24/7 AI Unit Copilot.**\n\n"
                "I convert units, explain formulas, and answer physics questions in **English** or **Roman Urdu**!\n\n"
                "Try asking:\n"
                "- *'Convert 120 km/h to mph'*\n"
                "- *'50 miles ko km me convert karo'*\n"
                "- *'Explain temperature conversion formula'*"
            ),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    ]

if "source_value" not in st.session_state:
    st.session_state.source_value = 1.0

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# -----------------------------------------------------------------------------
# 3. Sidebar Controls (Clean Settings)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; padding: 6px 0;">
            <span style="font-size: 2.2rem;">⚡</span>
            <div>
                <h2 style="margin: 0; padding: 0; font-size: 1.35rem; font-weight: 800; color: #ffffff !important;">OmniConvert AI</h2>
                <span style="font-size: 0.78rem; color: #38bdf8 !important; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;">Smart Converter</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-badge">
            <span class="live-indicator-dot"></span> System Ready
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚙️ Display Settings")
    
    precision = st.selectbox(
        "Decimal Places:",
        options=[2, 3, 4, 6, 8],
        index=2,
        help="Number of decimal places displayed in results."
    )
    use_scientific = st.checkbox("Scientific Notation (1.0 × 10ⁿ)", value=False)

    st.markdown("---")
    st.markdown("""
        <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 12px;">
            <span style="color: #38bdf8; font-weight: 700; font-size: 0.9rem;">🤖 24/7 AI Copilot Active</span>
            <p style="color: #cbd5e1; font-size: 0.82rem; margin: 4px 0 0 0;">
                Click the floating <b>✨ Ask Nova AI</b> button anytime. 100% free, zero key required.
            </p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Modern Header (Full Width & Clean)
# -----------------------------------------------------------------------------
st.markdown("""
    <div>
        <div class="hero-badge"><span class="live-indicator-dot"></span> NIST SP 811 & ISO 80000 Physical Standards</div>
        <h1 style="margin: 0; font-size: 2.4rem; font-weight: 800; color: #ffffff !important;">
            Smart <span style="color: #38bdf8;">Unit Converter</span>
        </h1>
        <p style="color: #cbd5e1; font-size: 1.05rem; margin-top: 4px; margin-bottom: 20px;">
            High-precision, instantaneous calculations across 10 physical dimensions.
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Main Converter Section (Clean Full-Width Tabs)
# -----------------------------------------------------------------------------
tab_quick, tab_nlu = st.tabs(["⚡ Quick Unit Converter", "💬 Smart Language (Urdu & English)"])

# ---------------- TAB 1: Quick Unit Converter ----------------
with tab_quick:
    categories = get_categories()
    category_labels = [f"{CATEGORY_ICONS.get(cat, '📐')} {cat}" for cat in categories]
    selected_cat_idx = st.selectbox(
        "Select Category:",
        options=range(len(categories)),
        format_func=lambda i: category_labels[i],
        index=0,
        key="cat_selector_main"
    )
    selected_category = categories[selected_cat_idx]

    units_dict = get_units_for_category(selected_category)
    unit_keys = list(units_dict.keys())
    unit_display_names = [f"{units_dict[k].name} ({units_dict[k].symbol})" for k in unit_keys]

    st.markdown("<br>", unsafe_allow_html=True)

    from_key_state = f"from_{selected_category}"
    to_key_state = f"to_{selected_category}"

    if from_key_state not in st.session_state:
        st.session_state[from_key_state] = 0
    if to_key_state not in st.session_state:
        st.session_state[to_key_state] = 1 if len(unit_keys) > 1 else 0

    col_c1, col_swap, col_c2 = st.columns([5, 1.4, 5])

    with col_c1:
        st.markdown(f"**From ({selected_category}):**")
        from_idx = st.selectbox(
            "Source Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            key=from_key_state,
            label_visibility="collapsed"
        )
        source_key = unit_keys[from_idx]

        source_val = st.number_input(
            "Enter Quantity:",
            value=float(st.session_state.source_value),
            format="%.4f",
            key=f"val_{selected_category}"
        )
        st.session_state.source_value = source_val

        # Quick preset buttons
        p1, p2, p3, p4 = st.columns(4)
        if p1.button("+1", use_container_width=True, key=f"btn_p1_{selected_category}"):
            st.session_state.source_value = source_val + 1.0
            st.rerun()
        if p2.button("+10", use_container_width=True, key=f"btn_p2_{selected_category}"):
            st.session_state.source_value = source_val + 10.0
            st.rerun()
        if p3.button("100", use_container_width=True, key=f"btn_p3_{selected_category}"):
            st.session_state.source_value = 100.0
            st.rerun()
        if p4.button("Reset", use_container_width=True, key=f"btn_p4_{selected_category}"):
            st.session_state.source_value = 1.0
            st.rerun()

    with col_swap:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⇄ Swap", help="Swap Source and Target Units", use_container_width=True, key=f"btn_swap_{selected_category}"):
            curr_from = st.session_state[from_key_state]
            curr_to = st.session_state[to_key_state]
            st.session_state[from_key_state] = curr_to
            st.session_state[to_key_state] = curr_from
            st.rerun()

    with col_c2:
        st.markdown(f"**To ({selected_category}):**")
        to_idx = st.selectbox(
            "Target Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            key=to_key_state,
            label_visibility="collapsed"
        )
        target_key = unit_keys[to_idx]

        conversion = convert(source_val, source_key, target_key)

        if conversion.success:
            if use_scientific:
                formatted_val = f"{conversion.target_value:.{precision}e}"
            else:
                formatted_val = f"{conversion.target_value:,.{precision}f}".rstrip('0').rstrip('.') if '.' in f"{conversion.target_value:.{precision}f}" else f"{conversion.target_value:.0f}"

            st.markdown(f"""
                <div class="result-card-box">
                    <div class="result-card-label">Converted Result</div>
                    <div class="result-card-value">{formatted_val}</div>
                    <div class="result-card-badge">
                        {conversion.target_unit} ({conversion.target_symbol})
                    </div>
                </div>
            """, unsafe_allow_html=True)

            history_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Category": selected_category,
                "From": f"{source_val:g} {conversion.source_symbol}",
                "To": f"{conversion.target_value:.6g} {conversion.target_symbol}",
                "Formula": conversion.formula_latex
            }
            if not st.session_state.conversion_history or st.session_state.conversion_history[-1]["From"] != history_entry["From"] or st.session_state.conversion_history[-1]["To"] != history_entry["To"]:
                st.session_state.conversion_history.append(history_entry)
        else:
            st.error(f"⚠️ {conversion.error_message}")

    if conversion.success:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📐 View Step-by-Step Formula & Explanation", expanded=False):
            st.markdown("**Mathematical Formula:**")
            clean_formula = (
                conversion.formula_latex
                .replace("\\text", "")
                .replace("{", "")
                .replace("}", "")
                .replace("\\times", " × ")
                .replace("\\frac", "")
            ).strip()
            st.markdown(f"""
            <div style="background: #111827; border: 1.5px solid #0284c7; border-radius: 8px; padding: 10px 14px; font-family: monospace; font-size: 1.05rem; color: #38bdf8 !important; font-weight: 700; margin-bottom: 12px;">
                {clean_formula}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Calculation Steps:**")
            st.code(conversion.step_by_step, language="text")

# ---------------- TAB 2: Smart NLU (Urdu & English) ----------------
with tab_nlu:
    st.markdown("**Click an example to test:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    test_query = ""
    if q_col1.button("🚗 120 km/h to mph", use_container_width=True, key="btn_ex1"):
        test_query = "convert 120 km/h to mph"
    if q_col2.button("🇵🇰 50 miles ko km me badlo", use_container_width=True, key="btn_ex2"):
        test_query = "50 miles ko km me badlo"
    if q_col3.button("🌡️ 100 celsius ko fahrenheit me badlo", use_container_width=True, key="btn_ex3"):
        test_query = "100 celsius ko fahrenheit me badlo"

    user_query = st.text_input(
        "Enter conversion query in English or Roman Urdu:",
        value=test_query,
        placeholder="e.g. 'Convert 75 miles to km' or '500 gram kitne kg hote hain'",
        key="nlu_input_box"
    )

    if user_query:
        nlp_result = parse_conversion_query(user_query)
        st.markdown("<br>", unsafe_allow_html=True)
        nlu_res1, nlu_res2 = st.columns([4, 6])

        with nlu_res1:
            st.markdown("#### 🔍 Parsed Query Details")
            st.markdown(f"""
            <div style="background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8 !important;">Language:</span>
                    <strong style="color: #38bdf8 !important;">{nlp_result.detected_language}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8 !important;">Value:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.source_value}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8 !important;">From Unit:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.source_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8 !important;">To Unit:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.target_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8 !important;">Category:</span>
                    <strong style="color: #38bdf8 !important;">{nlp_result.category or 'Auto'}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with nlu_res2:
            st.markdown("#### 🎯 Converted Result")
            if nlp_result.success and nlp_result.conversion_result:
                conv = nlp_result.conversion_result
                st.markdown(f"""
                    <div class="result-card-box">
                        <div class="result-card-label">{conv.source_value:g} {conv.source_unit} =</div>
                        <div class="result-card-value">{conv.target_value:.6g}</div>
                        <div class="result-card-badge">
                            {conv.target_unit} ({conv.target_symbol})
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ {nlp_result.message}")

# =============================================================================
# 6. ALWAYS VISIBLE: Download Buttons & Instant Native Audit Trail
# =============================================================================
st.markdown("---")
h_col1, h_col2 = st.columns([8, 2])
h_col1.markdown("### 📥 Download & Audit Trail")
with h_col2:
    if st.button("🗑️ Clear History", use_container_width=True, key="clear_hist_btn"):
        st.session_state.conversion_history = []
        st.rerun()

history_list = st.session_state.conversion_history if st.session_state.conversion_history else [{
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Category": "Length",
    "From": "1 km",
    "To": "1000 m",
    "Formula": "1 km = 1000 m"
}]

d_col1, d_col2 = st.columns(2)
with d_col1:
    st.download_button(
        label="📥 Download Audit Data (CSV)",
        data=export_history_csv(st.session_state.conversion_history),
        file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
        key="dl_csv_btn"
    )
with d_col2:
    st.download_button(
        label="📥 Download Audit Data (JSON)",
        data=export_history_json(st.session_state.conversion_history),
        file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True,
        key="dl_json_btn"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Instant Native Dark Table (Zero-JS Chunk Delay, 100% Crisp Visible Text)
table_rows = "".join([
    f"""<tr style="border-bottom: 1px solid #1e293b; background: rgba(15, 23, 42, 0.6);">
        <td style="padding: 10px 14px; color: #94a3b8 !important; font-family: monospace; font-size: 0.88rem;">{row.get('Timestamp', '')}</td>
        <td style="padding: 10px 14px; color: #38bdf8 !important; font-weight: 700;">{row.get('Category', '')}</td>
        <td style="padding: 10px 14px; color: #ffffff !important; font-weight: 600;">{row.get('From', '')}</td>
        <td style="padding: 10px 14px; color: #10b981 !important; font-weight: 700;">{row.get('To', '')}</td>
    </tr>"""
    for row in reversed(history_list[-25:])
])

st.markdown(f"""
<div style="overflow-x: auto; border: 1.5px solid #334155; border-radius: 12px; background: #0f172a; box-shadow: 0 4px 20px rgba(0,0,0,0.35);">
    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem;">
        <thead>
            <tr style="border-bottom: 2px solid #0284c7; background: #162032;">
                <th style="padding: 12px 14px; color: #94a3b8 !important; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.05em; text-transform: uppercase;">⏱️ Timestamp</th>
                <th style="padding: 12px 14px; color: #38bdf8 !important; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.05em; text-transform: uppercase;">📂 Category</th>
                <th style="padding: 12px 14px; color: #ffffff !important; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.05em; text-transform: uppercase;">📤 From</th>
                <th style="padding: 12px 14px; color: #10b981 !important; font-weight: 800; font-size: 0.82rem; letter-spacing: 0.05em; text-transform: uppercase;">📥 To</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 7. TWO-SIDED CHATBOT WIDGET (OPENS ON RIGHT CORNER - PERSISTENT UNTIL CUT)
# =============================================================================
if st.session_state.get("chat_open", False):
    with st.container(key="side_chat_card"):
        # Header with Title and Cut (✖) Button
        head_c1, head_c2 = st.columns([8, 2])
        with head_c1:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.25rem;">🤖</span>
                    <div>
                        <strong style="color: #ffffff !important; font-size: 1rem;">Nova AI Copilot</strong>
                        <div style="color: #10b981 !important; font-size: 0.72rem; font-weight: 700;">● Live 24/7 (No Key Needed)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with head_c2:
            if st.button("✖", key="cut_chat_btn", help="Close Nova AI Copilot"):
                st.session_state.chat_open = False
                st.rerun()

        st.markdown("<hr style='margin: 6px 0; border-color: #1e293b;'>", unsafe_allow_html=True)

        # Quick clickable chips
        qc1, qc2 = st.columns(2)
        selected_prompt = None
        if qc1.button("🚗 100 km/h in mph", use_container_width=True, key="float_qp1"):
            selected_prompt = "Convert 100 km/h to mph"
        if qc2.button("🇵🇰 50 miles in km", use_container_width=True, key="float_qp2"):
            selected_prompt = "50 miles ko km me convert karo"

        # Chat message history container (Two-sided bubble layout)
        chat_box = st.container(height=270)
        with chat_box:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    # USER ON THE RIGHT SIDE (Vibrant Royal Blue Bubble)
                    st.markdown(f"""
                    <div class="chat-row-user">
                        <div class="chat-bubble-user">
                            <div style="font-size: 0.75rem; color: #bae6fd !important; font-weight: 700; margin-bottom: 2px;">👤 You</div>
                            <div style="font-size: 0.95rem; line-height: 1.4;">{msg['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # AGENT ON THE LEFT SIDE (Dark Slate + Cyan Border)
                    st.markdown(f"""
                    <div class="chat-row-agent">
                        <div class="chat-bubble-agent">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <span style="font-size: 0.8rem; color: #38bdf8 !important; font-weight: 800;">🤖 Nova AI</span>
                                <small style="font-size: 0.7rem; color: #94a3b8 !important;">{msg.get('provider', '24/7 Engine')}</small>
                            </div>
                            <div style="font-size: 0.95rem; line-height: 1.45;">{msg['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Chat Input Box
        chat_input = st.chat_input("Ask Nova any question...", key="float_chat_input")
        user_message = selected_prompt or chat_input

        if user_message:
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            chatbot = get_ai_copilot()
            with st.spinner("🤖 Nova is thinking..."):
                res = chatbot.process_message(
                    user_message=user_message,
                    chat_history=st.session_state.chat_messages[:-1]
                )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": res["response"],
                "provider": res["provider_used"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.rerun()

        if len(st.session_state.chat_messages) > 1:
            if st.button("🗑️ Clear Chat History", key="float_clear_chat", use_container_width=True):
                st.session_state.chat_messages = [st.session_state.chat_messages[0]]
                st.rerun()

# Floating Aesthetic Corner Button Trigger (Glassmorphism Aurora FAB)
fab_label = "✕ Close Nova AI" if st.session_state.get("chat_open", False) else "✨ Ask Nova AI"
if st.button(fab_label, key="fab_chat_trigger", help="Toggle 24/7 AI Unit Copilot"):
    st.session_state.chat_open = not st.session_state.get("chat_open", False)
    st.rerun()

# -----------------------------------------------------------------------------
# 8. Clean Minimalist Global Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.88rem; padding: 16px 0;">
    <strong style="color: #ffffff;">OmniConvert AI</strong> • High-Precision Unit Intelligence Engine
    <br/>
    Conforms to NIST SP 811 & ISO 80000 Physical Standards • English & Roman Urdu NLU
</div>
""", unsafe_allow_html=True)
