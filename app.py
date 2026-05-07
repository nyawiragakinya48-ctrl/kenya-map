import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
from streamlit_folium import st_folium
import pandas as pd
import io

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Nairobi Logistics Map (942)")
st.title("🚚 Nairobi GT: Route Tracker & Market Coverage")

# --- DATA TRANSCRIPTION (Exact tally: 942) ---
data = {
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

df = pd.DataFrame(data)

# Supply Routes (Defining paths from Hubs to Town Clusters)
routes = {
    "A104 North Route": ["NAIROBI CBD", "KAMITI RD", "KIAMBU", "THIKA", "RUIRU-JUJA"],
    "Mombasa Rd Route": ["NAIROBI CBD", "MOMBASA RD", "MACHAKOS", "SALAMA", "SULTAN HAMUD", "EMALI", "KIBWEZI"],
    "Eastern Corridor": ["EASTLEIGH", "KAYOLE", "KASA-MWIKI", "KANGUNDO RD", "TALA", "MATUU", "MWINGI", "GARISSA"],
    "Southern/Kajiado Route": ["NAIROBI WEST", "RONGAI", "KAJIADO", "ISINYA", "BISIL", "NAMANGA"]
}

# --- SIDEBAR OPTIONS ---
st.sidebar.header("Map Controls")
show_routes = st.sidebar.toggle("Show Logistics Routes", value=True)
show_fill = st.sidebar.toggle("Show Market Coverage (Fill)", value=True)
min_shops = st.sidebar.slider("Filter by Min. Customers", 1, 81, 1)

# Filter Data
filtered_df = df[df['Count'] >= min_shops]

# --- MAP INITIALIZATION ---
m = folium.Map(location=[-1.286, 36.817], zoom_start=9, tiles='CartoDB Positron')
Fullscreen().add_to(m)

# 1. Fill Coverage (Market Reach Circles)
if show_fill:
    for idx, row in df.iterrows():
        # Color based on count density
        color = '#ff4b4b' if row['Count'] > 40 else '#1f77b4'
        folium.Circle(
            location=[row['Lat'], row['Lon']],
            radius=row['Count'] * 150, # Size relative to customer count
            color=color,
            fill=True,
            fill_opacity=0.2,
            popup=f"{row['Area']}: Market Coverage Area"
        ).add_to(m)

# 2. Logistics Routes (Tracing Supply Paths)
if show_routes:
    route_colors = {"A104 North Route": "blue", "Mombasa Rd Route": "green", "Eastern Corridor": "red", "Southern/Kajiado Route": "purple"}
    for route_name, locations in routes.items():
        path = []
        for loc in locations:
            coords = df[df['Area'] == loc][['Lat', 'Lon']].values
            if len(coords) > 0:
                path.append(coords[0].tolist())
        
        folium.PolyLine(path, color=route_colors[route_name], weight=4, opacity=0.7, tooltip=route_name).add_to(m)

# 3. Markers
marker_cluster = MarkerCluster().add_to(m)
for idx, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        tooltip=f"{row['Area']}: {row['Count']} Shops",
        popup=f"<b>{row['Area']}</b><br>Distinct Customers: {row['Count']}",
        icon=folium.Icon(color="red" if row['Count'] > 40 else "blue", icon="truck", prefix='fa')
    ).add_to(marker_cluster)

# --- DISPLAY & DOWNLOAD ---
col1, col2 = st.columns([3, 1])

with col1:
    st_folium(m, width=950, height=600)

with col2:
    st.write(f"### Regional Stats")
    st.metric("Total Customers", df['Count'].sum())
    st.metric("Top Area", f"{df.iloc[0]['Area']} ({df.iloc[0]['Count']})")
    
    # Download Map Button
    map_html = io.BytesIO()
    m.save(map_html, close_file=False)
    st.download_button(
        label="📥 Download Interactive Map (HTML)",
        data=map_html.getvalue(),
        file_name="Nairobi_Logistics_Map.html",
        mime="text/html"
    )

    st.write("---")
    st.dataframe(filtered_df[['Area', 'Count']].sort_values(by="Count", ascending=False), height=300)

st.success("The map tracks supply routes from central hubs to satellite markets. Red circles indicate high-density market clusters.")
