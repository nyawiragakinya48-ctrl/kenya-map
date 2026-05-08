import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Kenya National Retail Expansion")

st.title("📈 National Expansion & Potential Tracker")
st.markdown("Measuring **942 Actual Customers** against **National Retail Potential** by Area.")

@st.cache_data
def get_comprehensive_data():
    # 1. BASE DATA (ACTUAL CUSTOMERS)
    # [Area, Actual_Customers, Potential_Base_Multiplier]
    raw_list = [
        ['EASTLEIGH', 81, 15], ['NAIROBI CBD', 71, 20], ['THIKA', 45, 12], ['KAMITI RD', 43, 8], 
        ['KITUI', 43, 6], ['MOMBASA RD', 40, 10], ['KAYOLE', 37, 12], ['RUIRU-JUJA', 36, 10], 
        ['NAIROBI WEST', 34, 6], ['KADAMALA', 32, 5], ['UMOJA', 31, 10], ['RONGAI', 29, 10], 
        ['UTAWALA', 27, 7], ['KASA-MWIKI', 26, 7], ['WANGIGE-LIMURU', 26, 6], ['GARISSA', 25, 6], 
        ['MACHAKOS', 23, 8], ['PIPELINE', 21, 14], ['KILIMANI', 20, 5], ['KAWANGWARE', 20, 15], 
        ['GITHURAI 45', 17, 15], ['MWINGI', 16, 5], ['NGONG', 15, 8], ['WOTE', 14, 5], 
        ['KIBWEZI', 14, 4], ['KIAMBU', 13, 10], ['OLOITOKTOK', 12, 4], ['KANGUNDO RD', 12, 9], 
        ['PARKLANDS', 12, 5], ['KIKUYU', 10, 8], ['MATUU', 10, 4], ['EMALI', 10, 4], 
        ['NAMANGA', 8, 4], ['WAIYAKI WAY', 8, 8], ['KAJIADO', 7, 5], ['ISINYA', 7, 5], 
        ['MAKINDU', 7, 4], ['KIBRA', 6, 20], ['JOGOO RD', 6, 12], ['SULTAN HAMUD', 5, 4], 
        ['JOGOO ROAD', 5, 12], ['NUNGUNI', 4, 3], ['BISIL', 4, 3], ['TALA', 3, 5], 
        ['KAREN', 3, 4], ['SALAMA', 2, 3], ['KANGUNDO', 1, 5], ['KOLA', 1, 3]
    ]
    df = pd.DataFrame(raw_list, columns=['Area', 'Actual_Customers', 'Pot_Mult'])

    # 2. CALCULATION: POTENTIAL VS ACTUAL
    # We estimate potential as (Current * Multiplier) OR a minimum retail floor
    df['Potential_Customers'] = (df['Actual_Customers'] * df['Pot_Mult']).astype(int)
    # Add National Expansion Hubs with 0 actuals but high potential
    expansion_hubs = pd.DataFrame([
        ['MOMBASA CBD', 0, 0, 1800], ['NAKURU TOWN', 0, 0, 1100], ['KISUMU CBD', 0, 0, 950]
    ], columns=['Area', 'Actual_Customers', 'Pot_Mult', 'Potential_Customers'])
    
    df = pd.concat([df, expansion_hubs], ignore_index=True)
    df['Untapped_Gap'] = df['Potential_Customers'] - df['Actual_Customers']
    df['Market_Share_Percent'] = ((df['Actual_Customers'] / df['Potential_Customers']) * 100).round(1)

    # 3. GEOGRAPHIC MAPPING (Sub-County & Route)
    geo_lookup = {
        'NAIROBI CBD': [-1.283, 36.823, 'Nairobi', 'Starehe', [255, 100, 0]],
        'EASTLEIGH': [-1.274, 36.848, 'Nairobi', 'Kamkunji', [255, 100, 0]],
        'PIPELINE': [-1.314, 36.898, 'Nairobi', 'Embakasi South', [0, 120, 255]],
        'KAYOLE': [-1.267, 36.931, 'Nairobi', 'Embakasi Central', [0, 120, 255]],
        'KITUI': [-1.368, 37.994, 'Kitui', 'Kitui Central', [0, 255, 150]],
        'THIKA': [-1.033, 37.069, 'Kiambu', 'Thika West', [0, 120, 255]],
        'MOMBASA CBD': [-4.043, 39.668, 'Mombasa', 'Mvita', [255, 0, 150]]
    }

    def apply_geo(area):
        info = geo_lookup.get(area, [-1.28, 36.82, 'Kenya', 'Regional', [100, 100, 100]])
        return pd.Series(info)

    df[['lat', 'lon', 'County', 'Sub_County', 'Highlight_Color']] = df['Area'].apply(apply_geo)
    return df

df = get_comprehensive_data()

# SIDEBAR METRICS
st.sidebar.title("National Reach")
st.sidebar.metric("Total Customers", f"{df['Actual_Customers'].sum()}")
st.sidebar.metric("National Potential", f"{df['Potential_Customers'].sum():,}")
total_share = (df['Actual_Customers'].sum() / df['Potential_Customers'].sum() * 100)
st.sidebar.progress(total_share / 100)
st.sidebar.caption(f"Current Market Penetration: {total_share:.2f}%")

# VISUALIZATION
st.subheader("Sub-County Highlights: Actual Strength vs. Growth Gap")
st.markdown("_Bars represent Actual Strength. Colored Circles highlight Expansion Potential per Area._")

view_state = pdk.ViewState(latitude=-1.3, longitude=37.1, zoom=7.5, pitch=40)

# Potential Layer (Circles - Highlighting Area Potential)
potential_layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='Highlight_Color',
    opacity=0.3,
    get_radius='Potential_Customers * 25', 
    pickable=True,
)

# Actual Layer (Columns - Visualizing Current Presence)
actual_layer = pdk.Layer(
    'ColumnLayer',
    data=df,
    get_position='[lon, lat]',
    get_elevation='Actual_Customers',
    elevation_scale=1000,
    radius=2000,
    get_fill_color=[255, 255, 255, 220],
    pickable=True,
    auto_highlight=True,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v10',
    initial_view_state=view_state,
    layers=[potential_layer, actual_layer],
    tooltip={"text": "Area: {Area}\nActual: {Actual_Customers}\nPotential: {Potential_Customers}\nGap: {Untapped_Gap}"}
))

# ANALYSIS TABLE
st.subheader("Territory Inventory: Expansion readiness")
st.dataframe(df[['County', 'Sub_County', 'Area', 'Actual_Customers', 'Potential_Customers', 'Market_Share_Percent', 'Untapped_Gap']].sort_values(by='Untapped_Gap', ascending=False), use_container_width=True)

# EXPORT
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Download Data with Potential for Google Maps", data=csv, file_name="kenya_market_gap.csv", mime="text/csv")
