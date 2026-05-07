import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen
from streamlit_folium import st_folium
import pandas as pd
import io

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Nairobi Market Segmentation")
st.title("📊 Nairobi GT: Customer Segmentation & Population Density")

# --- DATA WITH REGIONAL & CHANNEL ESTIMATES ---
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
    'Pop_Density': [
        25000, 12000, 9500, 15000, 450, 5200, 31000, 7800, 11000, 19000, 26000, 
        6200, 18000, 18000, 4200, 120, 600, 35000, 9500, 29000, 22000, 210, 
        4500, 85, 60, 8500, 45, 15000, 8500, 4200, 280, 90, 80, 8000, 110, 
        110, 75, 35000, 24000, 95, 24000, 110, 80, 400, 3500, 70, 400, 120
    ],
    'Lat': [-1.275, -1.285, -1.039, -1.185, -1.365, -1.346, -1.292, -1.144, -1.315, -1.250, -1.288, -1.393, -1.285, -1.238, -1.221, -0.456, -1.517, -1.312, -1.289, -1.274, -1.150, -0.933, -1.359, -1.780, -2.414, -1.171, -2.980, -1.276, -1.263, -1.246, -1.144, -2.080, -2.534, -1.265, -1.850, -1.670, -2.280, -1.312, -1.285, -2.020, -1.286, -1.748, -1.890, -1.282, -1.336, -2.020, -1.291, -1.580],
    'Lon': [36.848, 36.823, 37.090, 36.896, 37.994, 36.902, 36.897, 36.959, 36.828, 36.880, 36.892, 36.741, 36.995, 36.891, 36.702, 39.658, 37.262, 36.897, 36.791, 36.751, 36.930, 38.011, 36.657, 37.625, 37.950, 36.835, 37.500, 36.950, 36.804, 36.671, 37.535, 37.460, 36.786, 36.750, 36.780, 36.850, 37.830, 36.790, 36.878, 37.380, 36.879, 37.380, 36.790, 37.265, 36.702, 37.240, 37.346, 37.330]
}

df = pd.DataFrame(area_data)

# Channel Estimates Logic
# Assumption: In typical Nairobi GT, Dukas/Retail Wholesalers account for ~92%, Supermarkets ~8%
df['Dukas_Wholesale'] = (df['Count'] * 0.92).round().astype(int)
df['Supermarkets'] = df['Count'] - df['Dukas_Wholesale']

# Region Assignment
def assign_region(area):
    area = area.upper()
    if area in ['NAIROBI CBD', 'EASTLEIGH', 'PARKLANDS']: return 'CENTRAL'
    if area in ['THIKA', 'KAMITI RD', 'RUIRU-JUJA', 'GITHURAI 45', 'KIAMBU', 'KADAMALA']: return 'NORTH'
    if area in ['MOMBASA RD', 'RONGAI', 'MACHAKOS', 'WOTE', 'KIBWEZI', 'EMALI', 'NAMANGA', 'KAJIADO', 'ISINYA', 'MAKINDU', 'SULTAN HAMUD', 'NUNGUNI', 'BISIL', 'SALAMA']: return 'SOUTH'
    if area in ['KAYOLE', 'KITUI', 'UMOJA', 'UTAWALA', 'KASA-MWIKI', 'GARISSA', 'MWINGI', 'KANGUNDO RD', 'MATUU', 'OLOITOKTOK', 'TALA', 'KANGUNDO', 'KOLA', 'JOGOO RD', 'JOGOO ROAD', 'PIPELINE']: return 'EAST'
    if area in ['NAIROBI WEST', 'KILIMANI', 'KAWANGWARE', 'NGONG', 'WANGIGE-LIMURU', 'KIKUYU', 'WAIYAKI WAY', 'KIBRA', 'KAREN']: return 'WEST'
    return 'OTHER'

df['Region'] = df['Area'].apply(assign_region)

# --- SIDEBAR ---
st.sidebar.header("Strategy Dashboard")
show_table = st.sidebar.checkbox("Show Detailed Table", value=True)
selected_region = st.sidebar.multiselect("Filter Region", df['Region'].unique(), default=df['Region'].unique())
map_type = st.sidebar.radio("Display Mode", ["Individual Markers", "Heatmap (Density)"])

filtered_df = df[df['Region'].isin(selected_region)]

# Calculate Averages for the Sidebar
avg_dukas = filtered_df['Dukas_Wholesale'].mean()
avg_supers = filtered_df['Supermarkets'].mean()
avg_density = filtered_df['Pop_Density'].mean()

st.sidebar.write("---")
st.sidebar.markdown(f"**Region Averages:**")
st.sidebar.write(f"🏠 Dukas/Wholesalers: {avg_dukas:.1f}")
st.sidebar.write(f"🛒 Supermarkets: {avg_supers:.1f}")
st.sidebar.write(f"👥 Pop Density: {avg_density:,.0f} /km²")

# --- MAP LOGIC ---
m = folium.Map(location=[-1.286, 36.817], zoom_start=10, tiles='CartoDB Positron')
Fullscreen().add_to(m)

if map_type == "Heatmap (Density)":
    heat_data = [[row['Lat'], row['Lon'], row['Pop_Density']] for _, row in filtered_df.iterrows()]
    HeatMap(heat_data, radius=30, blur=20).add_to(m)
else:
    cluster = MarkerCluster().add_to(m)
    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="color:#2E4053; margin-bottom:5px;">{row['Area']}</h4>
            <span style="background-color:#EBF5FB; padding:2px 5px; border-radius:3px;">Region: {row['Region']}</span><br><br>
            <b>Total Customers:</b> {row['Count']}<br>
            <hr>
            <b>🛒 Supermarkets:</b> {row['Supermarkets']}<br>
            <b>🏠 Dukas/Wholesale:</b> {row['Dukas_Wholesale']}<br>
            <br>
            <b>👥 Pop Density:</b> {row['Pop_Density']:,} /km²
        </div>
        """
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['Area']}: {row['Count']} customers",
            icon=folium.Icon(color="red" if row['Count'] > 40 else "blue", icon="info-sign")
        ).add_to(cluster)

# --- LAYOUT DISPLAY ---
if show_table:
    col_map, col_data = st.columns([2.5, 1.2])
    with col_map:
        st_folium(m, width=900, height=700)
    with col_data:
        st.subheader("Region Analysis")
        st.dataframe(
            filtered_df[['Area', 'Count', 'Dukas_Wholesale', 'Supermarkets', 'Pop_Density']]
            .sort_values('Count', ascending=False),
            hide_index=True,
            height=650
        )
else:
    # Large Full-Screen Map
    st_folium(m, width=1350, height=800)

# --- DOWNLOAD ---
map_html = io.BytesIO()
m.save(map_html, close_file=False)
st.sidebar.download_button(
    label="📥 Download Map (HTML)",
    data=map_html.getvalue(),
    file_name="Nairobi_Retail_Map.html",
    mime="text/html"
)

st.info("Market Insight: Averages are calculated based on the 942 distinct customers distributed across the 5 Nairobi regions.")
