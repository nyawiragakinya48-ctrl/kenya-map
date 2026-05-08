import pandas as pd

# 1. Full Dataset with corrected Administrative Mapping
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

# 2. Reference Table for Geography (Counties and Sub-Counties)
geo_ref = {
    'EASTLEIGH': {'Lat': -1.2741, 'Lon': 36.8485, 'County': 'Nairobi', 'Sub_County': 'Kamkunji'},
    'NAIROBI CBD': {'Lat': -1.2833, 'Lon': 36.8233, 'County': 'Nairobi', 'Sub_County': 'Starehe'},
    'THIKA': {'Lat': -1.0333, 'Lon': 37.0692, 'County': 'Kiambu', 'Sub_County': 'Thika West'},
    'KAMITI RD': {'Lat': -1.2050, 'Lon': 36.8900, 'County': 'Nairobi', 'Sub_County': 'Roysambu'},
    'KITUI': {'Lat': -1.3683, 'Lon': 37.9944, 'County': 'Kitui', 'Sub_County': 'Kitui Central'},
    'MOMBASA RD': {'Lat': -1.3340, 'Lon': 36.8625, 'County': 'Nairobi', 'Sub_County': 'Embakasi South'},
    'KAYOLE': {'Lat': -1.2673, 'Lon': 36.9314, 'County': 'Nairobi', 'Sub_County': 'Embakasi Central'},
    'RUIRU-JUJA': {'Lat': -1.1167, 'Lon': 36.9667, 'County': 'Kiambu', 'Sub_County': 'Ruiru'},
    'NAIROBI WEST': {'Lat': -1.3033, 'Lon': 36.8200, 'County': 'Nairobi', 'Sub_County': 'Langata'},
    'KADAMALA': {'Lat': -1.3150, 'Lon': 36.8850, 'County': 'Nairobi', 'Sub_County': 'Embakasi East'},
    'UMOJA': {'Lat': -1.2825, 'Lon': 36.8970, 'County': 'Nairobi', 'Sub_County': 'Embakasi West'},
    'RONGAI': {'Lat': -1.3931, 'Lon': 36.7420, 'County': 'Kajiado', 'Sub_County': 'Kajiado North'},
    'UTAWALA': {'Lat': -1.2750, 'Lon': 36.9830, 'County': 'Nairobi', 'Sub_County': 'Embakasi East'},
    'KASA-MWIKI': {'Lat': -1.2250, 'Lon': 36.9080, 'County': 'Nairobi', 'Sub_County': 'Kasarani'},
    'WANGIGE-LIMURU': {'Lat': -1.2260, 'Lon': 36.6740, 'County': 'Kiambu', 'Sub_County': 'Kabete'},
    'GARISSA': {'Lat': -0.4532, 'Lon': 39.6461, 'County': 'Garissa', 'Sub_County': 'Garissa Township'},
    'MACHAKOS': {'Lat': -1.5177, 'Lon': 37.2634, 'County': 'Machakos', 'Sub_County': 'Machakos Town'},
    'PIPELINE': {'Lat': -1.3144, 'Lon': 36.8981, 'County': 'Nairobi', 'Sub_County': 'Embakasi South'},
    'KILIMANI': {'Lat': -1.2913, 'Lon': 36.7880, 'County': 'Nairobi', 'Sub_County': 'Dagoretti North'},
    'KAWANGWARE': {'Lat': -1.2861, 'Lon': 36.7450, 'County': 'Nairobi', 'Sub_County': 'Dagoretti North'},
    'GITHURAI 45': {'Lat': -1.2050, 'Lon': 36.9150, 'County': 'Kiambu', 'Sub_County': 'Ruiru'},
    'MWINGI': {'Lat': -0.9333, 'Lon': 38.0667, 'County': 'Kitui', 'Sub_County': 'Mwingi Central'},
    'NGONG': {'Lat': -1.3621, 'Lon': 36.6565, 'County': 'Kajiado', 'Sub_County': 'Kajiado North'},
    'WOTE': {'Lat': -1.7808, 'Lon': 37.6258, 'County': 'Makueni', 'Sub_County': 'Makueni'},
    'KIBWEZI': {'Lat': -2.4167, 'Lon': 37.9667, 'County': 'Makueni', 'Sub_County': 'Kibwezi East'},
    'KIAMBU': {'Lat': -1.1714, 'Lon': 36.8356, 'County': 'Kiambu', 'Sub_County': 'Kiambu Town'},
    'OLOITOKTOK': {'Lat': -2.8500, 'Lon': 37.5167, 'County': 'Kajiado', 'Sub_County': 'Kajiado South'},
    'KANGUNDO RD': {'Lat': -1.2660, 'Lon': 36.9610, 'County': 'Nairobi', 'Sub_County': 'Njiru'},
    'PARKLANDS': {'Lat': -1.2628, 'Lon': 36.8156, 'County': 'Nairobi', 'Sub_County': 'Westlands'},
    'KIKUYU': {'Lat': -1.2430, 'Lon': 36.6714, 'County': 'Kiambu', 'Sub_County': 'Kikuyu'},
    'MATUU': {'Lat': -1.1333, 'Lon': 37.5500, 'County': 'Machakos', 'Sub_County': 'Yatta'},
    'EMALI': {'Lat': -2.0667, 'Lon': 37.4667, 'County': 'Makueni', 'Sub_County': 'Kibwezi West'},
    'NAMANGA': {'Lat': -2.5500, 'Lon': 36.7833, 'County': 'Kajiado', 'Sub_County': 'Kajiado Central'},
    'WAIYAKI WAY': {'Lat': -1.2630, 'Lon': 36.7620, 'County': 'Nairobi', 'Sub_County': 'Westlands'},
    'KAJIADO': {'Lat': -1.8500, 'Lon': 36.7833, 'County': 'Kajiado', 'Sub_County': 'Kajiado Central'},
    'ISINYA': {'Lat': -1.6667, 'Lon': 36.8500, 'County': 'Kajiado', 'Sub_County': 'Kajiado East'},
    'MAKINDU': {'Lat': -2.2833, 'Lon': 37.8167, 'County': 'Makueni', 'Sub_County': 'Kibwezi West'},
    'KIBRA': {'Lat': -1.3122, 'Lon': 36.7876, 'County': 'Nairobi', 'Sub_County': 'Kibra'},
    'JOGOO RD': {'Lat': -1.2900, 'Lon': 36.8550, 'County': 'Nairobi', 'Sub_County': 'Makadara'},
    'SULTAN HAMUD': {'Lat': -2.0167, 'Lon': 37.3667, 'County': 'Makueni', 'Sub_County': 'Kibwezi West'},
    'JOGOO ROAD': {'Lat': -1.2900, 'Lon': 36.8551, 'County': 'Nairobi', 'Sub_County': 'Makadara'},
    'NUNGUNI': {'Lat': -1.6833, 'Lon': 37.2833, 'County': 'Makueni', 'Sub_County': 'Kaiti'},
    'BISIL': {'Lat': -2.1333, 'Lon': 36.7833, 'County': 'Kajiado', 'Sub_County': 'Kajiado Central'},
    'TALA': {'Lat': -1.2833, 'Lon': 37.2667, 'County': 'Machakos', 'Sub_County': 'Matungulu'},
    'KAREN': {'Lat': -1.3200, 'Lon': 36.7020, 'County': 'Nairobi', 'Sub_County': 'Langata'},
    'SALAMA': {'Lat': -1.8667, 'Lon': 37.2000, 'County': 'Makueni', 'Sub_County': 'Kilome'},
    'KANGUNDO': {'Lat': -1.3000, 'Lon': 37.3500, 'County': 'Machakos', 'Sub_County': 'Kangundo'},
    'KOLA': {'Lat': -1.6167, 'Lon': 37.3167, 'County': 'Machakos', 'Sub_County': 'Machakos Town'},
}

# 3. Join logic
def get_geo(area):
    return pd.Series(geo_ref.get(area, {'Lat':0, 'Lon':0, 'County':'Unknown', 'Sub_County':'Unknown'}))

df[['Latitude', 'Longitude', 'County', 'Sub_County']] = df['Area'].apply(get_geo)

# 4. Add Population Density Logic for Nairobi/Satellite
density_map = {
    'Nairobi': 'High', 'Kiambu': 'Medium-High', 'Machakos': 'Medium', 
    'Kajiado': 'Medium-Low', 'Makueni': 'Low', 'Garissa': 'Low', 'Kitui': 'Low'
}
df['Pop_Density_Class'] = df['County'].map(density_map)

# Check sum: should be 942
print(f"Verified Total Customers: {df['Customers'].sum()}")

# Export to CSV for Google Maps
df.to_csv('nairobi_market_mapping_ready.csv', index=False)
