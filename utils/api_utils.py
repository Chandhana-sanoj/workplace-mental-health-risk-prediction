import pickle
import pandas as pd
import numpy as np
import streamlit as st

# Cache model 
@st.cache_resource
def load_models():
    base = "models/"
    try:
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
        return model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map, False
    except Exception:
        # Fallback
        return None, None, None, None, None, None, True
def calculate_risk(fields, age):
    model, ord_enc_social, label_encoders, ohe, scaler, no_emp_map, is_demo = load_models()
    
    if is_demo:
        
        base_prob = 0.35
        
        # Risk factors
        if fields["Family history"] == "Yes":
            base_prob += 0.20
        if fields["Benefits"] == "No":
            base_prob += 0.15
        if fields["Care options"] == "No":
            base_prob += 0.10
        if fields["MH consequence"] == "Yes":
            base_prob += 0.12
        if fields["Observed consequence"] in ["Yes", "Yes, I experienced", "Yes, I observed"]:
            base_prob += 0.15
        if fields["Anonymity"] == "No":
            base_prob += 0.10
        if fields["Coworkers"] in ["No", "Maybe"]:
            base_prob += 0.08
        if fields["Supervisor"] in ["No", "Maybe"]:
            base_prob += 0.10
        
        # Protective factors
        if fields["Benefits"] == "Yes" and fields["Care options"] == "Yes":
            base_prob -= 0.12
        if fields["Coworkers"] == "Yes" and fields["Supervisor"] == "Yes":
            base_prob -= 0.15
        if fields["Remote work"] == "Yes":
            base_prob -= 0.05
            
        prob = float(np.clip(base_prob, 0.05, 0.95))
        return prob
        
    else:
        
        binary_map = {"Yes": 1, "No": 0}
        seek_help_map = {
            "Yes"        : "Yes",
            "No"         : "No",
            "Don't know" : "Don't know",
        }
        
        gender = fields["Gender"]
        family_history = fields["Family history"]
        no_employees = fields["Company size"]
        tech_company = fields["Tech company"]
        self_employed = fields["Self employed"]
        remote_work = fields["Remote work"]
        benefits = fields["Benefits"]
        care_options = fields["Care options"]
        seek_help_display = fields["Seek help"]
        mental_health_consequence = fields["MH consequence"]
        obs_consequence = fields["Observed consequence"]
        coworkers = fields["Coworkers"]
        supervisor = fields["Supervisor"]
        anonymity = fields["Anonymity"]
        seek_help = seek_help_map[seek_help_display]
        no_emp_encoded = no_emp_map[no_employees]
        social_df = pd.DataFrame(
            [[coworkers, supervisor]],
            columns=["coworkers", "supervisor"]
        )
        social_encoded = ord_enc_social.transform(social_df)
        care_enc = label_encoders['care_options'].transform([care_options])[0]
        seek_enc = label_encoders['seek_help'].transform([seek_help])[0]
        mhc_enc  = label_encoders['mental_health_consequence'].transform([mental_health_consequence])[0]
        obs_enc  = label_encoders['obs_consequence'].transform([obs_consequence])[0]
        gender_enc   = ohe.transform([[gender]])[0]
        gender_male  = gender_enc[0]
        gender_other = gender_enc[1] if len(gender_enc) > 1 else 0
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
        row['Age'] = scaler.transform(row[['Age']])
        prob = float(model.predict_proba(row)[0][1])
        return prob
