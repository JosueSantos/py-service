import streamlit as st
import os

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

from partials.navbar import streamlit_menu
from services.download_img import download_img
from services.screenshots import screenshots
from selenium import webdriver
from selenium.webdriver import FirefoxOptions


def main():
    st.set_page_config(
        page_title='Serviços Python'
    )

    st.header('Serviços Python')
    st.caption('by. Josué Santos')

    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)

    browser.get('http://example.com')
    st.write(browser.page_source)

    selected = streamlit_menu()

    if selected == "Download de Imagens":
        download_img()
    if selected == "Screenshots":
        screenshots()

if __name__ == '__main__':
    main()
