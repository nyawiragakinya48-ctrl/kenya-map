import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Nairobi GT 942 Map")
st.title("📍 Nairobi GT Region: 942 Customer Strategy Map")

# --- DATA LOADING & PROCESSING ---
# Updated with exact data from the provided image tally
area_data = {
    'Area': [
        'EASTLEIGH', 'NAIROBI CBD', 'THIKA', 'KAMITI RD', 'KITUI', 
        'MOMBASA RD', 'KAYOLE', 'RUIRU-JUJA', 'NAIROBI WEST', 'KADAMALA', 
        'UMOJA', 'RONGAI', 'UTAWALA', 'KASA-MWIKI', 'WANGIGE-LIMURU', 
        'GARISSA', 'MACHAKOS', 'PIPELINE', 'KILIMANI', 'KAWANGWARE', 
        'GITHURAI 45', 'MWINGI', 'NGONG', 'WOTE', 'KIBWEZI', 
        'KIAMBU', 'OLOITOKTOK', 'KANGUNDO RD', 'PARKLANDS', 'KIKUYU', 
        'MATUU', 'EMALI', 'NAMANGA', 'WAIYAKI WAY', 'KAJIADO', 
        'ISINYA', 'MAKINDU', 'KIBRA', 'JOGOO RD', 'SULTAN HAMUD', 
        'JOGOO ROAD', 'NUNGUNI', 'BISIL', 'TALA', 'KAREN', 
        'SALAMA', 'KANGUNDO', 'KOLA'
    ],
    'Count': [
        81, 71, 45, 43, 43, 
        40, 37, 36, 34, 32, 
        31, 29, 27, 26, 26, 
        25, 23, 21, 20, 20, 
        17, 16, 15, 14, 14, 
        13, 12, 12, 12, 10, 
        10, 10, 8, 8, 7, 
        7, 7, 6, 6, 5, 
        5, 4, 4, 3, 3, 
        2, 1, 1
    ],
    # Approximate Lat/Lon coordinates for mapping
    'Lat': [
        -1.275, -1.285, -1.039, -1.185, -1.365, 
        -1.346, -1.292, -1.144, -1.315, -1.250, 
        -1.288, -1.393, -1.285, -1.238, -1.221, 
        -0.456, -1.517, -1.312, -1.289, -1.274, 
        -1.150, -0.933, -1.359, -1.780, -2.414, 
        -1.171, -2.980, -1.276, -1.263, -1.246, 
        -1.144, -2.080, -2.534, -1.265, -1.850, 
        -1.670, -2.280, -1.312, -1.285, -2.020, 
        -1.286, -1.748, -1.890, -1.282, -1.336, 
        -2.020, -1.291, -1.580
    ],
    'Lon': [
        36.848, 36.823, 37.090, 36.896, 37.994, 
        36.902, 36.897, 36.959, 36.828, 36.880, 
        36.892, 36.741, 36.995, 36.891, 36.702, 
        39.658, 37.262, 36.897, 36.791, 36.751, 
        36.930, 38.011, 36.657, 37.625, 37.950, 
        36.835, 37.500, 36.950, 36.804, 36.671, 
        37.535, 37.460, 36.786, 36.750, 36.780, 
        36.850, 37.830, 36.790, 36.878, 37.380, 
        36.879, 37.380, 36.790, 37.265, 36.702, 
        37.240, 37.346, 37.330
    ],
    'Pop_Density': [
        25000, 12000, 9500, 15000, 450, 
        5200, 31000, 7800, 11000, 19000, 
        26000, 6200, 18000, 18000, 4200, 
        120, 600, 35000, 9500, 29000, 
        22000, 210, 4500, 85, 60, 
        8500, 45, 15000, 8500, 4200, 
        280, 90, 80, 8000, 110, 
        110, 75, 35000, 24000, 95, 
        24000, 110, 80, 400, 3500, 
        70, 400, 120
    ]
}

df = pd.DataFrame(area_data)

# --- VERIFICATION STEP ---
total_customers = df['Count'].sum()

# Likelihood estimation based on Area Type
def estimate_channels(row):
    if row['Count'] >= 40 or row['Area'] in ['EASTLEIGH', 'NAIROBI CBD']:
        return "High (Distribution Hub)"
    elif row['Pop_Density'] > 15000:
        return "Retail Heavy (Dukas & Small Shops)"
    else:
        return "Mixed (Retail & Local Wholesale)"

df['Likelihood'] = df.apply(estimate_channels, axis=1)

# --- SIDEBAR & FILTERING ---
st.sidebar.title("Strategy & Stats")
view = st.sidebar.radio("Map View:", ["Customer Density (Heatmap)", "Specific Shop Counts (Markers)"])

st.sidebar.markdown(f"### Total Customer Tally: **{total_customers}**")
if total_customers == 942:
    st.sidebar.success("✅ Perfectly Matches Excel Tally")
else:
    st.sidebar.warning(f"Note: Current Tally is {total_customers}.")

# Area Selection for Auto-Zoom
selected_area = st.sidebar.selectbox("Jump to Area:", ["All Areas"] + list(df['Area']))

# --- MAP LOGIC ---
# Centering map on Nairobi
map_center = [-1.286, 36.817]
if selected_area != "All Areas":
    row = df[df['Area'] == selected_area].iloc[0]
    map_center = [row['Lat'], row['Lon']]
    zoom = 13
else:
    zoom = 9

m = folium.Map(location=map_center, zoom_start=zoom, tiles='CartoDB Positron')

if view == "Customer Density (Heatmap)":
    heat_data = [[row['Lat'], row['Lon'], row['Count']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=25, blur=15).add_to(m)
else:
    marker_cluster = MarkerCluster().add_to(m)
    for index, row in df.iterrows():
        html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color:navy; margin-bottom:5px;">{row['Area']}</h4>
            <hr style="margin:5px 0;">
            <b>Distinct Customers:</b> {row['Count']}<br>
            <b>Est. Pop Density:</b> {row['Pop_Density']:,} km²<br>
            <b>Strategy Segment:</b><br>{row['Likelihood']}
        </div>
        """
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=folium.Popup(html, max_width=250),
            tooltip=f"{row['Area']}: {row['Count']} customers",
            icon=folium.Icon(color='red' if row['Count'] >= 40 else 'blue', icon='shopping-cart', prefix='fa')
        ).add_to(marker_cluster)

# --- DISPLAY ---
col1, col2 = st.columns([3, 1.2])

with col1:
    st_folium(m, width=900, height=650)

with col2:
    st.subheader("Data Tally Table")
    st.dataframe(
        df[['Area', 'Count', 'Likelihood']].sort_values(by='Count', ascending=False), 
        hide_index=True,
        height=600
    )

st.info("Market Intel: Red markers denote High-Priority regions with 40+ distinct customers, typically acting as regional distribution hubs.")
