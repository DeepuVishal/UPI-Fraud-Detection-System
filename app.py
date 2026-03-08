import streamlit as st
import pandas as pd
import base64
import time
from datetime import datetime
import plotly.express as px

# --- 1. SYSTEM CONFIGURATION ---
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


# --- 2. CORPORATE UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    .stApp { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #FFFFFF; }
    header, footer { visibility: hidden; }
    div.stButton > button {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: uppercase;
    }
    div.stButton > button:hover { color: #1A73E8 !important; text-decoration: underline !important; }
    .login-section { text-align: center; margin-top: 120px; }
    .field-label { color: #FFFFFF; font-size: 14px; font-weight: 600; display: block; margin-top: 15px; margin-bottom: 5px; }
    .status-alert { padding: 25px; border-radius: 10px; text-align: center; font-weight: 800; font-size: 26px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION LOGIC ---
if 'page' not in st.session_state: st.session_state.page = 'Home'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'logs' not in st.session_state: st.session_state.logs = []

# --- 4. TOP RIGHT NAVIGATION ---
_, nav_r = st.columns([1.5, 1])
with nav_r:
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("HOME"): st.session_state.page = 'Home'
    with n2:
        if st.button("LOGIN"): st.session_state.page = 'Login'
    with n3:
        if st.button("SCANNER"): st.session_state.page = 'Scanner'
    with n4:
        if st.button("ANALYSIS"): st.session_state.page = 'Analysis'

# --- 5. PAGE MODULES ---

if st.session_state.page == 'Home':
    set_bg_image(r"frontpage.jpg")
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 6rem; font-weight: 900;'>UPI FRAUD DETECTION</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='opacity:0.9; background:rgba(0,0,0,0.4); display:inline-block; padding:5px 15px;'>Predictive Forensic Intelligence Terminal</h3>",
        unsafe_allow_html=True)

elif st.session_state.page == 'Login':
    set_bg_color("#001f3f")
    st.markdown(
        "<div class='login-section'><h1>Administrative Portal</h1><p>Enter forensic security credentials to proceed.</p></div>",
        unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1, 1])
    with col_m:
        u_id = st.text_input("ADMIN ID", placeholder="User Identification")
        u_pw = st.text_input("ACCESS KEY", type="password", placeholder="••••••••")
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
            st.markdown("<span class='field-label'>Amount (INR)</span>", unsafe_allow_html=True)
            amt = st.number_input("", min_value=0.0, label_visibility="collapsed")
            st.markdown("<span class='field-label'>UPI Interface</span>", unsafe_allow_html=True)
            u_app = st.selectbox("", ["GPay", "PhonePe", "Paytm", "BHIM", "Amazon Pay", "PayZapp", "WhatsApp Pay"],
                                 label_visibility="collapsed")
            st.markdown("<span class='field-label'>Financial Institution</span>", unsafe_allow_html=True)
            u_bank = st.selectbox("", ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "BOB", "PNB", "Canara", "Union Bank",
                                       "IndusInd"], label_visibility="collapsed")

        with c2:
            st.markdown("<span class='field-label'>Agent Type (Behavior Pattern)</span>", unsafe_allow_html=True)
            # MERGED: AGENT TYPE DROPDOWN ADDED HERE
            agent_type = st.selectbox("", ["Normal", "Dormant", "Fraud", "Bot", "Impatient"],
                                      label_visibility="collapsed")

            st.markdown("<span class='field-label'>Payment Mode</span>", unsafe_allow_html=True)
            u_meth = st.selectbox("", ["upi", "qr_code", "collect"], label_visibility="collapsed")

            st.markdown("<span class='field-label'>Transaction Velocity (Attempts)</span>", unsafe_allow_html=True)
            u_att = st.number_input("", min_value=1, label_visibility="collapsed")

        if st.button("EXECUTE ML DIAGNOSTICS", use_container_width=True):
            with st.spinner("Analyzing Behavior Patterns..."):
                time.sleep(1)

                # --- UPDATED MULTI-PATTERN LOGIC ---
                is_fraud = False

                # 1. NEW RULE: HIGH RISK AGENT TYPES
                if agent_type in ["Fraud", "Bot", "Impatient"]:
                    is_fraud = True

                # 2. BOT & IMPATIENT PATTERN (Extreme Velocity)
                elif u_att >= 11:
                    is_fraud = True

                # 3. MICRO-FRAUD PATTERN (Small amount + Moderate attempts)
                elif amt < 150 and u_att >= 6:
                    is_fraud = True

                # 4. HIGH VALUE OUTLIER
                elif amt > 50000:
                    is_fraud = True

            if is_fraud:
                st.markdown(
                    f"<div class='status-alert' style='background:#D93025;'>🚨 FRAUDULENT PATTERN IDENTIFIED ({agent_type})</div>",
                    unsafe_allow_html=True)
                st.image("https://cdn-icons-png.flaticon.com/512/5974/5974771.png", width=250)
            else:
                st.markdown(
                    "<div class='status-alert' style='background:#1E8E3E;'>✅ SECURE: TRANSACTION VERIFIED</div>",
                    unsafe_allow_html=True)
                st.image("https://cdn-icons-png.flaticon.com/512/5610/5610944.png", width=250)

            st.session_state.logs.append({"Time": datetime.now().strftime("%H:%M"), "Bank": u_bank, "Amount": amt,
                                          "Verdict": "FRAUD" if is_fraud else "SAFE"})

elif st.session_state.page == 'Analysis':
    if not st.session_state.logged_in:
        st.error("Login Required.")
    else:
        set_bg_image(r"analayis.jpg")
        st.markdown("<h2 style='margin-top:80px;'>Forensic Intelligence Dashboard</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.logs) if st.session_state.logs else pd.DataFrame(
            {'Verdict': ['SAFE', 'FRAUD'], 'Bank': ['SBI', 'HDFC'], 'Amount': [1000, 45000]})
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(df, names='Verdict', title="Risk Distribution", hole=0.5, color='Verdict',
                             color_discrete_map={'SAFE': '#1E8E3E', 'FRAUD': '#D93025'})
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            fig_bar = px.bar(df, x='Bank', y='Amount', color='Verdict', title="Institution Risk Exposure",
                             barmode='group', color_discrete_map={'SAFE': '#1E8E3E', 'FRAUD': '#D93025'})
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)
