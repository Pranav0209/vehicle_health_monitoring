import folium
from geopy.geocoders import Nominatim

def create_map(location):
    # Create a map centered around the location
    geolocator = Nominatim(user_agent="vehicle_health_monitoring")
    location = geolocator.geocode(location)
    if location:
        map_center = [location.latitude, location.longitude]
    else:
        map_center = [0, 0]  # Default to a neutral location

    m = folium.Map(location=map_center, zoom_start=12)
    folium.Marker(location=map_center, popup='Your Location').add_to(m)
    return m
