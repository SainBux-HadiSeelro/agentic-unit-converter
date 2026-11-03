"""
OmniConvert AI - Autonomous Unit Intelligence & 24/7 Live Copilot
Conforms to NIST SP 811, BIPM SI & ISO 80000 standards.
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
# 1. Page Configuration & Modern Theme Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OmniConvert AI | Fast & Intelligent Unit Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
/* Modern Clean Inter & JetBrains Typography */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background Theme */
.stApp {
    background: radial-gradient(circle at 20% 15%, rgba(14, 165, 233, 0.08), transparent 40%),
                radial-gradient(circle at 80% 85%, rgba(99, 102, 241, 0.08), transparent 40%),
                #0b0f19;
    color: #f8fafc;
}

/* Header & Title Styling */
.main-header {
    margin-bottom: 24px;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.live-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px #10b981;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

.header-title {
    margin: 0;
    font-size: 2.3rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.header-gradient-text {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-desc {
    color: #94a3b8;
    margin-top: 6px;
    font-size: 1.05rem;
    line-height: 1.5;
}

/* Glassmorphism Clean Cards */
.converter-card {
    background: rgba(18, 24, 38, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(16px);
    margin-bottom: 20px;
}

/* Ultra Clean Result Display Box */
.result-container {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 20px;
    padding: 26px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.45);
}

.result-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
}

.result-caption {
    font-size: 0.9rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

.result-number {
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin: 10px 0;
    word-break: break-word;
    letter-spacing: -0.02em;
}

.result-badge {
    display: inline-block;
    background: rgba(14, 165, 233, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 1.1rem;
    font-weight: 700;
}

/* Chat Assistant Bubbles */
.chat-user {
    background: linear-gradient(135deg, #1e293b, #334155);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #f8fafc;
}

.chat-assistant {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9));
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 16px 20px;
    margin-bottom: 14px;
    color: #f1f5f9;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

/* Streamlit native widget polish */
div[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    color: #38bdf8 !important;
}

.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.25) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #0b0f19;
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #38bdf8;
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
                "I can convert units, explain formulas step-by-step, and answer any physics or math queries.\n\n"
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
# 3. Sidebar Configuration (Clean & Simple)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span style="font-size: 2.2rem;">⚡</span>
            <div>
                <h3 style="margin: 0; padding: 0; font-size: 1.3rem; font-weight: 800; color: #fff;">OmniConvert AI</h3>
                <span style="font-size: 0.75rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.05em;">SMART CONVERTER</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-pill">
            <span class="live-dot"></span> System Online & Ready
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.radio(
        "Navigation Mode:",
        [
            "⚡ Multi-Category Converter",
            "💬 Smart NLU (English & Urdu)",
            "🤖 24/7 AI Copilot"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Settings & Formatting")
    precision = st.slider("Decimal Places", min_value=1, max_value=8, value=4)
    use_scientific = st.checkbox("Scientific Notation ($1.0 \\times 10^n$)", value=False)

    # Optional Copilot Settings (Clean Collapsible)
    with st.expander("🤖 AI Provider Settings (Optional)"):
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
# 4. Mode 1: Standard & Multi-Category Interactive Converter
# -----------------------------------------------------------------------------
if app_mode == "⚡ Multi-Category Converter":
    st.markdown("""
        <div class="main-header">
            <div class="hero-pill"><span class="live-dot"></span> High-Precision Physics Engine</div>
            <h1 class="header-title">
                Smart <span class="header-gradient-text">Unit Converter</span>
            </h1>
            <p class="header-desc">
                Instant, accurate conversions across 10 physical dimensions with step-by-step mathematical proofs.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Category Selector
    categories = get_categories()
    category_labels = [f"{CATEGORY_ICONS.get(cat, '📐')} {cat}" for cat in categories]
    selected_cat_idx = st.selectbox(
        "Choose Category:",
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

    # Inputs layout
    col1, col_swap, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown(f"**From ({selected_category})**")
        from_idx = st.selectbox(
            "From Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            key=from_key_state,
            label_visibility="collapsed"
        )
        source_key = unit_keys[from_idx]

        # Numeric value input
        source_val = st.number_input(
            "Enter Value:",
            value=float(st.session_state.source_value),
            format="%.4f",
            key=f"val_{selected_category}"
        )
        st.session_state.source_value = source_val

        # Quick preset helper buttons
        p1, p2, p3, p4 = st.columns(4)
        if p1.button("+1", use_container_width=True, help="Add 1"):
            st.session_state.source_value = source_val + 1.0
            st.rerun()
        if p2.button("+10", use_container_width=True, help="Add 10"):
            st.session_state.source_value = source_val + 10.0
            st.rerun()
        if p3.button("100", use_container_width=True, help="Set to 100"):
            st.session_state.source_value = 100.0
            st.rerun()
        if p4.button("Reset", use_container_width=True, help="Reset to 1"):
            st.session_state.source_value = 1.0
            st.rerun()

    with col_swap:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⇄", help="Swap From & To Units", use_container_width=True):
            curr_from = st.session_state[from_key_state]
            curr_to = st.session_state[to_key_state]
            st.session_state[from_key_state] = curr_to
            st.session_state[to_key_state] = curr_from
            st.rerun()

    with col2:
        st.markdown(f"**To ({selected_category})**")
        to_idx = st.selectbox(
            "To Unit",
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
                <div class="result-container">
                    <div class="result-caption">Converted Result</div>
                    <div class="result-number">{formatted_val}</div>
                    <div class="result-badge">
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

    # Step-by-Step Derivation
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
                label="📥 Download History (CSV)",
                data=csv_data,
                file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with d_col2:
            json_data = json.dumps(st.session_state.conversion_history, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Download History (JSON)",
                data=json_data,
                file_name=f"conversion_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# 5. Mode 2: Natural Language Converter (English & Roman Urdu)
# -----------------------------------------------------------------------------
elif app_mode == "💬 Smart NLU (English & Urdu)":
    st.markdown("""
        <div class="main-header">
            <div class="hero-pill"><span class="live-dot"></span> Bilingual Language Understanding</div>
            <h1 class="header-title">
                Smart <span class="header-gradient-text">Language Converter</span>
            </h1>
            <p class="header-desc">
                Type naturally in plain <b>English</b> or <b>Roman Urdu</b>. The system understands your query and computes the result instantly.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Quick example chips
    st.markdown("**Quick Examples (Click to try):**")
    q_col1, q_col2, q_col3 = st.columns(3)
    test_query = ""
    if q_col1.button("🚗 120 km/h to mph", use_container_width=True):
        test_query = "convert 120 km/h to mph"
    if q_col2.button("🇵🇰 50 miles ko km me badlo", use_container_width=True):
        test_query = "50 miles ko km me badlo"
    if q_col3.button("🌡️ 100 celsius ko fahrenheit me badlo", use_container_width=True):
        test_query = "100 celsius ko fahrenheit me badlo"

    user_query = st.text_input(
        "Enter your query in English or Roman Urdu:",
        value=test_query,
        placeholder="e.g. 'Convert 75 miles to km' or '500 gram kitne kg hote hain'"
    )

    if user_query:
        nlp_result = parse_conversion_query(user_query)

        st.markdown("<br>", unsafe_allow_html=True)
        col_res1, col_res2 = st.columns([4, 6])

        with col_res1:
            st.markdown("#### 🔍 Parsed Parameters")
            st.markdown(f"""
            <div class="converter-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">Language:</span>
                    <strong style="color: #38bdf8;">{nlp_result.detected_language}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">Value:</span>
                    <strong style="color: #ffffff;">{nlp_result.source_value}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">From:</span>
                    <strong style="color: #ffffff;">{nlp_result.source_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">To:</span>
                    <strong style="color: #ffffff;">{nlp_result.target_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">Category:</span>
                    <strong style="color: #38bdf8;">{nlp_result.category or 'Auto'}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("#### 🎯 Result")
            if nlp_result.success and nlp_result.conversion_result:
                conv = nlp_result.conversion_result
                st.markdown(f"""
                    <div class="result-container">
                        <div class="result-caption">{conv.source_value:g} {conv.source_unit} =</div>
                        <div class="result-number">{conv.target_value:.6g}</div>
                        <div class="result-badge">
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
# 6. Mode 3: 24/7 AI Customer Support Copilot
# -----------------------------------------------------------------------------
elif app_mode == "🤖 24/7 AI Copilot":
    st.markdown("""
        <div class="main-header">
            <div class="hero-pill"><span class="live-dot"></span> 24/7 AI Assistant</div>
            <h1 class="header-title">
                Nova <span class="header-gradient-text">AI Copilot</span>
            </h1>
            <p class="header-desc">
                Your smart physics and unit conversion companion. Ask questions, request conversions, or understand formulas in English or Roman Urdu.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Chatbot Engine
    chatbot = OmniAgentChatbot(
        provider="gemini" if "Gemini" in provider_choice else ("openai" if "OpenAI" in provider_choice else "auto"),
        api_key=user_api_key if user_api_key else None
    )

    # Suggested inquiries chips
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
                <div class="chat-user">
                    <strong style="color: #38bdf8;">👤 You</strong> <span style="font-size: 0.75rem; color: #94a3b8; float: right;">{msg.get('timestamp', '')}</span>
                    <div style="margin-top: 6px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-assistant">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #38bdf8; font-weight: 700;">🤖 Nova Copilot</span>
                        <span style="font-size: 0.75rem; background: rgba(14, 165, 233, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 10px;">
                            {msg.get('provider', '24/7 Engine')} • {msg.get('timestamp', '')}
                        </span>
                    </div>
                    <div>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Chat Input
    chat_input_val = st.chat_input("Ask Nova any question or conversion command...")
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
# 7. Clean Global Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 16px 0;">
    <strong>OmniConvert AI</strong> • High-Precision Unit Intelligence Engine
    <br/>
    Conforms to NIST SP 811 & ISO 80000 Physical Standards • English & Roman Urdu NLU
</div>
""", unsafe_allow_html=True)
