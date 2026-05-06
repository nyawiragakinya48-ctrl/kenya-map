
import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import pandas as pd

# 1. SETUP DATA
st.set_page_config(layout="wide", page_title="Kenya Customer Strategy Map")
st.title("📍 Interactive Customer Density Map - Kenya")

# Data from your list (Top clusters)
data = {
    'Area': ['Eastleigh', 'CBD/OTC', 'Kitui', 'Thika', 'Kayole', 'Kahawa West', 'Rongai', 'Machakos', 'Mombasa Rd', 'Mwiki', 'Garissa', 'Githurai 45', 'Matuu', 'Oloitoktok', 'Limuru', 'Kasarani', 'Umoja', 'Isinya', 'Wote', 'Emali'],
    'Count': [70, 44, 38, 35, 27, 24, 23, 21, 20, 19, 18, 15, 10, 12, 22, 19, 18, 5, 10, 8],
    'Lat': [-1.276, -1.285, -1.365, -1.039, -1.292, -1.185, -1.393, -1.517, -1.346, -1.238, -0.456, -1.150, -1.144, -2.980, -1.107, -1.218, -1.298, -1.670, -1.780, -2.080],
    'Lon': [36.850, 36.823, 37.994, 37.090, 36.897, 36.896, 36.741, 37.262, 36.902, 36.891, 39.658, 36.930, 37.535, 37.500, 36.640, 36.895, 36.868, 36.850, 37.625, 37.460]
}
df = pd.DataFrame(data)

# 2. SIDEBAR KEY (The "Key" to change the map)
st.sidebar.header("Map Controls")
map_type = st.sidebar.radio("Select View:", ["Heat Map (Density)", "Marker Cluster (Customer Count)"])
show_table = st.sidebar.checkbox("Show Data Table", value=True)

# 3. BUILD THE MAP
m = folium.Map(location=[-1.286, 36.817], zoom_start=8)

if map_type == "Heat Map (Density)":
    heat_data = [[row['Lat'], row['Lon'], row['Count']] for index, row in df.iterrows()]
    HeatMap(heat_data, radius=25, blur=15).add_to(m)
else:
    marker_cluster = MarkerCluster().add_to(m)
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['Area']}</b><br>Customers: {row['Count']}",
            tooltip=row['Area'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

# 4. DISPLAY
st_folium(m, width=1200, height=600)

if show_table:
    st.subheader("Customer Counts per Area")
    st.dataframe(df.sort_values(by='Count', ascending=False), use_container_width=True)

st.info("Edit the 'data' dictionary in the code to add more customers instantly.")
