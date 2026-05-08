import streamlit as st
import pandas as pd
import pydeck as pdk

# Configure Streamlit page
st.set_page_config(layout="wide", page_title="Kenya Retail Hub Mapping")

st.title("🗺️ National Expansion: Area Highlight Map")
st.markdown("Detailed breakdown of **942 Customers** across all regional trade routes.")

# 1. THE COMPLETE GEOGRAPHIC & DATASET REFERENCE
@st.cache_data
def get_final_mapped_data():
    # Area, Customers
    base_data = [
        ['EASTLEIGH', 81], ['NAIROBI CBD', 71], ['THIKA', 45], ['KAMITI RD', 43], 
        ['KITUI', 43], ['MOMBASA RD', 40], ['KAYOLE', 37], ['RUIRU-JUJA', 36], 
        ['NAIROBI WEST', 34], ['KADAMALA', 32], ['UMOJA', 31], ['RONGAI', 29], 
        ['UTAWALA', 27], ['KASA-MWIKI', 26], ['WANGIGE-LIMURU', 26], ['GARISSA', 25], 
        ['MACHAKOS', 23], ['PIPELINE', 21], ['KILIMANI', 20], ['KAWANGWARE', 20], 
        ['GITHURAI 45', 17], ['MWINGI', 16], ['NGONG', 15], ['WOTE', 14], 
        ['KIBWEZI', 14], ['KIAMBU', 13], ['OLOITOKTOK', 12], ['KANGUNDO RD', 12], 
        ['PARKLANDS', 12], ['KIKUYU', 10], ['MATUU', 10], ['EMALI', 10], 
        ['NAMANGA', 8], ['WAIYAKI WAY', 8], ['KAJIADO', 7], ['ISINYA', 7], 
        ['MAKINDU', 7], ['KIBRA', 6], ['JOGOO RD', 6], ['SULTAN HAMUD', 5], 
        ['JOGOO ROAD', 5], ['NUNGUNI', 4], ['BISIL', 4], ['TALA', 3], 
        ['KAREN', 3], ['SALAMA', 2], ['KANGUNDO', 1], ['KOLA', 1]
    ]
    df = pd.DataFrame(base_data, columns=['Area', 'Actual_Customers'])

    # COORDINATE AND ROUTE TABLE (Highlights)
    geo_map = {
        # Area: [lat, lon, Route_Color, Route_Name, County, Sub_County]
        'EASTLEIGH': [-1.2741, 36.8485, [255, 0, 0], 'Thika Rd Corridor', 'Nairobi', 'Kamkunji'],
        'NAIROBI CBD': [-1.2833, 36.8233, [255, 0, 0], 'Internal Hub', 'Nairobi', 'Starehe'],
        'THIKA': [-1.0333, 37.0692, [0, 100, 255], 'Thika Rd Corridor', 'Kiambu', 'Thika West'],
        'KAMITI RD': [-1.2050, 36.8900, [0, 100, 255], 'Thika Rd Corridor', 'Nairobi', 'Roysambu'],
        'KITUI': [-1.3683, 37.9944, [0, 200, 100], 'Eastern Corridor', 'Kitui', 'Kitui Central'],
        'MOMBASA RD': [-1.3340, 36.8625, [255, 165, 0], 'Mombasa Rd Route', 'Nairobi', 'Embakasi South'],
        'KAYOLE': [-1.2673, 36.9314, [0, 200, 100], 'Eastern Corridor', 'Nairobi', 'Embakasi Central'],
        'MACHAKOS': [-1.5177, 37.2634, [0, 200, 100], 'Eastern Corridor', 'Machakos', 'Machakos Town'],
        'GARISSA': [-0.4532, 39.6461, [0, 200, 100], 'Eastern Corridor', 'Garissa', 'Garissa Township'],
        'RONGAI': [-1.3931, 36.7420, [128, 0, 128], 'South Route', 'Kajiado', 'Kajiado North'],
        'WOTE': [-1.7808, 37.6258, [255, 165, 0], 'Mombasa Rd Route', 'Makueni', 'Makueni'],
        'PIPELINE': [-1.3144, 36.8981, [255, 165, 0], 'Mombasa Rd Route', 'Nairobi', 'Embakasi South'],
        'KIBWEZI': [-2.4167, 37.9667, [255, 165, 0], 'Mombasa Rd Route', 'Makueni', 'Kibwezi East'],
    }

    def apply_ref(row):
        # Default for any areas not specifically mapped (General Nairobi coordinates)
        info = geo_map.get(row['Area'], [-1.285, 36.821, [150, 150, 150], 'Nairobi Central', 'Nairobi', 'Internal'])
        return pd.Series(info)

    df[['lat', 'lon', 'route_color', 'route_name', 'county', 'sub_county']] = df['Area'].apply(apply_ref)
    
    # Calculate Channels & Potential (Simulation for highlighting growth)
    df['Potential_General'] = (df['Actual_Customers'] * 5).astype(int)
    df['Potential_Beauty'] = (df['Actual_Customers'] * 3).astype(int)
    df['Potential_MiniMart'] = (df['Actual_Customers'] * 2).astype(int)
    df['Growth_Headroom'] = df['Potential_General'] + df['Potential_Beauty']
    
    return df

df = get_final_mapped_data()

# 2. KEY PERFORMANCE INDICATORS
c1, c2, c3 = st.columns(3)
c1.metric("National Customers", df['Actual_Customers'].sum())
c2.metric("Market Areas Mapped", len(df))
c3.metric("Largest Hub", "Eastleigh / CBD")

# 3. 3D MAP VISUALIZATION WITH HIGHLIGHTS
st.subheader("Highlighted Customer Reach & Potential")

view_state = pdk.ViewState(latitude=-1.3, longitude=37.2, zoom=7, pitch=45)

# Layer 1: The Highlight Halo (Glow ring around every area showing potential)
potential_layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='route_color',
    opacity=0.3,
    get_radius='Growth_Headroom * 30',
    pickable=True,
)

# Layer 2: The Core Hub Tower (The Height of existing business)
actual_layer = pdk.Layer(
    'ColumnLayer',
    data=df,
    get_position='[lon, lat]',
    get_elevation='Actual_Customers',
    elevation_scale=1000,
    radius=3500,
    get_fill_color='route_color',
    pickable=True,
    auto_highlight=True,
)

# Render Map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[potential_layer, actual_layer],
    tooltip={
        "html": "<b>Area:</b> {Area}<br/><b>County:</b> {county}<br/><b>Customers:</b> {Actual_Customers}<br/><b>Headroom:</b> {Growth_Headroom}",
        "style": {"color": "white"}
    }
))

# 4. REGIONAL DATA BREAKDOWN
st.subheader("Route & Channel Inventory")
tabs = st.tabs(["Strategic Table", "Channel Forecast", "Export for Google Maps"])

with tabs[0]:
    st.dataframe(df[['Area', 'county', 'sub_county', 'route_name', 'Actual_Customers']].sort_values('Actual_Customers', ascending=False), use_container_width=True)

with tabs[1]:
    st.write("National Retail Breakdown (Potential Outlets):")
    st.dataframe(df[['Area', 'Potential_General', 'Potential_Beauty', 'Potential_MiniMart']], use_container_width=True)

with tabs[2]:
    st.info("Download this file and upload it to Google My Maps for field sales tracking.")
    csv_file = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download National Highlight Data", data=csv_file, file_name="kenya_highlight_analysis.csv", mime="text/csv")
