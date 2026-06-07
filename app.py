import streamlit as st
import os
from utils.api_utils import calculate_risk, load_models

# Page config
st.set_page_config(
    page_title="Workplace Mental Health Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling - Global theme locks to enforce light styles in dark mode
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global page layout and background */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #dbeafe !important;
        background-image: linear-gradient(to bottom, #edf6ff 0%, #dbeafe 50%, #bfdbfe 100%) !important;
        background-attachment: fixed !important;
    }

    /* Force transparency on top header bar and page background layers */
    [data-testid="stHeader"], [data-testid="stMainViewContainer"] {
        background: transparent !important;
    }

    /* Hide the Streamlit sidebar navigation toggle control */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        max-width: 1050px !important; /* Widen layout from 800px for a better website feel */
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Lock typography to dark navy color across all Streamlit markdown blocks */
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] label {
        color: #1e293b !important;
    }

    /* Compact Dark Blue Gradient Header Card */
    .header-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 20px 30px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1) !important;
        text-align: center !important;
    }
    /* High specificity overrides to force header card elements to remain white/light-blue */
    [data-testid="stAppViewContainer"] .header-card h1,
    [data-testid="stAppViewContainer"] .header-card h1 *,
    [data-testid="stAppViewContainer"] .header-card span,
    .header-card h1,
    .header-card h1 *,
    .header-card span {
        color: #ffffff !important;
        font-size: 42px !important; /* Increased font size for title impact */
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stAppViewContainer"] .header-card p,
    [data-testid="stAppViewContainer"] .header-card p *,
    .header-card p,
    .header-card p * {
        color: #cbd5e1 !important;
        font-size: 14.5px !important; /* Restored subtitle size */
    }

    /* Form Container Card */
    .portfolio-card * {
        color: #1e293b !important;
    }

    /* Force widget labels color to dark slate */
    label, 
    div[data-testid="stWidgetLabel"] p, 
    label[data-testid="stWidgetLabel"] {
        color: #1e293b !important;
        font-weight: 500 !important;
    }

    /* Force selectbox styles */
    div[data-testid="stSelectbox"] {
        background-color: #f8fafc !important;
        border-radius: 8px !important;
    }
    div[data-testid="stSelectbox"] > div {
        background-color: transparent !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stSelectbox"] div[role="button"] {
        background-color: transparent !important;
        color: #1e293b !important;
    }
    div[data-testid="stSelectbox"] svg {
        fill: #1e293b !important;
    }

    /* Dropdown popover menu styling (React portals outside block container) */
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"], 
    div[data-baseweb="menu"] *,
    ul[role="listbox"], 
    ul[role="listbox"] *,
    li[role="option"], 
    div[role="option"] {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    div[role="option"]:hover, 
    li[role="option"]:hover {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
    }

    /* Section Headings */
    .section-title {
        color: #1e3a8a !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        margin-top: 5px !important;
        margin-bottom: 2px !important;
    }
    .section-hint {
        color: #64748b !important;
        font-size: 12.5px !important;
        margin-top: 0px !important;
        margin-bottom: 16px !important;
        font-style: italic !important;
    }
    .subtle-divider {
        border: none !important;
        border-top: 1px solid #e2e8f0 !important;
        margin: 20px 0 !important;
    }

    /* Primary Predict Button styling */
    div.stButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* Mode Indicator Badge */
    .mode-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 6px;
        background-color: #e2e8f0;
        color: #475569;
        border: 1px solid #cbd5e1;
        font-weight: 500;
        z-index: 100;
    }

    /* Mobile view responsive styling overrides */
    @media (max-width: 600px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
        .portfolio-card {
            padding: 24px 20px !important;
        }
        .header-card {
            padding: 16px 20px !important;
            margin-bottom: 16px !important;
        }
        .header-card h1 {
            font-size: 20px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load helper model configurations
model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map, is_demo = load_models()

# Display mode indicator if in Demo mode
if is_demo:
    st.markdown("<div class='mode-badge'>Demo Mode (Mock Model)</div>", unsafe_allow_html=True)

# Header Card
st.markdown("""
<div class='header-card'>
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: block; margin: 0 auto 8px auto;">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        <path d="M12 8v8"/>
        <path d="M8 12h8"/>
    </svg>
    <h1>Workplace Mental Health Predictor</h1>
    <p>Assess workplace mental health support needs based on workplace factors.</p>
</div>
""", unsafe_allow_html=True)

# Form Helper dropdown select
def select(label, options, key=None):
    opts = ["— Select —"] + options
    return st.selectbox(label, opts, key=key)

# Assessment Form Container
st.markdown("<div class='portfolio-card'>", unsafe_allow_html=True)

with st.form("prediction_form", border=False):
    
    # 1. Personal Profile
    st.markdown("<div class='section-title'>Personal Profile</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Basic personal details to set demographic context.</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.selectbox("Age", list(range(18, 76)), index=10, key="age")
    with col2:
        gender = select("Gender", ["Male", "Female", "Other"], key="gender")
    with col3:
        family_history = select("Family history of mental illness?", ["No", "Yes"], key="fh")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 2. Work Setup
    st.markdown("<div class='section-title'>Work Setup</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Your day-to-day working environment and employment type.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        no_employees = select(
            "Company size",
            ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"], 
            key="emp"
        )
        self_employed = select("Are you self-employed?", ["No", "Yes"], key="se")
    with col2:
        remote_work = select("Works remotely?", ["Yes", "No"], key="rw")
        tech_company = select("Does your company primarily work in tech?", ["Yes", "No"], key="tc")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 3. Workplace Support
    st.markdown("<div class='section-title'>Workplace Support</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Assistance programs, benefits, and privacy protections.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        benefits = select("Mental health benefits provided?", ["Yes", "No"], key="ben")
        seek_help_display = select("Employer offers help resources?", ["Yes", "No", "Don't know"], key="sh")
    with col2:
        care_options = select("Aware of care options at work?", ["Yes", "No", "Not sure"], key="co")
        anonymity = select("Anonymity protected?", ["Yes", "No"], key="anon")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 4. Workplace Culture
    st.markdown("<div class='section-title'>Workplace Culture</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Workplace climate and observed consequences regarding mental health.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        mental_health_consequence = select("Discussing mental health has consequences?", ["Yes", "No", "Maybe"], key="mhc")
    with col2:
        # Simplified to 3 core choices: No, Yes, Maybe/Not sure
        obs_consequence = select(
            "Have you observed consequences for others?",
            ["No", "Yes", "Maybe/Not sure"], 
            key="oc"
        )

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 5. Social Comfort
    st.markdown("<div class='section-title'>Social Comfort</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-hint'>Your comfort levels discussing well-being with your peers and leads.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        coworkers = select("Comfortable discussing mental health with coworkers?", ["Yes", "Some of them", "Maybe", "No"], key="cw")
    with col2:
        supervisor = select("Comfortable discussing mental health with your supervisor?", ["Yes", "Some of them", "Maybe", "No"], key="sv")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Submit action
    submitted = st.form_submit_button("🔍 Predict Mental Health Risk")

st.markdown("</div>", unsafe_allow_html=True)

# Trigger inference & redirect
if submitted:
    fields = {
        "Gender"              : gender,
        "Family history"      : family_history,
        "Company size"        : no_employees,
        "Tech company"        : tech_company,
        "Self employed"       : self_employed,
        "Remote work"         : remote_work,
        "Benefits"            : benefits,
        "Care options"        : care_options,
        "Seek help"           : seek_help_display,
        "MH consequence"      : mental_health_consequence,
        "Observed consequence": obs_consequence,
        "Coworkers"           : coworkers,
        "Supervisor"          : supervisor,
        "Anonymity"           : anonymity,
    }

    unselected = [k for k, v in fields.items() if v == "— Select —"]

    if unselected:
        st.warning(f"⚠️ Please pick options for: {', '.join(unselected)}")
    else:
        try:
            # Perform prediction
            prob = calculate_risk(fields, age)
            
            # Store in session state
            st.session_state.results = {
                "prob": prob,
                "fields": fields,
                "age": age
            }
            # Redirect to results page
            st.switch_page("pages/prediction.py")
        except Exception as e:
            st.error(f"Inference pipeline error: {str(e)}")