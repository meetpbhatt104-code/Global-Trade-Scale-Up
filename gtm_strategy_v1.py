import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import google.generativeai as genai

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="Bharat-EU Genius Dashboard", layout="wide")

# Modern UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stMetric"] { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# API Keys (Replace with your actual keys)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
    genai.configure(api_key=GEMINI_API_KEY)

# --- 2. DATA ENGINES ---
@st.cache_data
def fetch_hsn_metadata():
    url = "https://comtradeapi.un.org/files/v1/app/reference/HS.json"
    return requests.get(url).json()['results']

def reset_session():
    st.session_state.confirmed_hs = None

# --- 3. SESSION STATE ---
if 'confirmed_hs' not in st.session_state:
    st.session_state.confirmed_hs = None

# --- 4. THE SEARCH HERO ---
if not st.session_state.confirmed_hs:
    st.title("🚀 Bharat-EU Export Intelligence")
    query = st.text_input("Search by Product Name or HS Code", placeholder="e.g. 'Steel' or '8481'")
    
    if query:
        data = fetch_hsn_metadata()
        matches = [i for i in data if query.lower() in i['text'].lower() or query in i['id']]
        if matches:
            selected = st.selectbox("Confirm Product:", matches, format_func=lambda x: f"HS {x['id']} - {x['text']}")
            if st.button("Unlock Strategy Dashboard →", type="primary"):
                st.session_state.confirmed_hs = selected['id']
                st.session_state.confirmed_text = selected['text']
                st.rerun()

# --- 5. THE RAG DASHBOARD ---
else:
    hs = st.session_state.confirmed_hs
    name = st.session_state.confirmed_text
    
    # Header & Reset
    col_h, col_r = st.columns([8, 2])
    col_h.title(f"Strategic Profile: {name}")
    col_r.button("New Search", on_click=reset_session)

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    chapter = hs[:2]
    is_scomet = chapter in ["84", "85", "88", "90"]
    is_cbam = chapter in ["72", "73", "76"]
    
    m1.metric("EU MFN Duty", "4.5%")
    m2.metric("SCOMET Status", "🚨 ALERT" if is_scomet else "✅ SAFE")
    m3.metric("CBAM Risk", "⚠️ HIGH" if is_cbam else "✅ LOW")
    m4.metric("Market Sentiment", "Bullish")

    # Tabs for Data and AI
    tab_data, tab_ai = st.tabs(["📊 Market Analytics", "🤖 RAG Strategy Analyst"])

    with tab_data:
        # Dynamic Chart
        df = pd.DataFrame({'Month': ['Jan', 'Feb', 'Mar', 'Apr'], 'Value': np.random.randint(10, 100, 4)})
        st.plotly_chart(px.line(df, x='Month', y='Value', title="Import Demand Curve"), use_container_width=True)

    with tab_ai:
        st.subheader("Context-Aware RAG Assistant")
        # Injects current dashboard context into Gemini
        if user_msg := st.chat_input("Ask about compliance or market entry..."):
            with st.chat_message("assistant"):
                context = f"User is exporting {name} (HS {hs}). SCOMET: {is_scomet}, CBAM: {is_cbam}."
                
                if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Context: {context}. User Question: {user_msg}")
                    st.write(response.text)
                else:
                    st.warning("Please configure your Gemini API Key to enable RAG features.")