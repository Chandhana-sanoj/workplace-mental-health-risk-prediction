import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="Mental Health Risk Predictor",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #e3f0dc 75%;
        background-image:
            radial-gradient(ellipse at top left, #cde7c5 0%, transparent 55%),
            radial-gradient(ellipse at bottom right, #edf7e7 0%, transparent 55%);
        background-attachment: fixed;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 4rem;
        padding-right: 4rem;
        padding-bottom: 4rem;
        max-width: 1100px;
    }

    .header-box {
        background:linear-gradient(135deg, #ffccd5 0%, #ffb3c1 100%);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 36px 40px;
        border-radius: 20px;
        margin-bottom: 32px;
        box-shadow: 0 4px 24px rgba(138, 56, 70, 0.08);
    }
    .header-box h1 {
        color: #2d5a30 !important;
        font-size: 30px !important;
        font-weight: 700 !important;
        margin: 0 0 8px 0 !important;
    }
    .header-box p {
        color: #065f46 !important;
        margin: 0 !important;
        font-size: 15px !important;
    }

    .section-label {
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2d5a30;
        margin: 28px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 1.5px solid #e0e7ff;
    }

    .result-high {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 2px 12px rgba(239,68,68,0.08);
    }
    .result-medium {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 2px 12px rgba(245,158,11,0.08);
    }
    .result-low {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 5px solid #22c55e;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 2px 12px rgba(34,197,94,0.08);
    }
    .result-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #111827;
    }
    .result-sub {
        font-size: 14px;
        color: #374151;
        line-height: 1.7;
    }

    .disclaimer {
        background: rgba(241, 245, 249, 0.8);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 13px;
        color: #64748b;
        margin-top: 24px;
        line-height: 1.8;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b6e3e, #2d5a30);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 14px 0;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        margin-top: 12px;
        box-shadow: 0 4px 12px rgba(99,102,241,0.3);
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div {
        background: rgba(255,255,255,0.85)!important;
        border-radius: 8px !important;
    }

    hr {
        border: none;
        border-top: 1px solid #e0e7ff;
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)


# Load models
@st.cache_resource
def load_models():
    base = "models/"
    with open(base + "mental_health_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open(base + "ord_enc_social.pkl", "rb") as f:
        ord_enc_social = pickle.load(f)
    with open(base + "label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    with open(base + "onehot_encoder.pkl", "rb") as f:
        ohe = pickle.load(f)
    with open(base + "minmax_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open(base + "no_emp_map.pkl", "rb") as f:
        no_emp_map = pickle.load(f)
    return model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map

model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map = load_models()


# Header 
st.markdown("""
<div class='header-box'>
    <h1>Workplace Mental Health Risk Predictor</h1>
    <p>
    Assess potential mental health support needs based on workplace
    conditions and personal factors.
    </p>
</div>
""", unsafe_allow_html=True)

def select(label, options, key=None):
    opts = ["— Select —"] + options
    return st.selectbox(label, opts, key=key)


# Form
with st.form("prediction_form"):

    st.markdown("<div class='section-label'>Personal Information</div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=75,
                              value=28, step=1)
    with col2:
        gender = select("Gender", ["Male", "Female", "Other"], key="gender")
    with col3:
        family_history = select(
            "Family history of mental illness?",
            ["No", "Yes"], key="fh")

    st.markdown("<div class='section-label'>Company Information</div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        no_employees = select(
            "Company size",
            ["1-5", "6-25", "26-100",
             "100-500", "500-1000", "More than 1000"], key="emp")
    with col2:
        tech_company = select("Tech company?", ["Yes", "No"], key="tc")
    with col3:
        self_employed = select("Self employed?", ["No", "Yes"], key="se")

    col1, col2, col3 = st.columns(3)
    with col1:
        remote_work = select("Works remotely?", ["Yes", "No"], key="rw")
    with col2:
        benefits = select(
            "Mental health benefits provided?",
            ["Yes", "No"], key="ben")

    st.markdown("<div class='section-label'>Workplace Support & Culture</div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        care_options = select(
            "Aware of care options at work?",
            ["Yes", "No", "Not sure"], key="co")
        mental_health_consequence = select(
            "Discussing MH has consequences?",
            ["Yes", "No", "Maybe"], key="mhc")
    with col2:
        seek_help_display = select(
            "Employer offers help resources?",
            ["Yes", "No", "Don't know"], key="sh")
        obs_consequence = select(
            "Observed consequences for others?",
            ["No", "Yes", "Yes, I experienced",
             "Yes, I observed", "Maybe/Not sure"], key="oc")
    with col3:
        coworkers = select(
            "Comfortable with coworkers?",
            ["Yes", "Some of them", "Maybe", "No"], key="cw")
        supervisor = select(
            "Comfortable with supervisor?",
            ["Yes", "Some of them", "Maybe", "No"], key="sv")

    col1, col2, col3 = st.columns(3)
    with col1:
        anonymity = select("Anonymity protected?", ["Yes", "No"], key="anon")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Predict Mental Health Risk")


# Prediction 
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
        st.warning(f"Please select: {', '.join(unselected)}")

    else:
        try:
            binary_map = {"Yes": 1, "No": 0}

            # seek_help — map display value to encoder value
            seek_help_map = {
                "Yes"        : "Yes",
                "No"         : "No",
                "Don't know" : "Don't know",
            }
            seek_help = seek_help_map[seek_help_display]

            # care_options — "Not sure" exists in encoder
            # encoder knows: 'I am not sure', 'No', 'Not sure', 'Yes'
            # so "Not sure" passes through directly

            # Encode no_employees
            no_emp_encoded = no_emp_map[no_employees]

            # Ordinal encode coworkers + supervisor
            social_df = pd.DataFrame(
                [[coworkers, supervisor]],
                columns=["coworkers", "supervisor"])
            social_encoded = ord_enc_social.transform(social_df)

            # Label encode
            care_enc = label_encoders['care_options'].transform(
                [care_options])[0]
            seek_enc = label_encoders['seek_help'].transform(
                [seek_help])[0]
            mhc_enc  = label_encoders['mental_health_consequence'].transform(
                [mental_health_consequence])[0]
            obs_enc  = label_encoders['obs_consequence'].transform(
                [obs_consequence])[0]

            # OneHot encode Gender
            gender_enc   = ohe.transform([[gender]])[0]
            gender_male  = gender_enc[0]
            gender_other = gender_enc[1] if len(gender_enc) > 1 else 0

            # Build feature row
            row = pd.DataFrame([[
                age,
                binary_map[self_employed],
                no_emp_encoded,
                binary_map[tech_company],
                binary_map[remote_work],
                binary_map[benefits],
                care_enc,
                seek_enc,
                binary_map[anonymity],
                mhc_enc,
                binary_map[family_history],
                social_encoded[0][0],
                social_encoded[0][1],
                obs_enc,
                gender_male,
                gender_other
            ]], columns=[
                'Age', 'self_employed', 'no_employees', 'tech_company',
                'remote_work', 'benefits', 'care_options', 'seek_help',
                'anonymity', 'mental_health_consequence', 'family_history',
                'coworkers', 'supervisor', 'obs_consequence',
                'Gender_Male', 'Gender_Other'
            ])

            # Scale Age
            row['Age'] = scaler.transform(row[['Age']])

            # Predict
            prob = model.predict_proba(row)[0][1]

            st.markdown("---")

            if prob >= 0.70:
                st.markdown(f"""
                <div class='result-high'>
                    <div class='result-title'>🔴 High Risk — {prob:.0%}</div>
                    <div class='result-sub'>
                    This person shows patterns strongly associated with needing
                    mental health support. Consider ensuring they are aware of
                    available resources and confidential support options.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif prob >= 0.45:
                st.markdown(f"""
                <div class='result-medium'>
                    <div class='result-title'>🟡 Moderate Risk — {prob:.0%}</div>
                    <div class='result-sub'>
                    Some factors suggest potential mental health support needs.
                    Ensure the person is aware of available resources and
                    feels comfortable seeking help when needed.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class='result-low'>
                    <div class='result-title'>🟢 Low Risk — {prob:.0%}</div>
                    <div class='result-sub'>
                    Current workplace conditions appear relatively supportive.
                    Continue maintaining open communication and ensure
                    resources remain visible and accessible.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"**Risk probability: {prob:.1%}**")
            st.progress(float(prob))

            with st.expander("Model details"):
                st.markdown("""
                **Model:** Logistic Regression (tuned, C=0.01)
                **Recall:** 0.802 · **F1:** 0.738 · **Accuracy:** 0.687
                **Dataset:** OSMI 2014 + 2016 · 2,679 responses
                **Reference:** Paul & Das (2023), IJSRA 10(01), 221–233
                """)

            st.markdown("""
            <div class='disclaimer'>
            ⚠️ <b>Screening tool only.</b> This is not a medical diagnosis.
            Predictions are based on statistical patterns from survey data
            and may not reflect individual circumstances. Always involve
            qualified mental health professionals in any support decisions.
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            st.info("Check that all model files are in the models/ folder.")