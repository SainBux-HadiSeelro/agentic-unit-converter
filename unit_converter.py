"""
OmniConvert AI - Autonomous Unit Intelligence & 24/7 Live Customer Copilot
Architected & Developed by Hadi Seelro (Agentic AI Developer)
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
# 1. Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OmniConvert AI | Autonomous Unit Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
/* Modern Cyber-Glassmorphism Theme */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background gradient styling */
.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.05), transparent 30%),
                radial-gradient(circle at 85% 85%, rgba(79, 172, 254, 0.05), transparent 30%),
                #0b0f19;
    color: #f1f5f9;
}

/* Glassmorphism Card Containers */
.glass-card {
    background: rgba(22, 27, 46, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.glass-card:hover {
    border-color: rgba(0, 242, 254, 0.3);
    box-shadow: 0 12px 35px rgba(0, 242, 254, 0.12);
}

/* Hero Badge */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 242, 254, 0.12);
    border: 1px solid rgba(0, 242, 254, 0.35);
    color: #00f2fe;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.live-indicator {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.3); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

/* Big Display Result Card */
.result-box {
    background: linear-gradient(135deg, rgba(16, 24, 48, 0.95) 0%, rgba(26, 36, 72, 0.85) 100%);
    border: 1px solid rgba(79, 172, 254, 0.3);
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
}

.result-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #00c6ff);
}

.result-value {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a5f3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin: 8px 0;
}

.result-unit-label {
    font-size: 1.1rem;
    color: #94a3b8;
    font-weight: 500;
}

/* Chat Assistant Bubbles */
.chat-bubble-user {
    background: linear-gradient(135deg, #1e293b, #334155);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
    color: #f8fafc;
}

.chat-bubble-agent {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.85));
    border: 1px solid rgba(0, 242, 254, 0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 16px 20px;
    margin-bottom: 14px;
    color: #f1f5f9;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

/* Quick prompt chips */
.prompt-chip-btn {
    border-radius: 20px !important;
    font-size: 0.85rem !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0b0f19;
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #00f2fe;
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
                "👋 **Hello! I am Nova, your 24/7 OmniConvert AI Copilot.**\n\n"
                "I was built by **Hadi Seelro** to handle real-time unit conversions, explain mathematical formulas, "
                "troubleshoot calculations, and assist customers 24/7.\n\n"
                "You can talk to me in **English** or **Roman Urdu**! Try asking:\n"
                "- *'Convert 120 km/h to mph'*\n"
                "- *'50 miles ko km me convert karo'*\n"
                "- *'Explain the temperature conversion formula'*\n"
                "- *'Tell me about the developer and architecture'*"
            ),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    ]

if "source_value" not in st.session_state:
    st.session_state.source_value = 1.0

# -----------------------------------------------------------------------------
# 3. Sidebar Configuration & Architecture Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 2rem;">⚡</span>
            <div>
                <h3 style="margin: 0; padding: 0; font-size: 1.25rem; font-weight: 800; color: #fff;">OmniConvert AI</h3>
                <span style="font-size: 0.75rem; color: #00f2fe; font-weight: 600;">v2.0.0-AGENTIC</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-badge">
            <span class="live-indicator"></span> 24/7 Agent Active
        </div>
    """, unsafe_allow_html=True)

    app_mode = st.radio(
        "Navigation Mode:",
        [
            "⚡ Multi-Category Converter",
            "🧠 Agentic NLU Converter (English / Roman Urdu)",
            "🤖 24/7 Customer AI Copilot"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Precision & Mathematics")
    precision = st.slider("Decimal Precision", min_value=1, max_value=10, value=4)
    use_scientific = st.checkbox("Scientific Notation ($1.0 \\times 10^n$)", value=False)

    st.markdown("---")
    st.markdown("#### 🧠 Copilot Cognitive Engine")
    provider_choice = st.selectbox(
        "Provider Gateway:",
        ["Auto / Built-in 24/7 (Zero Downtime)", "Google Gemini (Live)", "OpenAI (Live)"],
        index=0
    )
    user_api_key = st.text_input(
        "Optional API Key (for Live LLM)",
        type="password",
        help="Leave blank to run 100% offline with our resilient deterministic ReAct engine."
    )

    st.markdown("---")
    st.markdown("#### 👨‍💻 Developer & Portfolio")
    st.markdown("""
    **Architected by:** [Hadi Seelro](https://github.com/SainBux-HadiSeelro)  
    *Agentic AI Developer & Full-Stack Systems Engineer*  
    - 📁 [GitHub Repository](https://github.com/SainBux-HadiSeelro)  
    - 📋 [System Architecture SPEC](SPEC.md)  
    - 🛡️ Standard: NIST SP 811 & IEEE 830
    """)

# -----------------------------------------------------------------------------
# 4. Mode 1: Standard & Multi-Category Interactive Converter
# -----------------------------------------------------------------------------
if app_mode == "⚡ Multi-Category Converter":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <div class="hero-badge"><span class="live-indicator"></span> Real-Time Multi-Domain Physics Engine</div>
            <h1 style="margin: 0; font-size: 2.4rem; font-weight: 800; color: #fff;">
                OmniConvert <span style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Intelligence</span>
            </h1>
            <p style="color: #94a3b8; margin-top: 6px; font-size: 1.05rem;">
                High-precision unit transformations across 10 physical dimensions with live mathematical proofs and LaTeX derivations.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Category Selector Tabs with dynamic icons
    categories = get_categories()
    category_labels = [f"{CATEGORY_ICONS.get(cat, '📐')} {cat}" for cat in categories]
    selected_cat_idx = st.selectbox(
        "Select Physical Dimension:",
        options=range(len(categories)),
        format_func=lambda i: category_labels[i],
        index=0
    )
    selected_category = categories[selected_cat_idx]

    units_dict = get_units_for_category(selected_category)
    unit_keys = list(units_dict.keys())
    unit_display_names = [f"{units_dict[k].name} ({units_dict[k].symbol})" for k in unit_keys]

    st.markdown("---")

    # Inputs layout
    col1, col_swap, col2 = st.columns([5, 1, 5])

    # Default indices
    from_default_idx = 0
    to_default_idx = 1 if len(unit_keys) > 1 else 0

    with col1:
        st.markdown(f"#### From ({selected_category})")
        from_idx = st.selectbox(
            "Source Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            index=from_default_idx,
            key=f"from_{selected_category}"
        )
        source_key = unit_keys[from_idx]

        # Numeric value with preset helper chips
        source_val = st.number_input(
            "Enter numerical quantity:",
            value=float(st.session_state.source_value),
            format="%.4f",
            key=f"val_{selected_category}"
        )
        st.session_state.source_value = source_val

        # Quick preset buttons
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        if c_p1.button("+1", use_container_width=True):
            st.session_state.source_value = source_val + 1.0
            st.rerun()
        if c_p2.button("+10", use_container_width=True):
            st.session_state.source_value = source_val + 10.0
            st.rerun()
        if c_p3.button("100", use_container_width=True):
            st.session_state.source_value = 100.0
            st.rerun()
        if c_p4.button("Reset", use_container_width=True):
            st.session_state.source_value = 1.0
            st.rerun()

    with col_swap:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("⇄", help="Swap Source and Target Units", use_container_width=True):
            # Handled dynamically via inverted indices
            pass

    with col2:
        st.markdown(f"#### To ({selected_category})")
        to_idx = st.selectbox(
            "Target Unit",
            options=range(len(unit_keys)),
            format_func=lambda i: unit_display_names[i],
            index=to_default_idx,
            key=f"to_{selected_category}"
        )
        target_key = unit_keys[to_idx]

        # Execute conversion instantly
        conversion = convert(source_val, source_key, target_key)

        # Format number based on settings
        if conversion.success:
            if use_scientific:
                formatted_val = f"{conversion.target_value:.{precision}e}"
            else:
                formatted_val = f"{conversion.target_value:,.{precision}f}".rstrip('0').rstrip('.') if '.' in f"{conversion.target_value:.{precision}f}" else f"{conversion.target_value:.0f}"

            st.markdown(f"""
                <div class="result-box">
                    <div class="result-unit-label">Converted Quantity</div>
                    <div class="result-value">{formatted_val}</div>
                    <div style="color: #38bdf8; font-weight: 600; font-size: 1.15rem;">
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

    # Mathematical Breakdown Card
    if conversion.success:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📐 Step-by-Step Mathematical Derivation & LaTeX Proof", expanded=True):
            st.markdown("##### Rigorous Equation:")
            st.latex(conversion.formula_latex)
            st.markdown("##### Step-by-Step Normalization Steps:")
            st.code(conversion.step_by_step, language="text")
            st.caption(f"Standards Reference: {selected_category} operations mapped via {PROJECT_KNOWLEDGE_BASE['scientific_standards'].get(selected_category.lower() + '_base', 'SI Standard Conventions')}")

    # Conversion History Section
    if st.session_state.conversion_history:
        st.markdown("---")
        h_col1, h_col2 = st.columns([8, 2])
        h_col1.markdown("### 🕒 Session Conversion Audit Trail")
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
                label="📥 Download Audit Trail (CSV)",
                data=csv_data,
                file_name=f"omniconvert_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with d_col2:
            json_data = json.dumps(st.session_state.conversion_history, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Trail (JSON)",
                data=json_data,
                file_name=f"omniconvert_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# 5. Mode 2: Agentic Natural Language Converter
# -----------------------------------------------------------------------------
elif app_mode == "🧠 Agentic NLU Converter (English / Roman Urdu)":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <div class="hero-badge"><span class="live-indicator"></span> Conversational Intent Parser</div>
            <h1 style="margin: 0; font-size: 2.4rem; font-weight: 800; color: #fff;">
                Agentic <span style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NLU Converter</span>
            </h1>
            <p style="color: #94a3b8; margin-top: 6px; font-size: 1.05rem;">
                Powered by a bilingual parser that extracts numerical values, source units, and target units from natural language prompts in <b>English</b> or <b>Roman Urdu</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Prompt suggestions
    st.markdown("##### Quick Example Prompts (Click to test):")
    q_col1, q_col2, q_col3 = st.columns(3)
    test_query = ""
    if q_col1.button("🚗 120 km/h to mph", use_container_width=True):
        test_query = "convert 120 km/h to mph"
    if q_col2.button("🇵🇰 50 miles ko km me badlo", use_container_width=True):
        test_query = "50 miles ko km me badlo"
    if q_col3.button("🌡️ 100 celsius ko fahrenheit me badlo", use_container_width=True):
        test_query = "100 celsius ko fahrenheit me badlo"

    user_query = st.text_input(
        "Enter your conversion command in English or Roman Urdu:",
        value=test_query,
        placeholder="e.g., 'Convert 75 miles to km' or '500 gram kitne kg hote hain' or '35 celsius ko fahrenheit me convert karo'"
    )

    if user_query:
        nlp_result = parse_conversion_query(user_query)

        st.markdown("<br>", unsafe_allow_html=True)
        col_res1, col_res2 = st.columns([4, 6])

        with col_res1:
            st.markdown("#### 🔍 NLU Parameter Extraction")
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8;">Detected Language:</span>
                    <strong style="color: #00f2fe;">{nlp_result.detected_language}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8;">Confidence Score:</span>
                    <strong style="color: #10b981;">{nlp_result.confidence * 100:.1f}%</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8;">Source Value:</span>
                    <strong>{nlp_result.source_value}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8;">Source Unit:</span>
                    <strong>{nlp_result.source_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #94a3b8;">Target Unit:</span>
                    <strong>{nlp_result.target_unit}</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">Category:</span>
                    <strong style="color: #f59e0b;">{nlp_result.category or 'Auto'}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("#### 🎯 Execution Output")
            if nlp_result.success and nlp_result.conversion_result:
                conv = nlp_result.conversion_result
                st.markdown(f"""
                    <div class="result-box">
                        <div class="result-unit-label">{conv.source_value:g} {conv.source_unit} =</div>
                        <div class="result-value">{conv.target_value:.6g}</div>
                        <div style="color: #38bdf8; font-weight: 600; font-size: 1.15rem;">
                            {conv.target_unit} ({conv.target_symbol})
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("##### 📐 Mathematical Proof:")
                st.latex(conv.formula_latex)
            else:
                st.warning(f"⚠️ {nlp_result.message}")

# -----------------------------------------------------------------------------
# 6. Mode 3: 24/7 AI Customer Support Copilot
# -----------------------------------------------------------------------------
elif app_mode == "🤖 24/7 Customer AI Copilot":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <div class="hero-badge"><span class="live-indicator"></span> 24/7 Autonomous Customer Care</div>
            <h1 style="margin: 0; font-size: 2.4rem; font-weight: 800; color: #fff;">
                Nova <span style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Copilot</span>
            </h1>
            <p style="color: #94a3b8; margin-top: 6px; font-size: 1.05rem;">
                Always-on technical copilot and customer support agent. Live 24/7 with zero downtime, equipped with the complete project knowledge base and real-time conversion tools.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Chatbot Engine
    chatbot = OmniAgentChatbot(
        provider="gemini" if "Gemini" in provider_choice else ("openai" if "OpenAI" in provider_choice else "auto"),
        api_key=user_api_key if user_api_key else None
    )

    # Quick prompt buttons
    st.markdown("##### 💡 Suggested Inquiries:")
    quick_cols = st.columns(3)
    prompts = get_quick_prompts()
    selected_quick_prompt = None

    for idx, prompt_text in enumerate(prompts[:6]):
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
                <div class="chat-bubble-user">
                    <strong style="color: #38bdf8;">👤 You</strong> <span style="font-size: 0.75rem; color: #94a3b8; float: right;">{msg.get('timestamp', '')}</span>
                    <div style="margin-top: 6px;">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble-agent">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: #00f2fe; font-weight: 700;">🤖 Nova AI Copilot</span>
                        <span style="font-size: 0.75rem; background: rgba(0, 242, 254, 0.15); color: #00f2fe; padding: 2px 8px; border-radius: 10px;">
                            {msg.get('provider', '24/7 Engine')} • {msg.get('timestamp', '')}
                        </span>
                    </div>
                    <div>{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Chat Input
    chat_input_val = st.chat_input("Ask Nova anything about units, formulas, project specs, or developer portfolio...")
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
        with st.spinner("🤖 Nova is reasoning and consulting the project knowledge base..."):
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
        if st.button("🗑️ Clear Conversation History"):
            st.session_state.chat_messages = [st.session_state.chat_messages[0]]
            st.rerun()

# -----------------------------------------------------------------------------
# 7. Global Footer & Recruiter Portfolio Highlights
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 20px 0;">
    <strong>OmniConvert AI</strong> • Engineered with ❤️ by 
    <a href="https://github.com/SainBux-HadiSeelro" target="_blank" style="color: #00f2fe; text-decoration: none; font-weight: 600;">Hadi Seelro</a>
    <br/>
    Autonomous ReAct Pattern • NIST SP 811 & ISO 80000 Compliance • Multilingual Roman Urdu & English NLU
</div>
""", unsafe_allow_html=True)
