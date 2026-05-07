import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm  # This provides a progress bar
import time

# 1. Load your file
try:
    df = pd.read_csv('supermarkets.csv')
    print(f"Loaded {len(df)} supermarkets for processing.")
except FileNotFoundError:
    print("Error: 'supermarkets.csv' not found. Please check the file path.")
    exit()

# 2. Setup Geolocator
# NOTE: User agent must be unique. Nominatim allows 1 request per second.
geolocator = Nominatim(user_agent="kenya_retail_strategy_mapper_v2")
reverse_geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1.1)

def get_kenya_hierarchy(lat, lon):
    """
    Extracts Region, County, and Sub-County from OSM reverse geocoding for Kenya.
    """
    try:
        # Request address in English to keep names consistent
        location = reverse_geocode((lat, lon), language='en', timeout=10)
        if not location:
            return "Unknown", "Unknown", "Unknown"
        
        address = location.raw.get('address', {})

        # --- KENYA MAPPING LOGIC ---
        # 1. Region (Usually the 'state' or 'region' key in OSM for Kenya)
        region = address.get('state', address.get('region', 'Unknown'))
        
        # 2. County (Directly mapped to 'county')
        county = address.get('county', 'Unknown')
        
        # 3. Sub-County (Usually 'city_district', 'subcounty', 'suburb' or 'town')
        sub_county = address.get('subcounty', 
                     address.get('city_district', 
                     address.get('suburb', 
                     address.get('town', 'Unknown'))))

        return region, county, sub_county

    except Exception as e:
        return "Error", "Error", "Error"

# 3. Process the Data
print("\nStarting reverse geocoding across Kenya...")
print("Estimated time: ~1.2 seconds per row (Nominatim Rate Policy).")

# We create a list to store results then join them back to the dataframe
results = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    # Note: Use the exact column names from your CSV (@lat and @lon)
    region, county, subcounty = get_kenya_hierarchy(row['@lat'], row['@lon'])
    results.append({
        'Region': region,
        'County': county,
        'Sub_County': subcounty
    })

# 4. Merge results back to the original table
geo_df = pd.DataFrame(results)
df = pd.concat([df, geo_df], axis=1)

# 5. Clean up data (Remove 'County' suffix if present for cleaner tables)
df['County'] = df['County'].str.replace(' County', '')

# 6. Save the final enriched file
output_file = 'supermarkets_kenya_hierarchy.csv'
df.to_csv(output_file, index=None)

print(f"\n✅ Done! File saved as: {output_file}")
print(df[['Region', 'County', 'Sub_County']].head())
