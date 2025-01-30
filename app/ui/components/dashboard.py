import streamlit as st
import plotly.graph_objects as go
from app.services.vehicle_service import get_vehicles

def display_dashboard(user_id):
    vehicles = get_vehicles(user_id)
    vehicle_options = [vehicle.registration_number for vehicle in vehicles]
    selected_vehicle = st.selectbox("Select Vehicle", vehicle_options)
    st.write(f"Selected Vehicle: {selected_vehicle}")

    # Visualization or further analysis code here
