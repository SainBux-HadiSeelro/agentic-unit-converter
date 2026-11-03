"""
OmniConvert AI - Fast, High-Precision Unit Intelligence & 24/7 AI Copilot
Conforms to NIST SP 811, BIPM SI & ISO 80000 physical standards.
"""
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import Optional

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
   5. ALL BUTTONS - INCLUDING DOWNLOAD BUTTONS
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
   6. AESTHETIC FLOATING CHATBOT LAUNCHER (BOTTOM-RIGHT CORNER)
   ========================================================================= */
.st-key-fab_chat_trigger {
    position: fixed !important;
    bottom: 26px !important;
    right: 26px !important;
    z-index: 999999 !important;
}

.st-key-fab_chat_trigger > button {
    background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: 2px solid rgba(255, 255, 255, 0.45) !important;
    border-radius: 9999px !important;
    padding: 14px 26px !important;
    font-size: 1.08rem !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 25px rgba(2, 132, 199, 0.6), 0 0 15px rgba(99, 102, 241, 0.4) !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.st-key-fab_chat_trigger > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 12px 35px rgba(2, 132, 199, 0.85), 0 0 25px rgba(99, 102, 241, 0.6) !important;
    border-color: #ffffff !important;
}

/* Chat bubble styling inside Dialog */
.chat-bubble-user {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

.chat-bubble-agent {
    background: #0f172a;
    border: 1px solid #38bdf8;
    border-radius: 14px 14px 14px 4px;
    padding: 14px 18px;
    margin-bottom: 12px;
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
            "Formula": "1\\text{ km} = 1000\\text{ m}"
        }
    ]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Hello! I am Nova, your 24/7 AI Unit Copilot.**\n\n"
                "I can convert units, explain formulas step-by-step, and answer any physics or math questions.\n\n"
                "You can talk to me in **English** or **Roman Urdu**! Try asking:\n"
                "- *'Convert 120 km/h to mph'*\n"
                "- *'50 miles ko km me convert karo'*\n"
                "- *'Explain temperature conversion formula'*"
            ),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    ]

if "source_value" not in st.session_state:
    st.session_state.source_value = 1.0

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
    use_scientific = st.checkbox("Scientific Notation ($1.0 \\times 10^n$)", value=False)

    # Optional AI Provider Configuration
    with st.expander("🔑 AI Provider Keys (Optional)"):
        provider_choice = st.selectbox(
            "Provider:",
            ["Auto / Built-in 24/7 (Zero Downtime)", "Google Gemini (Live)", "OpenAI (Live)"],
            index=0
        )
        user_api_key = st.text_input(
            "API Key (Optional)",
            type="password",
            help="Leave blank to run 100% offline with zero downtime."
        )

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
            st.latex(conversion.formula_latex)
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
# 6. ALWAYS VISIBLE: Download Buttons & Conversion Audit Trail
# =============================================================================
st.markdown("---")
h_col1, h_col2 = st.columns([8, 2])
h_col1.markdown("### 📥 Download & Audit Trail")
with h_col2:
    if st.button("🗑️ Clear History", use_container_width=True, key="clear_hist_btn"):
        st.session_state.conversion_history = []
        st.rerun()

df_history = pd.DataFrame(st.session_state.conversion_history) if st.session_state.conversion_history else pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Category": "Length", "From": "1 km", "To": "1000 m"}])

d_col1, d_col2 = st.columns(2)
with d_col1:
    csv_data = df_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Data (CSV)",
        data=csv_data,
        file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
        key="dl_csv_btn"
    )
with d_col2:
    json_data = json.dumps(st.session_state.conversion_history, indent=2).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Data (JSON)",
        data=json_data,
        file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True,
        key="dl_json_btn"
    )

st.markdown("<br>", unsafe_allow_html=True)
st.dataframe(df_history[["Timestamp", "Category", "From", "To"]], use_container_width=True)

# -----------------------------------------------------------------------------
# 7. AESTHETIC CORNER FLOATING CHATBOT WIDGET (LIKE MODERN WEBSITES)
# -----------------------------------------------------------------------------
@st.dialog("🤖 Nova AI Copilot • 24/7 Physics & Math Assistant", width="large")
def open_chatbot_dialog():
    chatbot = OmniAgentChatbot(
        provider="gemini" if "Gemini" in provider_choice else ("openai" if "OpenAI" in provider_choice else "auto"),
        api_key=user_api_key if user_api_key else None
    )

    st.markdown("""
        <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid #38bdf8; border-radius: 12px; padding: 12px 16px; margin-bottom: 12px;">
            <span style="color: #38bdf8 !important; font-weight: 700;">🟢 Nova 24/7 Online:</span>
            <span style="color: #cbd5e1 !important; font-size: 0.95rem;">Ask any unit conversion or physics formula in English or Roman Urdu.</span>
        </div>
    """, unsafe_allow_html=True)

    # Quick prompt chips
    qc1, qc2, qc3 = st.columns(3)
    selected_prompt = None
    if qc1.button("🚗 100 km/h in mph", use_container_width=True, key="dlg_qp1"):
        selected_prompt = "Convert 100 km/h to mph"
    if qc2.button("🇵🇰 50 miles in km", use_container_width=True, key="dlg_qp2"):
        selected_prompt = "50 miles ko km me convert karo"
    if qc3.button("🌡️ Temp Formula", use_container_width=True, key="dlg_qp3"):
        selected_prompt = "Explain temperature conversion formula"

    # Chat history box
    chat_box = st.container(height=360)
    with chat_box:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-bubble-user">
                    <strong style="color: #38bdf8 !important;">👤 You:</strong>
                    <div style="color: #ffffff !important; margin-top: 4px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble-agent">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <strong style="color: #38bdf8 !important;">🤖 Nova:</strong>
                        <small style="color: #94a3b8 !important;">{msg.get('provider', '24/7 Engine')}</small>
                    </div>
                    <div style="color: #ffffff !important; line-height: 1.4;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Chat Input Box
    chat_input = st.chat_input("Ask Nova anything...", key="dlg_chat_input")
    user_message = selected_prompt or chat_input

    if user_message:
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

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
        if st.button("🗑️ Clear Chat", key="dlg_clear_chat"):
            st.session_state.chat_messages = [st.session_state.chat_messages[0]]
            st.rerun()

# Floating Aesthetic Corner Button Trigger (Fixed at bottom-right corner)
if st.button("💬 Ask Nova AI", key="fab_chat_trigger", help="Open 24/7 AI Unit Copilot"):
    open_chatbot_dialog()

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
