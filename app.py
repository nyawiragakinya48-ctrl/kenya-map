import streamlit as st
import pandas as pd
import pydeck as pdk

# SET PAGE TO WIDE MODE
st.set_page_config(layout="wide", page_title="Kenya Retail Expansion")

st.title("🇰🇪 Kenya National Retail Expansion Analysis")
st.markdown("Route-based analysis of **942 Customers** vs National Market Potential.")

# 1. THE COMPLETE DATA & GEO-REFERENCE TABLE
# We hardcode these to ensure the map never loads as "Blank"
@st.cache_data
def load_and_map_data():
    data = {
        'Area': [
            'EASTLEIGH', 'NAIROBI CBD', 'THIKA', 'KAMITI RD', 'KITUI', 'MOMBASA RD', 'KAYOLE', 
            'RUIRU-JUJA', 'NAIROBI WEST', 'KADAMALA', 'UMOJA', 'RONGAI', 'UTAWALA', 'KASA-MWIKI', 
            'WANGIGE-LIMURU', 'GARISSA', 'MACHAKOS', 'PIPELINE', 'KILIMANI', 'KAWANGWARE', 
            'GITHURAI 45', 'MWINGI', 'NGONG', 'WOTE', 'KIBWEZI', 'KIAMBU', 'OLOITOKTOK', 
            'KANGUNDO RD', 'PARKLANDS', 'KIKUYU', 'MATUU', 'EMALI', 'NAMANGA', 'WAIYAKI WAY', 
            'KAJIADO', 'ISINYA', 'MAKINDU', 'KIBRA', 'JOGOO RD', 'SULTAN HAMUD', 'JOGOO ROAD', 
            'NUNGUNI', 'BISIL', 'TALA', 'KAREN', 'SALAMA', 'KANGUNDO', 'KOLA'
        ],
        'Actual_Customers': [
            81, 71, 45, 43, 43, 40, 37, 36, 34, 32, 31, 29, 27, 26, 26, 25, 23, 21, 20, 20, 
            17, 16, 15, 14, 14, 13, 12, 12, 12, 10, 10, 10, 8, 8, 7, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 1, 1
        ]
    }
    df = pd.DataFrame(data)

    # MAP COORDINATES, COUNTIES, AND ROUTES
    geo_ref = {
        # Format: Area: [Lat, Lon, County, Sub-County, Route, Potential_Total]
        'NAIROBI CBD': [-1.2833, 36.8233, 'Nairobi', 'Starehe', 'Hub', 1400],
        'EASTLEIGH': [-1.2741, 36.8485, 'Nairobi', 'Kamkunji', 'Thika Rd Route', 900],
        'THIKA': [-1.0333, 37.0692, 'Kiambu', 'Thika West', 'Thika Rd Route', 400],
        'MOMBASA RD': [-1.3340, 36.8625, 'Nairobi', 'Embakasi South', 'Mombasa Rd Route', 450],
        'KAYOLE': [-1.2673, 36.9314, 'Nairobi', 'Embakasi Central', 'Garissa Hwy', 350],
        'KITUI': [-1.3683, 37.9944, 'Kitui', 'Kitui Central', 'Garissa Hwy', 200],
        'MACHAKOS': [-1.5177, 37.2634, 'Machakos', 'Machakos Town', 'Garissa Hwy', 300],
        'GARISSA': [-0.4532, 39.6461, 'Garissa', 'Garissa Township', 'Garissa Hwy', 150],
        'RONGAI': [-1.3931, 36.7420, 'Kajiado', 'Kajiado North', 'South Route', 250],
        'PIPELINE': [-1.3144, 36.8981, 'Nairobi', 'Embakasi South', 'Mombasa Rd Route', 600],
        'KILIMANI': [-1.2913, 36.7880, 'Nairobi', 'Dagoretti North', 'Hub', 200],
        'KAREN': [-1.3200, 36.7020, 'Nairobi', 'Langata', 'South Route', 100],
        'WOTE': [-1.7808, 37.6258, 'Makueni', 'Makueni', 'Mombasa Rd Route', 120],
    }

    # Apply geographic info
    def apply_geo(area):
        info = geo_ref.get(area, [-1.28, 36.82, 'Regional', 'Other', 'Other', 100])
        return pd.Series(info)

    df[['lat', 'lon', 'County', 'Sub_County', 'Route', 'Potential_Shops']] = df['Area'].apply(apply_geo)
    
    # Calculate expansion rate columns
    df['Potential_General'] = (df['Potential_Shops'] * 0.5).astype(int)
    df['Potential_Beauty'] = (df['Potential_Shops'] * 0.3).astype(int)
    df['Potential_MiniMart'] = (df['Potential_Shops'] * 0.2).astype(int)
    df['Market_Gap'] = df['Potential_Shops'] - df['Actual_Customers']
    
    return df

df = load_and_map_data()

# 2. KEY METRICS DISPLAY
m1, m2, m3 = st.columns(3)
m1.metric("National Customers", f"{df['Actual_Customers'].sum():,}")
m2.metric("Total Market Gap", f"{df['Market_Gap'].sum():,}")
m3.metric("Growth Headroom", "High")

# 3. INTERACTIVE 3D MAP
st.subheader("Spatial Route Mapping (Red Towers = Existing Customers)")
# If the map is black, this logic ensures 'lat' and 'lon' are exactly what PyDeck needs.
view_state = pdk.ViewState(latitude=-1.30, longitude=37.20, zoom=7.5, pitch=45)

layer = pdk.Layer(
    'ColumnLayer',
    data=df,
    get_position='[lon, lat]',
    get_elevation='Actual_Customers',
    elevation_scale=500,
    radius=3000,
    get_fill_color=[231, 76, 60, 200], # Red pillars
    pickable=True,
    auto_highlight=True,
)

# Render Map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "Area: {Area}\nRoute: {Route}\nActual Customers: {Actual_Customers}\nExpansion Gap: {Market_Gap}"}
))

# 4. NATIONAL EXPANSION DATA TABLE (BY CHANNEL)
st.subheader("Route-Based Expansion Details")
channel_breakdown = df[['Route', 'Area', 'County', 'Actual_Customers', 'Potential_General', 'Potential_Beauty', 'Potential_MiniMart', 'Market_Gap']]
st.dataframe(channel_breakdown.sort_values(by='Market_Gap', ascending=False), use_container_width=True)

# 5. EXPORT FOR GOOGLE MY MAPS
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Data for Google My Maps", data=csv, file_name="national_route_expansion.csv", mime="text/csv")
