import csv
import requests
import folium

# Mapbox access token
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicmVlc2VsaGFuc2VuIiwiYSI6ImNtbHR4MWtoYjA1NmwzZG9tcms0NjY2dzgifQ.5-nQCNIzKfjduK9YRduXjw"

# Your custom Mapbox style URL
# Format: https://api.mapbox.com/styles/v1/{username}/{style_id}/tiles/256/{z}/{x}/{y}@2x?access_token={token}
MAPBOX_STYLE_URL = f"https://api.mapbox.com/styles/v1/reeselhansen/cmm11hknz002f01s5cdsr0q2f/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_ACCESS_TOKEN}"

# Color scheme for different location types
MARKER_COLORS = {
    'restaurant': 'red',
    'cafe': 'orange', 
    'activity': 'green',
    'school': 'blue'
}

# Icon scheme for different location types
MARKER_ICONS = {
    'restaurant': 'cutlery',
    'cafe': 'coffee',
    'activity': 'tree',
    'school': 'graduation-cap'
}

def geocode_address(address):
    """Geocode an address using the Mapbox Geocoding API."""
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    encoded_address = requests.utils.quote(address)
    url = f"{base_url}/{encoded_address}.json?access_token={MAPBOX_ACCESS_TOKEN}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("features"):
            # Get the first result's coordinates [longitude, latitude]
            coords = data["features"][0]["center"]
            return {"longitude": coords[0], "latitude": coords[1]}
    return None

def read_and_geocode_csv(csv_path):
    """Read CSV file and geocode all addresses."""
    locations = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get('Name ', '').strip()  # Note: CSV has trailing space in header
            address = row.get('Address', '').strip()
            loc_type = row.get('Type', '').strip()
            description = row.get('Description ', '').strip()  # Note: trailing space
            image_url = row.get('Image URL', '').strip()
            
            print(f"Geocoding: {name}")
            coords = geocode_address(address)
            
            if coords:
                locations.append({
                    'name': name,
                    'address': address,
                    'type': loc_type,
                    'description': description,
                    'image_url': image_url,
                    'latitude': coords['latitude'],
                    'longitude': coords['longitude']
                })
                print(f"  -> Found: {coords['latitude']}, {coords['longitude']}")
            else:
                print(f"  -> Could not geocode address")
    
    return locations

def create_map(locations, output_file="hometown_map.html"):
    """Create a Folium map with custom Mapbox basemap and color-coded markers."""
    if not locations:
        print("No locations to map!")
        return
    
    # Calculate center of map from all locations
    avg_lat = sum(loc['latitude'] for loc in locations) / len(locations)
    avg_lng = sum(loc['longitude'] for loc in locations) / len(locations)
    
    # Create map with custom Mapbox tile layer
    m = folium.Map(
        location=[avg_lat, avg_lng],
        zoom_start=14,
        tiles=None  # Start with no tiles, add custom one
    )
    
    # Add custom Mapbox basemap
    folium.TileLayer(
        tiles=MAPBOX_STYLE_URL,
        attr='Mapbox',
        name='Mapbox Streets',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add markers for each location
    for loc in locations:
        loc_type = loc['type'].lower()
        color = MARKER_COLORS.get(loc_type, 'gray')
        icon = MARKER_ICONS.get(loc_type, 'info-sign')
        
        # Create popup HTML with image and description
        popup_html = f"""
        <div style="width: 250px;">
            <h4 style="margin: 0 0 8px 0;">{loc['name']}</h4>
            <img src="{loc['image_url']}" style="width: 100%; max-height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">
            <p style="font-size: 12px; margin: 4px 0;"><strong>Type:</strong> {loc['type'].title()}</p>
            <p style="font-size: 12px; margin: 4px 0;"><strong>Address:</strong> {loc['address']}</p>
            <p style="font-size: 11px; margin: 4px 0;">{loc['description']}</p>
        </div>
        """
        
        folium.Marker(
            location=[loc['latitude'], loc['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=loc['name'],
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
    
    # Add a legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; 
                padding: 10px; border-radius: 5px; border: 2px solid gray; font-size: 12px;">
        <strong>Location Types</strong><br>
        <i class="fa fa-cutlery" style="color: red;"></i> Restaurant<br>
        <i class="fa fa-coffee" style="color: orange;"></i> Cafe<br>
        <i class="fa fa-tree" style="color: green;"></i> Activity/Park<br>
        <i class="fa fa-graduation-cap" style="color: blue;"></i> School
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(output_file)
    print(f"\nMap saved to {output_file}")

if __name__ == "__main__":
    csv_path = "images/hometown_locations - Sheet1.csv"
    locations = read_and_geocode_csv(csv_path)
    
    print(f"\n--- Geocoded {len(locations)} locations ---")
    for loc in locations:
        print(f"{loc['name']}: ({loc['latitude']}, {loc['longitude']})")
    
    # Create and save the map
    create_map(locations)



