import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, Fullscreen
from streamlit_folium import st_folium
import io

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Kenya GT Retail Mapper")
st.title("🇰🇪 Kenya Customer Strategy Map")
st.markdown("### National Distribution: Retailers, Wholesalers & Supermarkets")

# --- DATA LOADING ---
@st.cache_data
def load_customer_data():
    # Attempt to load your enriched CSV
    try:
        df = pd.read_csv('customers_with_counties.csv')
    except:
        # Fallback if file isn't ready yet (for testing)
        st.warning("Processed CSV not found. Please ensure 'customers_with_counties.csv' is in your folder.")
        return pd.DataFrame()
    
    # Combined General Trade (GT) Potential Calculation (Placeholder Logic)
    # In a real scenario, this would come from your census data
    df['Pot_GT'] = (df['@lat'].abs() * 50).round().astype(int) 
    df['Pot_Supermarket'] = (df['Pot_GT'] * 0.05).round().astype(int)
    return df

df = load_customer_data()

if df.empty:
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("📍 Search & Filter")

# 1. SEARCH BY AREA/SHOP NAME
all_names = sorted(df['name'].unique())
search_shop = st.sidebar.selectbox("🎯 Search Shop or Area:", ["Global View"] + all_names)

st.sidebar.write("---")

# 2. HIERARCHY FILTERS
selected_region = st.sidebar.multiselect("Region:", df['Region'].unique(), default=df['Region'].unique())
available_counties = df[df['Region'].isin(selected_region)]['County'].unique()
selected_county = st.sidebar.multiselect("County:", available_counties, default=available_counties[:5] if len(available_counties)>5 else available_counties)

# Apply Filters
mask = (df['Region'].isin(selected_region)) & (df['County'].isin(selected_county))
filtered_df = df[mask]

# --- METRICS ---
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Total Customers Found", f"{len(filtered_df)}")
with col_b:
    st.metric("Active Regions", f"{filtered_df['Region'].nunique()}")
with col_c:
    st.metric("Market Potential (GT)", f"{filtered_df['Pot_GT'].sum():,}")

# --- MAP LOGIC ---
# Default center: Nairobi
map_center = [-1.286, 36.817]
zoom_level = 7

if search_shop != "Global View":
    s_row = df[df['name'] == search_shop].iloc[0]
    map_center = [s_row['@lat'], s_row['@lon']]
    zoom_level = 15

m = folium.Map(location=map_center, zoom_start=zoom_level, tiles='CartoDB Positron')
Fullscreen().add_to(m)

cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    is_target = (row['name'] == search_shop)
    
    popup_html = f"""
    <div style="font-family: Arial; width: 220px;">
        <h4 style="color:#1A5276; margin:0;">{row['name']}</h4>
        <hr style="margin:8px 0;">
        <b>County:</b> {row['County']}<br>
        <b>Sub-County:</b> {row['Sub_County']}<br>
        <br>
        <b>Market Potential:</b><br>
        🏠 General Trade: {row['Pot_GT']}<br>
        🛒 Supermarkets: {row['Pot_Supermarket']}
    </div>
    """
    
    folium.Marker(
        location=[row['@lat'], row['@lon']],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{row['name']} ({row['County']})",
        icon=folium.Icon(color="red" if is_target else "blue", 
                         icon="star" if is_target else "shopping-cart", prefix="fa")
    ).add_to(cluster)

# --- DISPLAY ---
show_table = st.sidebar.checkbox("Show Data Analysis Table", value=True)

if show_table:
    m_col, t_col = st.columns([2.5, 1.2])
    with m_col:
        st_folium(m, width=900, height=700, key="main_map")
    with t_col:
        st.subheader("Regional Breakdown")
        summary = filtered_df.groupby(['Region', 'County']).size().reset_index(name='Customer Count')
        st.dataframe(summary, hide_index=True, height=650)
else:
    st_folium(m, width=1350, height=800, key="full_map")

# --- EXPORT ---
st.sidebar.write("---")
map_html = io.BytesIO()
m.save(map_html, close_file=False)
st.sidebar.download_button(
    label="📥 Download Map (HTML)",
    data=map_html.getvalue(),
    file_name="Kenya_Market_Report.html",
    mime="text/html"
)
