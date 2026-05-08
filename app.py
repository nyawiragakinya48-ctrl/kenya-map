import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Kenya National Highlight Map")

st.title("🗺️ National Expansion: Area Highlight Map")
st.markdown("Detailed breakdown of **942 Customers** across all regional trade routes.")

@st.cache_data
def get_final_mapped_data():
    # 1. ACTUAL CUSTOMER DATA (Transcribed from your image)
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

    # 2. THE GEOGRAPHIC LOOKUP (The fix: index by area name directly)
    geo_map = {
        'EASTLEIGH': [-1.2741, 36.8485, [255, 0, 0], 'Thika Rd Corridor', 'Nairobi'],
        'NAIROBI CBD': [-1.2833, 36.8233, [255, 0, 0], 'Internal Hub', 'Nairobi'],
        'THIKA': [-1.0333, 37.0692, [0, 100, 255], 'Thika Rd Corridor', 'Kiambu'],
        'KITUI': [-1.3683, 37.9944, [0, 200, 100], 'Garissa Highway', 'Kitui'],
        'MOMBASA RD': [-1.3340, 36.8625, [255, 165, 0], 'Mombasa Rd Route', 'Nairobi'],
        'KAYOLE': [-1.2673, 36.9314, [0, 200, 100], 'Garissa Highway', 'Nairobi'],
        'RUIRU-JUJA': [-1.1167, 36.9667, [0, 100, 255], 'Thika Rd Corridor', 'Kiambu'],
        'RONGAI': [-1.3931, 36.7420, [128, 0, 128], 'South Route', 'Kajiado'],
        'MACHAKOS': [-1.5177, 37.2634, [0, 200, 100], 'Garissa Highway', 'Machakos'],
        'GARISSA': [-0.4532, 39.6461, [0, 200, 100], 'Garissa Highway', 'Garissa'],
        'PIPELINE': [-1.3144, 36.8981, [255, 165, 0], 'Mombasa Rd Route', 'Nairobi'],
        'NGONG': [-1.3621, 36.6565, [128, 0, 128], 'South Route', 'Kajiado'],
        'WOTE': [-1.7808, 37.6258, [255, 165, 0], 'Mombasa Rd Route', 'Makueni'],
        'KIBWEZI': [-2.4167, 37.9667, [255, 165, 0], 'Mombasa Rd Route', 'Makueni'],
        'KAWANGWARE': [-1.2861, 36.7450, [100, 100, 100], 'Western Corridor', 'Nairobi'],
        'KIKUYU': [-1.2430, 36.6714, [100, 100, 100], 'Western Corridor', 'Kiambu'],
    }

    # FIX: Correct 'apply' logic for Pandas
    def apply_ref(area_name):
        # Default coords for areas not listed explicitly in geo_map
        info = geo_map.get(area_name, [-1.285, 36.821, [150, 150, 150], 'Internal Area', 'Nairobi'])
        return pd.Series(info)

    df[['lat', 'lon', 'route_color', 'route_name', 'county']] = df['Area'].apply(apply_ref)
    
    # 3. ANALYSIS HIGHLIGHTS
    df['Headroom'] = (df['Actual_Customers'] * 6.5).astype(int)
    return df

# Initialize Data
df = get_final_mapped_data()

# KPI Header
st.sidebar.title("National Market Share")
st.sidebar.metric("Verified Customers", f"{df['Actual_Customers'].sum()}")
st.sidebar.markdown("---")

# 3D MAP VISUALIZATION
st.subheader("Highlighted Geographic Inventory")

view_state = pdk.ViewState(latitude=-1.35, longitude=37.15, zoom=7.5, pitch=45)

# Glowing Ring Layer
glow = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='route_color',
    opacity=0.4,
    get_radius='Headroom * 25',
    pickable=True,
)

# Vertical Strength Layer
pillars = pdk.Layer(
    'ColumnLayer',
    data=df,
    get_position='[lon, lat]',
    get_elevation='Actual_Customers',
    elevation_scale=1200,
    radius=3000,
    get_fill_color='route_color',
    pickable=True,
    auto_highlight=True,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=view_state,
    layers=[glow, pillars],
    tooltip={"text": "Area: {Area}\nRoute: {route_name}\nCustomers: {Actual_Customers}\nEst. Market Potential: {Headroom}"}
))

# DETAILED AREA LIST
st.subheader("Full Highlight Inventory")
st.dataframe(df[['Area', 'county', 'route_name', 'Actual_Customers', 'Headroom']].sort_values(by='Actual_Customers', ascending=False), hide_index=True, use_container_width=True)

# EXPORT
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Data for Google My Maps", data=csv, file_name="nairobi_market_highlights.csv", mime="text/csv")
