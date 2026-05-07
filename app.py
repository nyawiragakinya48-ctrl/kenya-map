import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# 1. Load your file
# Make sure your CSV has columns named '@lat' and '@lon' or change them below
input_file = 'supermarkets.csv'
output_file = 'supermarkets_with_counties.csv'

df = pd.read_csv(input_file)

# 2. Setup Geocoder (Using a unique user_agent is required)
geolocator = Nominatim(user_agent="kenya_retail_mapper_v2")

# This creates a function that automatically waits 1 second between calls
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1.5)

def get_county(row):
    lat = row['@lat']
    lon = row['@lon']
    
    try:
        # Perform the lookup
        location = reverse((lat, lon), language='en')
        
        if location:
            address = location.raw.get('address', {})
            
            # Kenyan counties are often mapped to 'state', 'county', or 'state_district'
            # This order (County -> State District -> State) is most reliable for Kenya
            county = address.get('county') or \
                     address.get('state_district') or \
                     address.get('state') or \
                     address.get('region') or \
                     "Unknown"
            
            print(f"Lat: {lat} | Lon: {lon} -> Found: {county}")
            return county
        return "Not Found"
        
    except Exception as e:
        print(f"Error on {lat}, {lon}: {e}")
        return "Error"

# 3. Process the data
print("Starting lookup... (Nominatim allows 1 request per second)")

# Optimization: If you have many rows, we apply the function to the unique coordinates
# and then map them back to the main table to save API calls.
df['addr:county'] = df.apply(get_county, axis=1)

# 4. Save the fixed file
df.to_csv(output_file, index=False)
print(f"\nDone! File saved as: {output_file}")
