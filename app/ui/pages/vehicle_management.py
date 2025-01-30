import streamlit as st
from app.utils.maps import create_map

def display_map():
    user_location = st.text_input("Enter your location:")
    if user_location:
        map_ = create_map(user_location)
        st.write(map_)
