import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

st.set_page_config(page_title="Retail Market Gap Analysis", layout="wide")

st.title("🛒 Actual vs Potential Retail Analysis")
st.markdown("Comparing **942 Current Customers** against estimated total regional retail outlets (Wholesale & Supermarkets).")

# 1. ENHANCED DATASET (Geo + Potential Model)
@st.cache_data
def get_analysis_data():
    # Columns: Area, Actual_Customers, Lat, Lon, County, Sub_County, Est_Market_Density (Potential Outlets)
    geo_data = [
        ['EASTLEIGH', 81, -1.2741, 36.8485, 'Nairobi', 'Kamkunji', 850],
        ['NAIROBI CBD', 71, -1.2833, 36.8233, 'Nairobi', 'Starehe', 1200],
        ['THIKA', 45, -1.0333, 37.0692, 'Kiambu', 'Thika West', 450],
        ['KAMITI RD', 43, -1.2050, 36.8900, 'Nairobi', 'Roysambu', 300],
        ['KITUI', 43, -1.3683, 37.9944, 'Kitui', 'Kitui Central', 250],
        ['MOMBASA RD', 40, -1.3340, 36.8625, 'Nairobi', 'Embakasi South', 400],
        ['KAYOLE', 37, -1.2673, 36.9314, 'Nairobi', 'Embakasi Central', 550],
        ['RUIRU-JUJA', 36, -1.1167, 36.9667, 'Kiambu', 'Ruiru', 420],
        ['NAIROBI WEST', 34, -1.3033, 36.8200, 'Nairobi', 'Langata', 200],
        ['KADAMALA', 32, -1.3150, 36.8850, 'Nairobi', 'Embakasi East', 280],
        ['UMOJA', 31, -1.2825, 36.8970, 'Nairobi', 'Embakasi West', 350],
        ['RONGAI', 29, -1.3931, 36.7420, 'Kajiado', 'Kajiado North', 310],
        ['UTAWALA', 27, -1.2750, 36.9830, 'Nairobi', 'Embakasi East', 250],
        ['KASA-MWIKI', 26, -1.2250, 36.9080, 'Nairobi', 'Kasarani', 280],
        ['WANGIGE-LIMURU', 26, -1.2260, 36.6740, 'Kiambu', 'Kabete', 220],
        ['GARISSA', 25, -0.4532, 39.6461, 'Garissa', 'Garissa Township', 200],
        ['MACHAKOS', 23, -1.5177, 37.2634, 'Machakos', 'Machakos Town', 300],
        ['PIPELINE', 21, -1.3144, 36.8981, 'Nairobi', 'Embakasi South', 450],
        ['KILIMANI', 20, -1.2913, 36.7880, 'Nairobi', 'Dagoretti North', 150],
        ['KAWANGWARE', 20, -1.2861, 36.7450, 'Nairobi', 'Dagoretti North', 380],
        ['GITHURAI 45', 17, -1.2050, 36.9150, 'Kiambu', 'Ruiru', 400],
        ['MWINGI', 16, -0.9333, 38.0667, 'Kitui', 'Mwingi Central', 120],
        ['NGONG', 15, -1.3621, 36.6565, 'Kajiado', 'Kajiado North', 180],
        ['WOTE', 14, -1.7808, 37.6258, 'Makueni', 'Makueni', 110],
        ['KIBWEZI', 14, -2.4167, 37.9667, 'Makueni', 'Kibwezi East', 90],
        ['KIAMBU', 13, -1.1714, 36.8356, 'Kiambu', 'Kiambu Town', 200],
        ['OLOITOKTOK', 12, -2.8500, 37.5167, 'Kajiado', 'Kajiado South', 80],
        ['KANGUNDO RD', 12, -1.2660, 36.9610, 'Nairobi', 'Njiru', 220],
        ['PARKLANDS', 12, -1.2628, 36.8156, 'Nairobi', 'Westlands', 130],
        ['KIKUYU', 10, -1.2430, 36.6714, 'Kiambu', 'Kikuyu', 160],
        ['MATUU', 10, -1.1333, 37.5500, 'Machakos', 'Yatta', 80],
        ['EMALI', 10, -2.0667, 37.4667, 'Makueni', 'Kibwezi West', 75],
        ['NAMANGA', 8, -2.5500, 36.7833, 'Kajiado', 'Kajiado Central', 60],
        ['WAIYAKI WAY', 8, -1.2630, 36.7620, 'Nairobi', 'Westlands', 110],
        ['KAJIADO', 7, -1.8500, 36.7833, 'Kajiado', 'Kajiado Central', 90],
        ['ISINYA', 7, -1.6667, 36.8500, 'Kajiado', 'Kajiado East', 70],
        ['MAKINDU', 7, -2.2833, 37.8167, 'Makueni', 'Kibwezi West', 80],
        ['KIBRA', 6, -1.3122, 36.7876, 'Nairobi', 'Kibra', 450],
        ['JOGOO RD', 6, -1.2900, 36.8550, 'Nairobi', 'Makadara', 200],
        ['SULTAN HAMUD', 5, -2.0167, 37.3667, 'Makueni', 'Kibwezi West', 55],
        ['JOGOO ROAD', 5, -1.2900, 36.8551, 'Nairobi', 'Makadara', 200],
        ['NUNGUNI', 4, -1.6833, 37.2833, 'Makueni', 'Kaiti', 40],
        ['BISIL', 4, -2.1333, 36.7833, 'Kajiado', 'Kajiado Central', 45],
        ['TALA', 3, -1.2833, 37.2667, 'Machakos', 'Matungulu', 95],
        ['KAREN', 3, -1.3200, 36.7020, 'Nairobi', 'Langata', 65],
        ['SALAMA', 2, -1.8667, 37.2000, 'Makueni', 'Kilome', 40],
        ['KANGUNDO', 1, -1.3000, 37.3500, 'Machakos', 'Kangundo', 85],
        ['KOLA', 1, -1.6167, 37.3167, 'Machakos', 'Machakos Town', 30]
    ]
    cols = ['Area', 'Actual_Customers', 'lat', 'lon', 'County', 'Sub_County', 'Potential_Retailers']
    df = pd.DataFrame(geo_data, columns=cols)
    
    # 2. CALCULATION LOGIC
    df['Market_Capture_%'] = ((df['Actual_Customers'] / df['Potential_Retailers']) * 100).round(1)
    df['Remaining_Gap'] = df['Potential_Retailers'] - df['Actual_Customers']
    return df

df = get_analysis_data()

# 3. TOP LEVEL METRICS
st.sidebar.title("National Market Share")
avg_capture = df['Market_Capture_%'].mean()
st.sidebar.metric("Average Market Capture", f"{avg_capture:.1f}%")
st.sidebar.markdown("---")

total_pot = df['Potential_Retailers'].sum()
total_act = df['Actual_Customers'].sum()

m_col1, m_col2 = st.columns(2)
m_col1.metric("Current Customers", f"{total_act:,}", delta_color="normal")
m_col2.metric("Total Market Potential", f"{total_pot:,}", delta="Untapped Growth", delta_color="inverse")

# 4. ACTUAL VS POTENTIAL VISUALIZATION
st.subheader("Customer Capture vs Untapped Gap")
fig = px.bar(df.head(20), x='Area', y=['Actual_Customers', 'Remaining_Gap'], 
             title="Actual vs Untapped Potential (Top 20 Areas)",
             labels={'value': 'Count of Shops', 'variable': 'Type'},
             barmode='stack', color_discrete_sequence=['#2ecc71', '#e74c3c'])
st.plotly_chart(fig, use_container_width=True)

# 5. GAP ANALYSIS MAP
st.subheader("Spatial Market Penetration (Red = Opportunity)")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=pdk.ViewState(latitude=-1.30, longitude=37.10, zoom=8, pitch=40),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[255, 100, 0, 160]', # Orange
            get_radius='Remaining_Gap * 10', # Radius based on GAP size
            pickable=True,
        ),
        pdk.Layer(
            'ColumnLayer',
            data=df,
            get_position='[lon, lat]',
            get_elevation='Actual_Customers',
            elevation_scale=500,
            radius=2000,
            get_fill_color='[0, 255, 100, 200]', # Green actuals
            pickable=True,
        )
    ],
    tooltip={"text": "{Area}\nActual: {Actual_Customers}\nCapture Rate: {Market_Capture_%}%"}
))

# 6. DATA & DOWNLOAD
st.subheader("Area-Specific Analysis & Export")
st.dataframe(df.sort_values(by='Market_Capture_%', ascending=True), use_container_width=True)

st.download_button(
    label="Export Market Data for Google My Maps",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='kenya_market_gap_analysis.csv',
    mime='text/csv'
)
