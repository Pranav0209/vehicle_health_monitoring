import streamlit as st
from app.ui.components.dashboard import display_dashboard
from app.ui.pages.vehicle_management import display_map

def home_page(user_id):
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select Page", ["Dashboard", "Vehicle Management", "Map"])

    if option == "Dashboard":
        display_dashboard(user_id)
    elif option == "Vehicle Management":
        display_map()
    elif option == "Map":
        display_map()
