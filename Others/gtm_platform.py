import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. THE PROBLEM SOLVING LAYER (JTBD: DATA ACCURACY) ---
# In a real app, this replaces hardcoded data with live API calls to UN Comtrade
def get_compliance_data(hs_code):
    database = {
        "8481": {"name": "Industrial Valves", "fta": "0% (EFTA)", "cbam": False, "scomet": False, "desc": "Taps, cocks, valves for pipes/tanks."},
        "8542": {"name": "Integrated Circuits", "fta": "0% (ITA-1)", "cbam": False, "scomet": True, "desc": "Electronic microassemblies."},
        "7308": {"name": "Steel Structures", "fta": "3.7% (MFN)", "cbam": True, "scomet": False, "desc": "Bridges, lock-gates, towers of iron/steel."},
        "8806": {"name": "Drones/UAVs", "fta": "0%", "cbam": False, "scomet": True, "desc": "Unmanned Aircraft Systems."}
    }
    return database.get(hs_code, {"name": "Generic Product", "fta": "Check Tariff", "cbam": False, "scomet": False, "desc": "General Category"})

# --- 2. THE UI/UX FRAMEWORK (JTBD: EASE OF USE) ---
st.set_page_config(page_title="Bharat-EU Export Engine", layout="wide")

# Dashboard Styling
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    [data-testid="stSidebar"] { border-right: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR: THE ANALYST (Secondary Support)
with st.sidebar:
    st.title("🤖 Strategy Analyst")
    st.markdown("I monitor your dashboard for risks.")
    query = st.text_input("Ask a specific strategy question:")
    if query:
        st.info(f"Analyzing {query}... Based on current selections, focus on Rule of Origin (RoO) documentation.")
    st.divider()
    st.caption("v1.2 | Data: Eurostat & DGFT Live")

# MAIN DASHBOARD (Primary Job)
st.title("🚀 Bharat-EU Export Command Center")

# A. INPUT SECTION
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search HS Code or Product Description", "8481")
        # Easy UI/UX: Auto-resolving the code
        product = get_compliance_data(search)
        st.caption(f"**Detected:** {product['name']} | {product['desc']}")
    with col2:
        country = st.selectbox("EU Market", ["Germany", "France", "Italy", "Netherlands"])
    with col3:
        currency = st.selectbox("Display Currency", ["EUR", "INR"])

st.divider()

# B. DATA VISUALIZATION (JTBD: IDENTIFYING DEMAND)
c1, c2, c3 = st.columns([2, 2, 1])

with c1:
    st.subheader("Import Demand Trend")
    # Simulated Trend Data
    df_trend = pd.DataFrame({
        'Month': ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Value': [10, 12, 11, 15, 19, 18],
        'Volume': [100, 115, 108, 140, 170, 165]
    })
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_trend['Month'], y=df_trend['Value'], name="Value (M €)", marker_color='#004d99'))
    fig.add_trace(go.Scatter(x=df_trend['Month'], y=df_trend['Volume'], name="Volume (MT)", yaxis="y2", line=dict(color="#ff9900")))
    fig.update_layout(yaxis2=dict(overlaying="y", side="right"), height=350, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Competitive Gap")
    # Comparison vs Competitor (China/Turkey)
    comp_df = pd.DataFrame({'Entity': ['India', 'China', 'Turkey'], 'Unit Price (€)': [110, 125, 140]})
    fig_comp = px.bar(comp_df, x='Entity', y='Unit Price (€)', color='Entity', color_discrete_sequence=['green', 'red', 'blue'])
    st.plotly_chart(fig_comp, use_container_width=True)

with c3:
    st.subheader("Compliance Pulse")
    # Quick Status Indicators
    st.metric("Import Duty", product['fta'])
    st.metric("CBAM Tax", "3% Risk" if product['cbam'] else "0%")
    st.metric("SCOMET", "Required" if product['scomet'] else "Exempt")

# C. STRATEGY OUTPUT (JTBD: RISK MITIGATION)
st.divider()
st.subheader("📝 Export Strategy & SCOMET Advisory")
s1, s2 = st.columns(2)

with s1:
    if product['scomet']:
        st.error("⚠️ SCOMET POLICY ALERT")
        st.write(f"Product {search} is classified as Dual-Use. You must apply for an export license via the DGFT portal using Form ANF-10A.")
    else:
        st.success("✅ NO SCOMET CONTROLS")
        st.write("This product is free for export to EU markets under standard commercial invoices.")

with s2:
    if product['cbam']:
        st.warning("📊 CBAM COMPLIANCE")
        st.write("The EU Importer will require your 'Embedded Emissions' report quarterly. Failure to provide this will result in a €50/tonne penalty.")
    else:
        st.info("ℹ️ FTA ADVANTAGE")
        st.write(f"Utilize the {product['fta']} to gain a landing cost advantage over non-FTA countries.")