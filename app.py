import streamlit as st
import os
from utils.api_utils import calculate_risk, load_models

# Page config
st.set_page_config(
    page_title="Workplace Mental Health Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #dbeafe !important;
        background-image: linear-gradient(to bottom, #edf6ff 0%, #dbeafe 50%, #bfdbfe 100%) !important;
        background-attachment: fixed !important;
    }

    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Dark Blue Gradient Header Card */
    .header-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        border: none;
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
        text-align: center;
    }
    .header-card h1 {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin: 0 0 8px 0 !important;
        letter-spacing: 0.5px !important;
    }
    .header-card p {
        color: #cbd5e1 !important; /* Soft gray text */
        font-size: 14.5px !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }

    /* Form Container Card */
    .portfolio-card {
        background: #ffffff;
        border: 1px solid #d1e2f7;
        border-radius: 20px;
        padding: 35px 40px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.04);
    }

    /* Section Headings */
    .section-title {
        color: #1e3a8a;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 5px;
        margin-bottom: 12px;
    }
    .subtle-divider {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 20px 0;
    }

    /* Primary Predict Button styling */
    div.stButton > button {
        background: #2563eb !important; /* Royal Blue */
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
        background: #1d4ed8 !important; /* Darker blue */
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* Input elements style customization */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #f8fafc !important;
    }
    .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #f8fafc !important;
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
    }
</style>
""", unsafe_allow_html=True)

# model configurations
model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map, is_demo = load_models()

if is_demo:
    st.markdown("<div class='mode-badge'>Demo Mode (Mock Model)</div>", unsafe_allow_html=True)

# Header Card
st.markdown("""
<div class='header-card'>
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: block; margin: 0 auto 12px auto;">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        <path d="M12 8v8"/>
        <path d="M8 12h8"/>
    </svg>
    <h1>Workplace Mental Health Predictor</h1>
    <p>Assess workplace mental health support needs based on workplace factors.</p>
</div>
""", unsafe_allow_html=True)

# Form dropdown
def select(label, options, key=None):
    opts = ["— Select —"] + options
    return st.selectbox(label, opts, key=key)

#Container

with st.form("prediction_form", border=False):
    
    # 1. Personal Profile
    st.markdown("<div class='section-title'>Personal Profile</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=75, value=28, step=1)
    with col2:
        gender = select("Gender", ["Male", "Female", "Other"], key="gender")
    with col3:
        family_history = select("Family history of mental illness?", ["No", "Yes"], key="fh")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 2. Company Environment
    st.markdown("<div class='section-title'>Company & Working Conditions</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        no_employees = select(
            "Company size",
            ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"], 
            key="emp"
        )
    with col2:
        tech_company = select("Tech company?", ["Yes", "No"], key="tc")
    with col3:
        self_employed = select("Self employed?", ["No", "Yes"], key="se")

    col1, col2 = st.columns(2)
    with col1:
        remote_work = select("Works remotely?", ["Yes", "No"], key="rw")
    with col2:
        benefits = select("Mental health benefits provided?", ["Yes", "No"], key="ben")

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 3. Culture & Support
    st.markdown("<div class='section-title'>Workplace Culture & Resources</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        care_options = select("Aware of care options at work?", ["Yes", "No", "Not sure"], key="co")
        mental_health_consequence = select("Discussing MH has consequences?", ["Yes", "No", "Maybe"], key="mhc")
    with col2:
        seek_help_display = select("Employer offers help resources?", ["Yes", "No", "Don't know"], key="sh")
        obs_consequence = select(
            "Observed consequences for others?",
            ["No", "Yes", "Yes, I experienced", "Yes, I observed", "Maybe/Not sure"], 
            key="oc"
        )

    st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)

    # 4. Social Support & Safety
    st.markdown("<div class='section-title'>Social Support & Safety</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        coworkers = select("Comfortable with coworkers?", ["Yes", "Some of them", "Maybe", "No"], key="cw")
    with col2:
        supervisor = select("Comfortable with supervisor?", ["Yes", "Some of them", "Maybe", "No"], key="sv")
    with col3:
        anonymity = select("Anonymity protected?", ["Yes", "No"], key="anon")

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
            
            
            st.session_state.results = {
                "prob": prob,
                "fields": fields,
                "age": age
            }
            # Redirect to results page
            st.switch_page("pages/prediction.py")
        except Exception as e:
            st.error(f"Inference pipeline error: {str(e)}")


