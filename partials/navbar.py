import streamlit as st
from streamlit_option_menu import option_menu


menu = [
    "Home",
    "Download de Imagens",
    "Screenshots"
]

icons = [
    "house-fill",
    "file-earmark-image",
    "camera-fill"
]

def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=menu,
            icons=icons,
            menu_icon="cast",
            default_index=0
        )
        
        return selected
