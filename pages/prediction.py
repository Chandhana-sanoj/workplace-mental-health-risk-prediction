import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="Assessment Results - Workplace Mental Health Predictor",
    page_icon="🧠",
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
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Main Container Card */
    .portfolio-card {
        background: #ffffff;
        border: 1px solid #d1e2f7;
        border-radius: 20px;
        padding: 35px 40px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.04);
    }

    /* Section titles */
    .section-title {
        color: #1e3a8a;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 24px;
        margin-bottom: 12px;
    }

    /* Score display elements */
    .result-header {
        text-align: center;
        padding-bottom: 15px;
    }
    .result-score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 15px 0;
    }
    .result-score {
        font-size: 64px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
    }
    .result-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .badge-low {
        background-color: #e2f5e9;
        color: #1b7a43;
        border: 1px solid #c4ecce;
    }
    .badge-medium {
        background-color: #fff6e0;
        color: #b27b00;
        border: 1px solid #ffe9b8;
    }
    .badge-high {
        background-color: #fde8e8;
        color: #c81e1e;
        border: 1px solid #f8b4b4;
    }

    .result-description {
        font-size: 14.5px;
        color: #475569;
        line-height: 1.6;
        text-align: center;
        margin-top: 8px;
        max-width: 580px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Comparative cards layout */
    .factor-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 15px;
    }
    @media (max-width: 600px) {
        .factor-container {
            grid-template-columns: 1fr;
        }
    }
    
    .factor-card {
        background: #ffffff;
        border: 1px solid #d1e2f7;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.02);
    }
    .factor-card-title {
        font-size: 13.5px;
        font-weight: 600;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .factor-list {
        margin: 0;
        padding-left: 18px;
        font-size: 13px;
        color: #475569;
        line-height: 1.5;
    }
    .factor-list li {
        margin-bottom: 6px;
    }

    /* Return button customized secondary styling */
    .stButton.secondary-btn > button {
        background: #ffffff !important;
        color: #2563eb !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }
    .stButton.secondary-btn > button:hover {
        background: #f1f5f9 !important;
        color: #1d4ed8 !important;
        border: 1px solid #cbd5e1 !important;
        transform: translateY(-1px) !important;
    }

    .disclaimer {
        background: rgba(241, 245, 249, 0.7);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px;
        font-size: 12px;
        color: #64748b;
        margin-top: 24px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Safety check for results session
if "results" not in st.session_state or st.session_state.results is None:
    st.markdown("""
    <div class="portfolio-card" style="margin-top: 40px; text-align: center;">
        <h2 style="color: #1e3a8a; margin-top: 0;">No Assessment Data Found</h2>
        <p style="color: #475569; margin-bottom: 24px;">Please complete the form on the homepage before viewing results.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
    if st.button("⬅️ Go to assessment form"):
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Retrieve results
res = st.session_state.results
prob = res["prob"]
fields = res["fields"]


if prob >= 0.70:
    level_class = "badge-high"
    level_text = "High Risk"
    color_hex = "#c81e1e"
    description = (
        "Your answers suggest that you might benefit from active mental health support. "
        "Setting healthy boundaries and checking what resources are available at work "
        "could be a helpful next step."
    )
elif prob >= 0.45:
    level_class = "badge-medium"
    level_text = "Moderate Risk"
    color_hex = "#b27b00"
    description = (
        "Some aspects of your workplace could be causing stress. Finding ways to discuss "
        "your workload with peers or direct leads might help improve balance."
    )
else:
    level_class = "badge-low"
    level_text = "Low Risk"
    color_hex = "#1b7a43"
    description = (
        "Your workspace environment seems supportive. Keep communicating openly "
        "and stay aware of your company's support options."
    )

# Main Result 
st.markdown(f"""
<div class='result-header'>
    <div class='result-score-container'>
        <div class='result-score' style='color: {color_hex};'>{prob:.0%}</div>
        <div class='result-badge {level_class}'>{level_text}</div>
    </div>
    <p class='result-description'>{description}</p>
</div>
""", unsafe_allow_html=True)

st.progress(prob)
st.markdown("</div>", unsafe_allow_html=True)

# Comparative factors 
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='factor-card-title' style='color: #1b7a43;'>What helps lower risk</div>", unsafe_allow_html=True)
    
    positives = []
    if fields["Benefits"] == "Yes":
        positives.append("Mental health benefits are provided by your employer.")
    if fields["Care options"] == "Yes":
        positives.append("You are aware of care options at the company.")
    if fields["Seek help"] == "Yes":
        positives.append("Your employer actively offers help resources.")
    if fields["Anonymity"] == "Yes":
        positives.append("Your anonymity is protected if you request care.")
    if fields["Supervisor"] == "Yes":
        positives.append("You feel comfortable talking with your direct supervisor.")
    if fields["Coworkers"] == "Yes":
        positives.append("You feel comfortable discussing health with coworkers.")
    if fields["MH consequence"] == "No":
        positives.append("No negative career consequences are expected for discussing wellness.")
    if fields["Remote work"] == "Yes":
        positives.append("Remote work option is available.")
        
    if positives:
        st.markdown("<ul class='factor-list'>" + "".join([f"<li>{item}</li>" for item in positives]) + "</ul>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size: 13px; color: #7f8c8d; font-style: italic;'>No key protective indicators reported in this assessment.</p>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='factor-card-title' style='color: #c81e1e;'>What might increase risk</div>", unsafe_allow_html=True)
    
    warnings = []
    if fields["Family history"] == "Yes":
        warnings.append("Family history of mental health conditions increases risk trends.")
    if fields["Benefits"] == "No":
        warnings.append("No mental health benefits are provided by your employer.")
    if fields["Care options"] == "No":
        warnings.append("Not aware of care resources or options at the company.")
    if fields["MH consequence"] == "Yes":
        warnings.append("Discussing wellness at work feels like it has career consequences.")
    if fields["Observed consequence"] in ["Yes", "Yes, I experienced", "Yes, I observed"]:
        warnings.append("Peers have faced negative consequences for discussing wellness.")
    if fields["Supervisor"] == "No":
        warnings.append("You do not feel comfortable talking with your supervisor.")
    if fields["Coworkers"] == "No":
        warnings.append("You do not feel comfortable discussing wellness with coworkers.")
    if fields["Anonymity"] == "No":
        warnings.append("Anonymity protection is not guaranteed.")
        
    if warnings:
        st.markdown("<ul class='factor-list'>" + "".join([f"<li>{item}</li>" for item in warnings]) + "</ul>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size: 13px; color: #7f8c8d; font-style: italic;'>No key risk factors reported in this assessment.</p>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Suggested steps for you</div>", unsafe_allow_html=True)

if prob >= 0.70:
    st.markdown("""
    1. **Check support resources available at work**: Learn about employee assistance programs or wellness benefits that could offer free, confidential therapy.
    2. **Set clear limits between work and home life**: Block out disconnect times and avoid looking at work messages outside of working hours.
    3. **Review insurance benefits**: Look through your company's benefit guides to see what clinical services are covered.
    """)
elif prob >= 0.45:
    st.markdown("""
    1. **Talk with trusted coworkers, family, or supervisor**: Share how you feel about your workload stress to find supportive steps forward.
    2. **Check support resources available at work**: Review company portals or guides for quick access to stress management materials.
    3. **Schedule small breaks**: Take simple 5-10 minute breaks during the workday to step away from screens and stretch.
    """)
else:
    st.markdown("""
    1. **Keep up healthy daily habits**: Maintain regular syncs with your team and ensure you shut off work on time.
    2. **Build team safety**: Encourage a supportive culture in your team by discussing balance and open wellness topics.
    3. **Keep links handy**: Save your company's wellness resource pages in case work pressures change over time.
    """)

# model details
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
with st.expander("About this project model"):
    st.markdown("""
    We built this model using a Logistic Regression algorithm trained on data from the 2014 & 2016 OSMI mental health surveys. 
    It looks at statistical trends across 2,679 survey responses to estimate risks.
    
    * **Metrics:** Recall is 80.2% · F1-Score is 73.8% · Accuracy is 68.7%.  
    * **Academic reference:** Paul & Das (2023), IJSRA journal.
    """)

# Take Assessment Again
st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
if st.button("⬅️ Take Assessment Again"):
    st.session_state.results = None
    st.switch_page("app.py")
st.markdown("</div>", unsafe_allow_html=True)

# Disclaimer Box
st.markdown("""
<div class='disclaimer'>
    ⚠️ <b>Please Note:</b> This is a student screening project, not a clinical tool or medical diagnosis. 
    It calculates general risk levels based on statistical patterns from survey answers. 
    Please speak to a qualified medical professional if you have any health concerns.
</div>
""", unsafe_allow_html=True)
