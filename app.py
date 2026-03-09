import streamlit as st
import pandas as pd
import base64
import time
import pickle
from datetime import datetime
import plotly.express as px
import xgboost as xgb

# --- 1. LOAD MODEL AND ENCODERS ---
try:
    with open('train_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('upi_encoder.pkl', 'rb') as f:
        upi_encoder = pickle.load(f)
    with open('bank_encoder.pkl', 'rb') as f:
        bank_encoder = pickle.load(f)
    with open('payment_encoder.pkl', 'rb') as f:
        payment_encoder = pickle.load(f)
except Exception as e:
    st.error("Model files not found. Please run train_model.py first.")

# --- 2. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="UPI FRAUD DETECTION", layout="wide", initial_sidebar_state="collapsed")


def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""


def set_bg_image(image_path):
    bin_str = get_base64(image_path)
    if bin_str:
        st.markdown(
            f"""<style>.stApp {{ background-image: url("data:image/png;base64,{bin_str}"); background-size: cover; background-attachment: fixed; }}</style>""",
            unsafe_allow_html=True)


def set_bg_color(color):
    st.markdown(f"""<style>.stApp {{ background: {color}; background-image: none; }}</style>""", unsafe_allow_html=True)


# --- 3. UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    .stApp { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #FFFFFF; }
    header, footer { visibility: hidden; }
    div.stButton > button {
        background-color: transparent !important; color: #FFFFFF !important;
        border: none !important; font-weight: 700 !important; font-size: 14px !important; text-transform: uppercase;
    }
    div.stButton > button:hover { color: #1A73E8 !important; text-decoration: underline !important; }
    .field-label { color: #FFFFFF; font-size: 14px; font-weight: 600; display: block; margin-top: 15px; margin-bottom: 5px; }
    .status-alert { padding: 25px; border-radius: 10px; text-align: center; font-weight: 800; font-size: 26px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION LOGIC ---
if 'page' not in st.session_state: st.session_state.page = 'Home'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'logs' not in st.session_state: st.session_state.logs = []

# --- 5. NAVIGATION ---
_, nav_r = st.columns([1, 1.2])
with nav_r:
    n1, n2, n3, n4, n5 = st.columns(5)
    with n1:
        if st.button("HOME"): st.session_state.page = 'Home'
    with n2:
        if st.button("LOGIN"): st.session_state.page = 'Login'
    with n3:
        if st.button("SCANNER"): st.session_state.page = 'Scanner'
    with n4:
        if st.button("ANALYSIS"): st.session_state.page = 'Analysis'
    with n5:
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.page = 'Home'
            st.rerun()

# --- 6. PAGE MODULES ---

if st.session_state.page == 'Home':
    set_bg_image(r"C:\Users\DEEPIKA\PycharmProjects\upi_fraud_detection\model\frontpage.jpg")
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size: 3.5rem; font-weight: 900;'>AN INTELLIGENT ML-BASED<br>UPI FRAUD DETECTION SYSTEM</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<h3 style='opacity:0.9; background:rgba(0,0,0,0.4); display:inline-block; padding:5px 15px;'>Predictive Forensic Intelligence Terminal</h3>",
        unsafe_allow_html=True)

elif st.session_state.page == 'Login':
    set_bg_color("#001f3f")
    st.markdown(
        "<div style='text-align:center; margin-top:100px;'><h1>Administrative Portal</h1><p>Enter forensic security credentials.</p></div>",
        unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1, 1])
    with col_m:
        u_id = st.text_input("ADMIN ID", placeholder="User ID")
        u_pw = st.text_input("ACCESS KEY", type="password", placeholder="••••")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u_id == "CDE" and u_pw == "2026":
                st.session_state.logged_in = True
                st.session_state.page = 'Scanner'
                st.rerun()
            else:
                st.error("Access Denied.")

elif st.session_state.page == 'Scanner':
    if not st.session_state.logged_in:
        st.warning("Please Login First.")
    else:
        set_bg_color("#001f3f")
        st.markdown("<h2 style='margin-top:40px;'>Transaction Anomaly Scanner</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<span class='field-label'>1. Transaction Amount (INR)</span>", unsafe_allow_html=True)
            amt = st.number_input("Amount", min_value=0.0, label_visibility="collapsed", key="amt_in")

            st.markdown("<span class='field-label'>2. UPI App</span>", unsafe_allow_html=True)
            u_app = st.selectbox("App", ["Amazon Pay", "BHIM", "GPay", "Paytm", "PhonePe", "PayZapp", "WhatsApp Pay"],
                                 label_visibility="collapsed", key="app_in")

            st.markdown("<span class='field-label'>3. Financial Institution (Bank)</span>", unsafe_allow_html=True)
            u_bank = st.selectbox("Bank", ["Axis", "BOB", "Canara", "HDFC", "ICICI", "Kotak", "PNB", "SBI"],
                                  label_visibility="collapsed", key="bank_in")

            st.markdown("<span class='field-label'>4. Payment Method</span>", unsafe_allow_html=True)
            u_meth = st.selectbox("Method", ["QR Scan", "Mobile Number", "UPI ID"], label_visibility="collapsed",
                                  key="meth_in")

        with c2:
            st.markdown("<span class='field-label'>5. Hour of Transaction (0-23)</span>", unsafe_allow_html=True)
            u_hour = st.slider("Hour", 0, 23, 12, label_visibility="collapsed", key="hour_in")

            st.markdown("<span class='field-label'>6. Night Transaction?</span>", unsafe_allow_html=True)
            u_night = st.selectbox("Night", ["False", "True"], label_visibility="collapsed", key="night_in")

            st.markdown("<span class='field-label'>7. Weekend Transaction?</span>", unsafe_allow_html=True)
            u_weekend = st.selectbox("Weekend", ["False", "True"], label_visibility="collapsed", key="week_in")

            st.markdown("<span class='field-label'>8. Attempt Count (Velocity)</span>", unsafe_allow_html=True)
            u_att = st.number_input("Attempts", min_value=1, step=1, label_visibility="collapsed", key="att_in")

        if st.button("EXECUTE ML DIAGNOSTICS", use_container_width=True):
            with st.spinner("Processing XGBoost Inference..."):
                time.sleep(1)

                # 1. Encode Inputs
                app_enc = upi_encoder.transform([u_app])[0]
                bank_enc = bank_encoder.transform([u_bank])[0]
                meth_enc = payment_encoder.transform([u_meth])[0]
                is_night_val = 1.0 if u_night == "True" else 0.0
                is_week_val = 1.0 if u_weekend == "True" else 0.0

                # 2. Create DataFrame with Float types (Important for XGBoost)
                input_df = pd.DataFrame([{
                    'Amount': float(amt),
                    'UPI_App': float(app_enc),
                    'Bank': float(bank_enc),
                    'Payment_Method': float(meth_enc),
                    'Hour': float(u_hour),
                    'Is_Night': is_night_val,
                    'Is_Weekend': is_week_val,
                    'Attempt_Count': float(u_att)
                }])

                # 3. Predict
                prediction = model.predict(input_df)[0]
                is_fraud = bool(prediction)

            if is_fraud:
                st.markdown(
                    f"<div class='status-alert' style='background:#D93025;'>🚨 FRAUDULENT PATTERN IDENTIFIED</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div class='status-alert' style='background:#1E8E3E;'>✅ SECURE: TRANSACTION VERIFIED</div>",
                    unsafe_allow_html=True)

            st.session_state.logs.append({"Time": datetime.now().strftime("%H:%M"), "Bank": u_bank, "Amount": amt,
                                          "Verdict": "FRAUD" if is_fraud else "SAFE"})

elif st.session_state.page == 'Analysis':
    if not st.session_state.logged_in:
        st.error("Login Required.")
    else:
        set_bg_image(r"C:\Users\DEEPIKA\PycharmProjects\upi_fraud_detection\model\analayis.jpg")
        st.markdown("<h2 style='margin-top:80px;'>Forensic Intelligence Dashboard</h2>", unsafe_allow_html=True)
        df_logs = pd.DataFrame(st.session_state.logs) if st.session_state.logs else pd.DataFrame(
            {'Verdict': ['SAFE', 'FRAUD'], 'Bank': ['SBI', 'HDFC'], 'Amount': [1000, 45000]})

        st.dataframe(df_logs, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(df_logs, names='Verdict', title="Risk Distribution", hole=0.5, color='Verdict',
                             color_discrete_map={'SAFE': '#1E8E3E', 'FRAUD': '#D93025'})
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            fig_bar = px.bar(df_logs, x='Bank', y='Amount', color='Verdict', title="Institution Risk Exposure",
                             color_discrete_map={'SAFE': '#1E8E3E', 'FRAUD': '#D93025'})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)
