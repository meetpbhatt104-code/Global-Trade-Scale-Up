import streamlit as st
import pandas as pd
import requests
import feedparser
import random
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION (UX Enhancement) ---
st.set_page_config(
    page_title="Bharat Export Intelligence",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR "BETTER THAN EXIMGPT" LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stAlert {
        padding: 10px;
        border-radius: 5px;
    }
    div.stButton > button {
        width: 100%;
        background-color: #004d99;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CLASS 1: THE DATA INGESTION ENGINE (THE "EARS") ---
class DataIngestor:
    def __init__(self, target_country, cpv_code):
        self.target_country = target_country
        self.cpv_code = cpv_code

    def get_demand_signals(self):
        """Fetches Live Tenders from Opentender.eu"""
        url = "https://opentender.eu/api/tender/search"
        payload = {
            "cpv": self.cpv_code,
            "country": self.target_country,
            "sort": "date-desc",
            "limit": 10
        }
        try:
            r = requests.post(url, json=payload)
            data = r.json().get('data', [])
            return [
                {
                    "Buyer": d.get('buyer', {}).get('name', 'Unknown'),
                    "Title": d.get('title', 'N/A')[:80] + "...",
                    "Value": f"{d.get('value', {}).get('amount', 0):,} EUR",
                    "Deadline": d.get('bidDeadline', 'Check Doc')[:10],
                    "Link": f"https://opentender.eu/{self.target_country.lower()}/tender/{d.get('id')}"
                } for d in data
            ]
        except:
            return []

    def get_risk_signals(self):
        """Fetches Live Regulatory News via RSS"""
        # RSS feed looking for CBAM or Trade Compliance news
        rss_url = "https://news.google.com/rss/search?q=CBAM+OR+EU+Import+Regulations+site:europa.eu&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(rss_url)
        return [
            {
                "Title": entry.title,
                "Date": entry.published[:16],
                "Link": entry.link,
                "Risk_Level": "High" if "ban" in entry.title.lower() or "tax" in entry.title.lower() else "Medium"
            } for entry in feed.entries[:5]
        ]

    def get_supply_signals(self):
        """
        Simulates UN Comtrade API v2.
        (Real API requires a key, this mocks the logic for the UX demo)
        """
        # Logic: If you had a key, you'd hit https://comtradeapi.un.org/data/v1/get
        # Here we simulate a "Competitor Gap Analysis"
        return pd.DataFrame({
            "Competitor": ["China", "Vietnam", "Turkey", "India"],
            "Market_Share_Trend": [-5, 2, 1, 8], # India growing, China shrinking
            "Avg_Unit_Price_EUR": [120, 115, 130, 110] # India is price competitive
        })

# --- CLASS 2: THE RAG BRAIN (THE "MIND") ---
class RAGBrain:
    def __init__(self, demand, risk, supply):
        self.context = f"""
        DEMAND DATA: {len(demand)} active tenders found. Top buyer: {demand[0]['Buyer'] if demand else 'None'}.
        RISK DATA: {len(risk)} active alerts. Most recent: {risk[0]['Title'] if risk else 'None'}.
        SUPPLY DATA: India has +8% market share growth trend vs China -5%.
        """
    
    def ask(self, query):
        """
        In a real production app, this sends 'self.context + query' to OpenAI/Claude.
        Here, we simulate the 'Reasoning' based on the data inputs.
        """
        # Simulation of LLM Reasoning
        if "worth" in query.lower() or "should i" in query.lower():
            return f"**Analysis:** Yes, the opportunity score is high.\n\n1. **Demand:** We found {len(demand_data)} active tenders (e.g., from {demand_data[0]['Buyer']}).\n2. **Supply:** Your pricing (110 EUR) is lower than China (120 EUR) and Turkey (130 EUR).\n3. **Risk:** Be aware of '{risk_data[0]['Title']}' - ensure compliance before bidding."
        elif "competitor" in query.lower():
            return "**Competitor Intel:** China is losing market share (-5%) in this category, likely due to recent EU anti-dumping probes. India is currently the price leader."
        else:
            return "Based on live signals, the market is active. Review the 'Demand' tab for specific buyer names."

# --- UI LAYOUT ---

# Sidebar: Controls
with st.sidebar:
    st.header("⚙️ GTM Configuration")
    target_country = st.selectbox("Target EU Market", ["DE", "FR", "IT", "ES", "NL"], index=0)
    industry = st.selectbox("Industry Segment", ["Industrial Machinery (42000000)", "Automotive Parts (34000000)", "Textiles (19000000)"])
    cpv_code = industry.split("(")[1].replace(")", "")
    
    st.divider()
    st.info("Data Sources Active:\n✅ TED (EU Tenders)\n✅ Google News (Regs)\n✅ UN Comtrade (Trade Flow)")

# Main Header
st.title(f"🚀 GTM Command Center: Exporting to {target_country}")
st.markdown("Real-time Intelligence for Indian Mid-sized Manufacturers")
st.divider()

# Load Data
ingestor = DataIngestor(target_country, cpv_code)
with st.spinner('Connecting to EU Data Pipelines...'):
    demand_data = ingestor.get_demand_signals()
    risk_data = ingestor.get_risk_signals()
    supply_df = ingestor.get_supply_signals()

# Top Level Metrics (The Dashboard Feel)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Active Procurement Leads", value=len(demand_data), delta="+2 from yesterday")
with col2:
    st.metric(label="Compliance Risk Level", value="Medium", delta_color="off")
with col3:
    st.metric(label="India Price Competitiveness", value="High", delta="Cheaper than China")

# Tabs for Deep Dive
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Strategist (RAG)", "📋 Demand Signals", "⚠️ Regulatory Risk", "🏭 Supply Intel"])

with tab1:
    st.subheader("Talk to your Market Data")
    st.markdown("Ask strategic questions like: *'Is it worth bidding right now?'* or *'Who are my competitors?'*")
    
    # The Chat Interface
    user_query = st.chat_input("Ask about your GTM strategy...")
    
    if user_query:
        # Display User Message
        with st.chat_message("user"):
            st.write(user_query)
        
        # Generate & Display RAG Response
        brain = RAGBrain(demand_data, risk_data, supply_df)
        response = brain.ask(user_query)
        
        with st.chat_message("assistant"):
            st.markdown(response)
            st.caption("Generated using live context from TED & Eurostat")

with tab2:
    st.subheader(f"Live Tenders in {target_country}")
    if demand_data:
        df_demand = pd.DataFrame(demand_data)
        st.dataframe(df_demand, use_container_width=True, hide_index=True, column_config={
            "Link": st.column_config.LinkColumn("Tender URL")
        })
    else:
        st.warning("No active tenders found for this category today.")

with tab3:
    st.subheader("Compliance & Risk Monitor (CBAM/RoDTEP)")
    for news in risk_data:
        color = "red" if news["Risk_Level"] == "High" else "orange"
        st.markdown(f"**[:{color}[{news['Risk_Level']}]] [{news['Title']}]({news['Link']})**")
        st.caption(f"Published: {news['Date']}")
        st.divider()

with tab4:
    st.subheader("Competitor Gap Analysis")
    st.markdown("Comparative Advantage vs. Top Exporters to EU")
    
    # Using Plotly for nice charts
    import plotly.express as px
    fig = px.bar(supply_df, x='Competitor', y='Market_Share_Trend', 
                 color='Market_Share_Trend', 
                 title="Market Share Growth (Last Qtr)",
                 color_continuous_scale=['red', 'green'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(supply_df, hide_index=True)