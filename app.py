import streamlit as st

from partials.navbar import streamlit_menu
from services.data_card import data_card
from services.download_img import download_img
from services.screenshots import screenshots
from services.slug import slug
from services.test import test


def main():
    st.set_page_config(
        page_title='Serviços Python'
    )

    st.header('Serviços Python')
    st.caption('by. Josué Santos')

    selected = streamlit_menu()

    if selected == "Download de Imagens":
        download_img()
    if selected == "Screenshots":
        screenshots()
    if selected == "Slug":
        slug()
    if selected == "Dados de Cartões":
        data_card()
    if selected == "Test":
        test()

if __name__ == '__main__':
    main()
