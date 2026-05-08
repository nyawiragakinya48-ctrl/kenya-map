import pandas as pd

# 1. Dataset with Channel potential and Logistic Route Mapping
# Potential counts are estimates based on regional trade density
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
    'Customers': [
        81, 71, 45, 43, 43, 40, 37, 36, 34, 32, 31, 29, 27, 26, 26, 25, 23, 21, 20, 20, 
        17, 16, 15, 14, 14, 13, 12, 12, 12, 10, 10, 10, 8, 8, 7, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 1, 1
    ]
}

df = pd.DataFrame(data)

# 2. Reference Table with Routes, Channels, and Coordinates
# Route logic: Groups areas by the main highway/path they follow from Nairobi CBD
geo_ref = {
    # --- ROUTE 1: NAIROBI HUB & THIKA RD CORRIDOR ---
    'NAIROBI CBD': {'Lat': -1.2833, 'Lon': 36.8233, 'County': 'Nairobi', 'Route': 'Hub', 'Pot_Gen': 900, 'Pot_Beauty': 400, 'Pot_Mini': 200},
    'EASTLEIGH': {'Lat': -1.2741, 'Lon': 36.8485, 'County': 'Nairobi', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 700, 'Pot_Beauty': 250, 'Pot_Mini': 50},
    'KAMITI RD': {'Lat': -1.2050, 'Lon': 36.8900, 'County': 'Nairobi', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 150, 'Pot_Beauty': 80, 'Pot_Mini': 60},
    'GITHURAI 45': {'Lat': -1.2050, 'Lon': 36.9150, 'County': 'Kiambu', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 300, 'Pot_Beauty': 180, 'Pot_Mini': 40},
    'RUIRU-JUJA': {'Lat': -1.1167, 'Lon': 36.9667, 'County': 'Kiambu', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 350, 'Pot_Beauty': 120, 'Pot_Mini': 80},
    'THIKA': {'Lat': -1.0333, 'Lon': 37.0692, 'County': 'Kiambu', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 450, 'Pot_Beauty': 200, 'Pot_Mini': 150},
    'KIAMBU': {'Lat': -1.1714, 'Lon': 36.8356, 'County': 'Kiambu', 'Route': 'Thika Rd Corridor', 'Pot_Gen': 200, 'Pot_Beauty': 100, 'Pot_Mini': 80},

    # --- ROUTE 2: MOMBASA RD & SOUTHERN LOWER KENYA ---
    'MOMBASA RD': {'Lat': -1.3340, 'Lon': 36.8625, 'County': 'Nairobi', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 400, 'Pot_Beauty': 150, 'Pot_Mini': 300},
    'PIPELINE': {'Lat': -1.3144, 'Lon': 36.8981, 'County': 'Nairobi', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 320, 'Pot_Beauty': 280, 'Pot_Mini': 40},
    'SULTAN HAMUD': {'Lat': -2.0167, 'Lon': 37.3667, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 60, 'Pot_Beauty': 30, 'Pot_Mini': 15},
    'SALAMA': {'Lat': -1.8667, 'Lon': 37.2000, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 40, 'Pot_Beauty': 20, 'Pot_Mini': 10},
    'EMALI': {'Lat': -2.0667, 'Lon': 37.4667, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 90, 'Pot_Beauty': 40, 'Pot_Mini': 20},
    'MAKINDU': {'Lat': -2.2833, 'Lon': 37.8167, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 80, 'Pot_Beauty': 35, 'Pot_Mini': 15},
    'KIBWEZI': {'Lat': -2.4167, 'Lon': 37.9667, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 95, 'Pot_Beauty': 40, 'Pot_Mini': 20},
    'WOTE': {'Lat': -1.7808, 'Lon': 37.6258, 'County': 'Makueni', 'Route': 'Mombasa Rd Route', 'Pot_Gen': 110, 'Pot_Beauty': 50, 'Pot_Mini': 30},
    
    # --- ROUTE 3: KANGUNDO RD / GARISSA HIGHWAY ---
    'UMOJA': {'Lat': -1.2825, 'Lon': 36.8970, 'County': 'Nairobi', 'Route': 'Garissa Highway', 'Pot_Gen': 280, 'Pot_Beauty': 190, 'Pot_Mini': 60},
    'KAYOLE': {'Lat': -1.2673, 'Lon': 36.9314, 'County': 'Nairobi', 'Route': 'Garissa Highway', 'Pot_Gen': 300, 'Pot_Beauty': 210, 'Pot_Mini': 50},
    'KANGUNDO RD': {'Lat': -1.2660, 'Lon': 36.9610, 'County': 'Nairobi', 'Route': 'Garissa Highway', 'Pot_Gen': 220, 'Pot_Beauty': 90, 'Pot_Mini': 40},
    'MACHAKOS': {'Lat': -1.5177, 'Lon': 37.2634, 'County': 'Machakos', 'Route': 'Garissa Highway', 'Pot_Gen': 250, 'Pot_Beauty': 110, 'Pot_Mini': 70},
    'TALA': {'Lat': -1.2833, 'Lon': 37.2667, 'County': 'Machakos', 'Route': 'Garissa Highway', 'Pot_Gen': 80, 'Pot_Beauty': 30, 'Pot_Mini': 15},
    'KITUI': {'Lat': -1.3683, 'Lon': 37.9944, 'County': 'Kitui', 'Route': 'Garissa Highway', 'Pot_Gen': 150, 'Pot_Beauty': 70, 'Pot_Mini': 40},
    'MWINGI': {'Lat': -0.9333, 'Lon': 38.0667, 'County': 'Kitui', 'Route': 'Garissa Highway', 'Pot_Gen': 120, 'Pot_Beauty': 40, 'Pot_Mini': 20},
    'GARISSA': {'Lat': -0.4532, 'Lon': 39.6461, 'County': 'Garissa', 'Route': 'Garissa Highway', 'Pot_Gen': 200, 'Pot_Beauty': 60, 'Pot_Mini': 20},
    
    # --- ROUTE 4: WAIYAKI WAY / WESTERN ---
    'WAIYAKI WAY': {'Lat': -1.2630, 'Lon': 36.7620, 'County': 'Nairobi', 'Route': 'West Corridor', 'Pot_Gen': 120, 'Pot_Beauty': 80, 'Pot_Mini': 150},
    'WESTLANDS': {'Lat': -1.2628, 'Lon': 36.8156, 'County': 'Nairobi', 'Route': 'West Corridor', 'Pot_Gen': 90, 'Pot_Beauty': 110, 'Pot_Mini': 250},
    'PARKLANDS': {'Lat': -1.2628, 'Lon': 36.8156, 'County': 'Nairobi', 'Route': 'West Corridor', 'Pot_Gen': 50, 'Pot_Beauty': 40, 'Pot_Mini': 120},
    'KIKUYU': {'Lat': -1.2430, 'Lon': 36.6714, 'County': 'Kiambu', 'Route': 'West Corridor', 'Pot_Gen': 150, 'Pot_Beauty': 60, 'Pot_Mini': 80},
    'WANGIGE-LIMURU': {'Lat': -1.2260, 'Lon': 36.6740, 'County': 'Kiambu', 'Route': 'West Corridor', 'Pot_Gen': 140, 'Pot_Beauty': 50, 'Pot_Mini': 60},

    # --- ROUTE 5: MAGADI RD / SOUTH KAJIADO ---
    'NAIROBI WEST': {'Lat': -1.3033, 'Lon': 36.8200, 'County': 'Nairobi', 'Route': 'South Route', 'Pot_Gen': 90, 'Pot_Beauty': 45, 'Pot_Mini': 90},
    'KAREN': {'Lat': -1.3200, 'Lon': 36.7020, 'County': 'Nairobi', 'Route': 'South Route', 'Pot_Gen': 30, 'Pot_Beauty': 20, 'Pot_Mini': 140},
    'RONGAI': {'Lat': -1.3931, 'Lon': 36.7420, 'County': 'Kajiado', 'Route': 'South Route', 'Pot_Gen': 160, 'Pot_Beauty': 110, 'Pot_Mini': 130},
    'NGONG': {'Lat': -1.3621, 'Lon': 36.6565, 'County': 'Kajiado', 'Route': 'South Route', 'Pot_Gen': 140, 'Pot_Beauty': 90, 'Pot_Mini': 80},
    'KAJIADO': {'Lat': -1.8500, 'Lon': 36.7833, 'County': 'Kajiado', 'Route': 'South Route', 'Pot_Gen': 110, 'Pot_Beauty': 40, 'Pot_Mini': 30},
    'NAMANGA': {'Lat': -2.5500, 'Lon': 36.7833, 'County': 'Kajiado', 'Route': 'South Route', 'Pot_Gen': 70, 'Pot_Beauty': 25, 'Pot_Mini': 15},
}

# Fill the defaults for any missing items in the sample list above
def apply_geo(row):
    info = geo_ref.get(row['Area'], {
        'Lat': -1.28, 'Lon': 36.82, 'County': 'Other', 'Route': 'Internal Nairobi', 
        'Pot_Gen': 100, 'Pot_Beauty': 50, 'Pot_Mini': 30
    })
    return pd.Series(info)

df[['Latitude', 'Longitude', 'County', 'Route', 'Potential_General', 'Potential_Beauty', 'Potential_MiniMart']] = df.apply(apply_geo, axis=1)

# 3. Expansion Analytics
df['Total_Potential'] = df['Potential_General'] + df['Potential_Beauty'] + df['Potential_MiniMart']
df['Expansion_Headroom'] = df['Total_Potential'] - df['Customers']

# Sort by Route then Headroom to follow the logistics flow
df = df.sort_values(by=['Route', 'Expansion_Headroom'], ascending=[True, False])

# Final Check
print(f"Total Customer Verified: {df['Customers'].sum()}")
print(df[['Route', 'Area', 'Customers', 'Expansion_Headroom']].head(10))

# Export for Google My Maps
df.to_csv('nairobi_national_routes.csv', index=False)
