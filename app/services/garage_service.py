from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import requests
import time

class GarageService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="vehicle_health_monitor")

    def get_nearby_garages(self, pincode, radius=5000):
        """
        Find nearby garages using OpenStreetMap
        Args:
            pincode: User's pincode
            radius: Search radius in meters (default 5km)
        Returns:
            List of nearby garages with details and map HTML
        """
        try:
            # Get coordinates from pincode
            location = self.geolocator.geocode(pincode)
            if not location:
                return [], ""

            # Use Overpass API to find garages
            overpass_url = "http://overpass-api.de/api/interpreter"
            radius_km = radius / 1000
            overpass_query = f"""
            [out:json];
            (
              node["shop"="car_repair"](around:{radius},{location.latitude},{location.longitude});
              way["shop"="car_repair"](around:{radius},{location.latitude},{location.longitude});
              node["amenity"="car_repair"](around:{radius},{location.latitude},{location.longitude});
              way["amenity"="car_repair"](around:{radius},{location.latitude},{location.longitude});
            );
            out body;
            >;
            out skel qt;
            """
            
            # Add delay to respect rate limits
            time.sleep(1)
            response = requests.get(overpass_url, params={'data': overpass_query})
            data = response.json()

            garages = []
            for element in data.get('elements', []):
                if element.get('type') in ['node', 'way']:
                    tags = element.get('tags', {})
                    
                    # Get coordinates
                    if element['type'] == 'node':
                        lat, lon = element.get('lat'), element.get('lon')
                    else:
                        # For ways, use the center coordinates
                        center = self.get_way_center(element.get('nodes', []))
                        if not center:
                            continue
                        lat, lon = center

                    # Calculate distance
                    garage_coords = (lat, lon)
                    distance = geodesic(
                        (location.latitude, location.longitude),
                        garage_coords
                    ).kilometers

                    garage = {
                        'name': tags.get('name', 'Car Service Center'),
                        'address': tags.get('addr:full', tags.get('addr:street', '')),
                        'phone': tags.get('phone', ''),
                        'website': tags.get('website', ''),
                        'distance': f"{distance:.1f} km",
                        'location': {
                            'lat': lat,
                            'lng': lon
                        }
                    }
                    garages.append(garage)

            # Sort by distance
            garages = sorted(garages, key=lambda x: float(x['distance'].split()[0]))

            # Create map
            map_html = self.create_map(location.latitude, location.longitude, garages)

            return garages, map_html

        except Exception as e:
            print(f"Error finding nearby garages: {e}")
            return [], ""

    def get_way_center(self, node_ids):
        """Calculate center point of a way using its nodes"""
        try:
            # Query node coordinates
            overpass_url = "http://overpass-api.de/api/interpreter"
            nodes_query = f"""
            [out:json];
            node(id:{','.join(map(str, node_ids))});
            out body;
            """
            
            time.sleep(1)  # Respect rate limits
            response = requests.get(overpass_url, params={'data': nodes_query})
            data = response.json()

            if not data.get('elements'):
                return None

            # Calculate center
            lats = [node['lat'] for node in data['elements']]
            lons = [node['lon'] for node in data['elements']]
            return sum(lats) / len(lats), sum(lons) / len(lons)

        except Exception as e:
            print(f"Error getting way center: {e}")
            return None

    def create_map(self, lat, lon, garages):
        """Create a Folium map with garage markers"""
        # Create map centered on user location
        m = folium.Map(location=[lat, lon], zoom_start=13)

        # Add user location marker
        folium.Marker(
            [lat, lon],
            popup='Your Location',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Add garage markers
        for garage in garages:
            popup_html = f"""
            <div style="width: 200px;">
                <h6>{garage['name']}</h6>
                <p>{garage['address']}</p>
                <p>Distance: {garage['distance']}</p>
                {f'<p>Phone: <a href="tel:{garage["phone"]}">{garage["phone"]}</a></p>' if garage['phone'] else ''}
                {f'<p><a href="{garage["website"]}" target="_blank">Website</a></p>' if garage['website'] else ''}
            </div>
            """
            
            folium.Marker(
                [garage['location']['lat'], garage['location']['lng']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

        return m._repr_html_()
