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
# 1. Page Configuration & Guaranteed-Visible High-Contrast Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OmniConvert AI | Smart Unit Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
/* Instant System Fonts - 100% Legibility without Flash of Invisible Text */
html, body, [class*="css"], .stApp {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    background-color: #0b0f19 !important;
    color: #ffffff !important;
}

/* =========================================================================
   UNIVERSAL TEXT VISIBILITY (FORCE VISIBLE AT ALL TIMES - NEVER ON HOVER ONLY)
   ========================================================================= */

/* All headings, paragraphs, and labels forced to bright visible colors */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 800 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

p, span, label, strong, b, em, small {
    color: #f1f5f9 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Streamlit markdown container text */
[data-testid="stMarkdownContainer"] * {
    color: #f1f5f9 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Explicit input labels */
.stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label {
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    visibility: visible !important;
    margin-bottom: 6px !important;
}

/* =========================================================================
   BASEWEB SELECTBOX & DROPDOWN - FIXED INVISIBLE TEXT
   ========================================================================= */

/* Selectbox control container */
div[data-baseweb="select"] > div {
    background-color: #162032 !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

/* Selected value text inside the selectbox */
div[data-baseweb="select"] * {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Dropdown popover menu and options */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background-color: #162032 !important;
    color: #ffffff !important;
}

li[role="option"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

li[role="option"]:hover {
    background-color: #0284c7 !important;
}

/* =========================================================================
   INPUT FIELDS (QUANTITY & TEXT) - FIXED INVISIBLE TEXT
   ========================================================================= */

div[data-baseweb="input"] {
    background-color: #162032 !important;
    border: 1px solid #3b82f6 !important;
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

/* Radio buttons and checkboxes */
div[data-testid="stRadio"] label,
div[data-testid="stRadio"] span,
div[data-testid="stCheckbox"] label,
div[data-testid="stCheckbox"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
}

/* =========================================================================
   BUTTONS
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

.stButton > button * {
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover {
    background-color: #0284c7 !important;
    border-color: #38bdf8 !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
}

/* =========================================================================
   CUSTOM CARD & RESULT CONTAINERS
   ========================================================================= */

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(14, 165, 233, 0.2);
    border: 1px solid #38bdf8;
    color: #38bdf8 !important;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.live-indicator-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px #10b981;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff !important;
    margin: 0;
    line-height: 1.2;
}

.gradient-title-accent {
    color: #38bdf8 !important;
}

.subtitle-desc {
    color: #cbd5e1 !important;
    font-size: 1.05rem;
    margin-top: 6px;
    margin-bottom: 24px;
}

/* Converted Result Display Box */
.result-card-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 2px solid #38bdf8;
    border-radius: 18px;
    padding: 26px 20px;
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
    font-size: 3.4rem;
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

/* Info Overview Card */
.info-card {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}

/* Chat Styling */
.user-bubble {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 14px 14px 4px 14px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.assistant-bubble {
    background: #0f172a;
    border: 1px solid #38bdf8;
    border-radius: 14px 14px 14px 4px;
    padding: 16px 20px;
    margin-bottom: 14px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = []

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
                "- *'Explain temperature conversion formula'*\n"
                "- *'100 celsius ko fahrenheit me badlo'*"
            ),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    ]

if "source_value" not in st.session_state:
    st.session_state.source_value = 1.0

# -----------------------------------------------------------------------------
# 3. Sidebar Controls (Visible & High Contrast)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">
            <span style="font-size: 2.2rem;">⚡</span>
            <div>
                <h3 style="margin: 0; padding: 0; font-size: 1.3rem; font-weight: 800; color: #ffffff;">OmniConvert AI</h3>
                <span style="font-size: 0.75rem; color: #38bdf8; font-weight: 800; letter-spacing: 0.05em;">SMART CONVERTER</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-badge">
            <span class="live-indicator-dot"></span> System Ready
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.radio(
        "Navigation:",
        [
            "⚡ Quick Unit Converter",
            "💬 Smart Language (English & Urdu)",
            "🤖 24/7 AI Copilot"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Display Settings")
    
    # Safe Selectbox for Precision
    precision = st.selectbox(
        "Decimal Places:",
        options=[2, 3, 4, 6, 8],
        index=2,
        help="Number of decimal places shown in the converted result."
    )
    use_scientific = st.checkbox("Scientific Notation ($1.0 \\times 10^n$)", value=False)

    # Optional AI Provider Configuration
    with st.expander("🤖 AI Copilot Settings (Optional)"):
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
# 4. Mode 1: Quick Multi-Category Unit Converter
# -----------------------------------------------------------------------------
if app_mode == "⚡ Quick Unit Converter":
    st.markdown("""
        <div>
            <div class="hero-badge"><span class="live-indicator-dot"></span> NIST SP 811 & ISO 80000 Compliant</div>
            <h1 class="main-title">
                Smart <span class="gradient-title-accent">Unit Converter</span>
            </h1>
            <p class="subtitle-desc">
                High-precision, instantaneous conversions across 10 physical dimensions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Category Selector
    categories = get_categories()
    category_labels = [f"{CATEGORY_ICONS.get(cat, '📐')} {cat}" for cat in categories]
    selected_cat_idx = st.selectbox(
        "Select Category:",
        options=range(len(categories)),
        format_func=lambda i: category_labels[i],
        index=0
    )
    selected_category = categories[selected_cat_idx]

    units_dict = get_units_for_category(selected_category)
    unit_keys = list(units_dict.keys())
    unit_display_names = [f"{units_dict[k].name} ({units_dict[k].symbol})" for k in unit_keys]

    st.markdown("<br>", unsafe_allow_html=True)

    # State keys for swap feature
    from_key_state = f"from_{selected_category}"
    to_key_state = f"to_{selected_category}"

    if from_key_state not in st.session_state:
        st.session_state[from_key_state] = 0
    if to_key_state not in st.session_state:
        st.session_state[to_key_state] = 1 if len(unit_keys) > 1 else 0

    # Clean 2-Column Layout with Center Swap
    col1, col_swap, col2 = st.columns([5, 1.2, 5])

    with col1:
        st.markdown(f"**From ({selected_category}):**")
        from_idx = st.selectbox(
            "Source Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            key=from_key_state,
            label_visibility="collapsed"
        )
        source_key = unit_keys[from_idx]

        # Numeric Input
        source_val = st.number_input(
            "Enter Quantity:",
            value=float(st.session_state.source_value),
            format="%.4f",
            key=f"val_{selected_category}"
        )
        st.session_state.source_value = source_val

        # Quick Helper Buttons
        p1, p2, p3, p4 = st.columns(4)
        if p1.button("+1", use_container_width=True):
            st.session_state.source_value = source_val + 1.0
            st.rerun()
        if p2.button("+10", use_container_width=True):
            st.session_state.source_value = source_val + 10.0
            st.rerun()
        if p3.button("100", use_container_width=True):
            st.session_state.source_value = 100.0
            st.rerun()
        if p4.button("Reset", use_container_width=True):
            st.session_state.source_value = 1.0
            st.rerun()

    with col_swap:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⇄ Swap", help="Swap Source and Target Units", use_container_width=True):
            curr_from = st.session_state[from_key_state]
            curr_to = st.session_state[to_key_state]
            st.session_state[from_key_state] = curr_to
            st.session_state[to_key_state] = curr_from
            st.rerun()

    with col2:
        st.markdown(f"**To ({selected_category}):**")
        to_idx = st.selectbox(
            "Target Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            key=to_key_state,
            label_visibility="collapsed"
        )
        target_key = unit_keys[to_idx]

        # Execute conversion instantly
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

            # Record in conversion history
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

    # Step-by-Step Derivation Expander
    if conversion.success:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📐 View Step-by-Step Formula & Explanation", expanded=False):
            st.markdown("**Mathematical Formula:**")
            st.latex(conversion.formula_latex)
            st.markdown("**Calculation Steps:**")
            st.code(conversion.step_by_step, language="text")

    # Conversion History Section
    if st.session_state.conversion_history:
        st.markdown("---")
        h_col1, h_col2 = st.columns([8, 2])
        h_col1.markdown("### 🕒 Recent Conversions")
        with h_col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.conversion_history = []
                st.rerun()

        df_history = pd.DataFrame(st.session_state.conversion_history)
        st.dataframe(df_history[["Timestamp", "Category", "From", "To"]], use_container_width=True)

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            csv_data = df_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with d_col2:
            json_data = json.dumps(st.session_state.conversion_history, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# 5. Mode 2: Natural Language Converter (English & Roman Urdu)
# -----------------------------------------------------------------------------
elif app_mode == "💬 Smart Language (English & Urdu)":
    st.markdown("""
        <div>
            <div class="hero-badge"><span class="live-indicator-dot"></span> Bilingual NLU Engine</div>
            <h1 class="main-title">
                Smart <span class="gradient-title-accent">Language Converter</span>
            </h1>
            <p class="subtitle-desc">
                Type naturally in <b>English</b> or <b>Roman Urdu</b>. The system understands your query and computes the result automatically.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Clickable Example Chips
    st.markdown("**Click an example to test:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    test_query = ""
    if q_col1.button("🚗 120 km/h to mph", use_container_width=True):
        test_query = "convert 120 km/h to mph"
    if q_col2.button("🇵🇰 50 miles ko km me badlo", use_container_width=True):
        test_query = "50 miles ko km me badlo"
    if q_col3.button("🌡️ 100 celsius ko fahrenheit me badlo", use_container_width=True):
        test_query = "100 celsius ko fahrenheit me badlo"

    user_query = st.text_input(
        "Enter your conversion command:",
        value=test_query,
        placeholder="e.g. 'Convert 75 miles to km' or '500 gram kitne kg hote hain'"
    )

    if user_query:
        nlp_result = parse_conversion_query(user_query)

        st.markdown("<br>", unsafe_allow_html=True)
        col_res1, col_res2 = st.columns([4, 6])

        with col_res1:
            st.markdown("#### 🔍 Parsed Query Details")
            st.markdown(f"""
            <div class="info-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8 !important;">Language:</span>
                    <strong style="color: #38bdf8 !important;">{nlp_result.detected_language}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8 !important;">Value:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.source_value}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8 !important;">From Unit:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.source_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8 !important;">To Unit:</span>
                    <strong style="color: #ffffff !important;">{nlp_result.target_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8 !important;">Category:</span>
                    <strong style="color: #38bdf8 !important;">{nlp_result.category or 'Auto'}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
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

                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("📐 View Formula Proof", expanded=False):
                    st.latex(conv.formula_latex)
            else:
                st.warning(f"⚠️ {nlp_result.message}")

# -----------------------------------------------------------------------------
# 6. Mode 3: 24/7 AI Customer Copilot
# -----------------------------------------------------------------------------
elif app_mode == "🤖 24/7 AI Copilot":
    st.markdown("""
        <div>
            <div class="hero-badge"><span class="live-indicator-dot"></span> 24/7 Intelligent Assistant</div>
            <h1 class="main-title">
                Nova <span class="gradient-title-accent">AI Copilot</span>
            </h1>
            <p class="subtitle-desc">
                Ask questions, request conversions, or explore formulas in English or Roman Urdu.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Chatbot Engine
    chatbot = OmniAgentChatbot(
        provider="gemini" if "Gemini" in provider_choice else ("openai" if "OpenAI" in provider_choice else "auto"),
        api_key=user_api_key if user_api_key else None
    )

    # Suggested Prompts
    st.markdown("**Suggested Questions:**")
    quick_cols = st.columns(3)
    prompts = [
        "Convert 100 km/h to mph",
        "50 miles ko km me convert karo",
        "Explain temperature conversion formula",
        "How many meters are in a mile?",
        "100 celsius ko fahrenheit me badlo",
        "Convert 5 GB to megabytes"
    ]
    selected_quick_prompt = None

    for idx, prompt_text in enumerate(prompts):
        col = quick_cols[idx % 3]
        if col.button(f"💬 {prompt_text}", key=f"quick_{idx}", use_container_width=True):
            selected_quick_prompt = prompt_text

    st.markdown("---")

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-bubble">
                    <strong style="color: #38bdf8 !important;">👤 You</strong> <span style="font-size: 0.75rem; color: #94a3b8 !important; float: right;">{msg.get('timestamp', '')}</span>
                    <div style="margin-top: 6px; font-size: 1rem; color: #ffffff !important;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-bubble">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #38bdf8 !important; font-weight: 700;">🤖 Nova Copilot</span>
                        <span style="font-size: 0.75rem; background: rgba(14, 165, 233, 0.2); color: #38bdf8 !important; padding: 2px 8px; border-radius: 10px;">
                            {msg.get('provider', '24/7 Engine')} • {msg.get('timestamp', '')}
                        </span>
                    </div>
                    <div style="font-size: 1rem; line-height: 1.5; color: #ffffff !important;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Chat Input
    chat_input_val = st.chat_input("Type your question or conversion command here...")
    user_to_send = selected_quick_prompt or chat_input_val

    if user_to_send:
        # Append User Message
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_to_send,
            "timestamp": timestamp
        })

        # Process with OmniAgentChatbot
        with st.spinner("🤖 Nova is thinking..."):
            res = chatbot.process_message(
                user_message=user_to_send,
                chat_history=st.session_state.chat_messages[:-1]
            )

        # Append Assistant Message
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": res["response"],
            "provider": res["provider_used"],
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.rerun()

    # Clear chat option
    if len(st.session_state.chat_messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = [st.session_state.chat_messages[0]]
            st.rerun()

# -----------------------------------------------------------------------------
# 7. Clean Minimalist Global Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.88rem; padding: 16px 0;">
    <strong style="color: #ffffff;">OmniConvert AI</strong> • High-Precision Unit Intelligence Engine
    <br/>
    Conforms to NIST SP 811 & ISO 80000 Physical Standards • English & Roman Urdu NLU
</div>
""", unsafe_allow_html=True)
