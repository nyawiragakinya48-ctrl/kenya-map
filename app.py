import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
from streamlit_folium import st_folium
import pandas as pd
import io

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Nairobi GT Regional Strategy")
st.title("🗺️ Nairobi GT Region: 942 Customer Logistics Map")

# --- DATA WITH REGIONAL SEGMENTATION ---
area_data = {
    'Area': [
        'EASTLEIGH', 'NAIROBI CBD', 'THIKA', 'KAMITI RD', 'KITUI', 'MOMBASA RD', 
        'KAYOLE', 'RUIRU-JUJA', 'NAIROBI WEST', 'KADAMALA', 'UMOJA', 'RONGAI', 
        'UTAWALA', 'KASA-MWIKI', 'WANGIGE-LIMURU', 'GARISSA', 'MACHAKOS', 
        'PIPELINE', 'KILIMANI', 'KAWANGWARE', 'GITHURAI 45', 'MWINGI', 'NGONG', 
        'WOTE', 'KIBWEZI', 'KIAMBU', 'OLOITOKTOK', 'KANGUNDO RD', 'PARKLANDS', 
        'KIKUYU', 'MATUU', 'EMALI', 'NAMANGA', 'WAIYAKI WAY', 'KAJIADO', 
        'ISINYA', 'MAKINDU', 'KIBRA', 'JOGOO RD', 'SULTAN HAMUD', 'JOGOO ROAD', 
        'NUNGUNI', 'BISIL', 'TALA', 'KAREN', 'SALAMA', 'KANGUNDO', 'KOLA'
    ],
    'Count': [
        81, 71, 45, 43, 43, 40, 37, 36, 34, 32, 31, 29, 27, 26, 26, 25, 23, 21, 
        20, 20, 17, 16, 15, 14, 14, 13, 12, 12, 12, 10, 10, 10, 8, 8, 7, 7, 7, 
        6, 6, 5, 5, 4, 4, 3, 3, 2, 1, 1
    ],
    'Lat': [-1.275, -1.285, -1.039, -1.185, -1.365, -1.346, -1.292, -1.144, -1.315, -1.250, -1.288, -1.393, -1.285, -1.238, -1.221, -0.456, -1.517, -1.312, -1.289, -1.274, -1.150, -0.933, -1.359, -1.780, -2.414, -1.171, -2.980, -1.276, -1.263, -1.246, -1.144, -2.080, -2.534, -1.265, -1.850, -1.670, -2.280, -1.312, -1.285, -2.020, -1.286, -1.748, -1.890, -1.282, -1.336, -2.020, -1.291, -1.580],
    'Lon': [36.848, 36.823, 37.090, 36.896, 37.994, 36.902, 36.897, 36.959, 36.828, 36.880, 36.892, 36.741, 36.995, 36.891, 36.702, 39.658, 37.262, 36.897, 36.791, 36.751, 36.930, 38.011, 36.657, 37.625, 37.950, 36.835, 37.500, 36.950, 36.804, 36.671, 37.535, 37.460, 36.786, 36.750, 36.780, 36.850, 37.830, 36.790, 36.878, 37.380, 36.879, 37.380, 36.790, 37.265, 36.702, 37.240, 37.346, 37.330]
}

df = pd.DataFrame(area_data)

# Regional Logic
def assign_region(area):
    area = area.upper()
    if area in ['NAIROBI CBD', 'EASTLEIGH', 'PARKLANDS']: return 'CENTRAL'
    if area in ['THIKA', 'KAMITI RD', 'RUIRU-JUJA', 'GITHURAI 45', 'KIAMBU', 'KADAMALA']: return 'NORTH'
    if area in ['MOMBASA RD', 'RONGAI', 'MACHAKOS', 'WOTE', 'KIBWEZI', 'EMALI', 'NAMANGA', 'KAJIADO', 'ISINYA', 'MAKINDU', 'SULTAN HAMUD', 'NUNGUNI', 'BISIL', 'SALAMA']: return 'SOUTH'
    if area in ['KAYOLE', 'KITUI', 'UMOJA', 'UTAWALA', 'KASA-MWIKI', 'GARISSA', 'MWINGI', 'KANGUNDO RD', 'MATUU', 'OLOITOKTOK', 'TALA', 'KANGUNDO', 'KOLA', 'JOGOO RD', 'JOGOO ROAD', 'PIPELINE']: return 'EAST'
    if area in ['NAIROBI WEST', 'KILIMANI', 'KAWANGWARE', 'NGONG', 'WANGIGE-LIMURU', 'KIKUYU', 'WAIYAKI WAY', 'KIBRA', 'KAREN']: return 'WEST'
    return 'OTHER'

df['Region'] = df['Area'].apply(assign_region)

# Route Definitions (Hub to Cluster)
routes = {
    "Northern Logistics Path": ["NAIROBI CBD", "KAMITI RD", "KIAMBU", "THIKA", "RUIRU-JUJA"],
    "South-Mombasa Corridor": ["NAIROBI CBD", "MOMBASA RD", "MACHAKOS", "SALAMA", "EMALI", "KIBWEZI"],
    "Eastern Supply Line": ["EASTLEIGH", "KAYOLE", "KANGUNDO RD", "TALA", "MATUU", "MWINGI", "GARISSA"],
    "Western Market Route": ["NAIROBI WEST", "KILIMANI", "KIKUYU", "WAIYAKI WAY", "NGONG"]
}

# --- SIDEBAR & INTERACTIVITY ---
st.sidebar.header("Global Controls")
view_type = st.sidebar.selectbox("Map View", ["Regional Clusters", "Density Heatmap"])
show_table = st.sidebar.checkbox("Show Data Table", value=True)
show_routes = st.sidebar.checkbox("Show Logistics Routes", value=True)
selected_region = st.sidebar.multiselect("Filter by Region", ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"], default=["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"])

# Filter Logic
filtered_df = df[df['Region'].isin(selected_region)]

# --- MAP GENERATION ---
m = folium.Map(location=[-1.286, 36.817], zoom_start=9, tiles='CartoDB Positron')
Fullscreen().add_to(m)

# 1. Market Reach Fill (The "Fill")
for _, row in filtered_df.iterrows():
    color_map = {'NORTH': 'blue', 'SOUTH': 'green', 'EAST': 'red', 'WEST': 'purple', 'CENTRAL': 'orange'}
    folium.Circle(
        location=[row['Lat'], row['Lon']],
        radius=row['Count'] * 150,
        color=color_map.get(row['Region'], 'gray'),
        fill=True,
        fill_opacity=0.2,
        popup=f"{row['Area']} (Region: {row['Region']})"
    ).add_to(m)

# 2. Logistics Route Overlay
if show_routes:
    route_colors = {"Northern Logistics Path": "blue", "South-Mombasa Corridor": "darkgreen", "Eastern Supply Line": "red", "Western Market Route": "purple"}
    for r_name, points in routes.items():
        path = [[df[df['Area'] == p]['Lat'].values[0], df[df['Area'] == p]['Lon'].values[0]] for p in points if p in df['Area'].values]
        if path:
            folium.PolyLine(path, color=route_colors.get(r_name, 'black'), weight=3, opacity=0.6, tooltip=r_name).add_to(m)

# 3. Markers / Heatmap
if view_type == "Density Heatmap":
    heat_data = [[row['Lat'], row['Lon'], row['Count']] for _, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=25, blur=15).add_to(m)
else:
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['Area']}</b><br>Region: {row['Region']}<br>Customers: {row['Count']}",
            icon=folium.Icon(color="red" if row['Count'] > 40 else "blue", icon="shopping-cart", prefix='fa')
        ).add_to(marker_cluster)

# --- PAGE LAYOUT ---
if show_table:
    col_m, col_t = st.columns([3, 1.2])
    with col_m:
        st_folium(m, width=950, height=700)
    with col_t:
        st.subheader("Regional Tally")
        region_stats = filtered_df.groupby('Region')['Count'].sum().reset_index()
        st.dataframe(region_stats, hide_index=True)
        st.write("---")
        st.dataframe(filtered_df[['Area', 'Count', 'Region']].sort_values(by='Count', ascending=False), height=450)
else:
    # Full Width Map
    st_folium(m, width=1350, height=800)

# --- DOWNLOAD BUTTON ---
st.sidebar.write("---")
map_html = io.BytesIO()
m.save(map_html, close_file=False)
st.sidebar.download_button(
    label="📥 Download Map (HTML)",
    data=map_html.getvalue(),
    file_name="Nairobi_Strategy_Map.html",
    mime="text/html"
)

st.sidebar.info(f"Total Visible Customers: {filtered_df['Count'].sum()}")
