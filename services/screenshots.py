import streamlit as st
import pandas as pd

import zipfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=300x1000")
options.add_argument("--disable-features=VizDisplayCompositor")


def screenshots():
    st.markdown('#### &#x25A3; Download de Imagens de Screenshots')

    st.write('Arquivo CSV contendo os links. Screenshot realizado em 300px de largura e 1.000px de altura.')
    data_file = st.file_uploader("Upload arquivo CSV", type=['csv'])
    
    if data_file is not None:
        st.warning('Algumas janelas irão aparecer.')
        st.warning('Aguarde o Botão Download aparecer.')
        
        file_csv = pd.read_csv(data_file, names=['url'])

        with webdriver.Chrome(options=options) as driver:
            url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
            driver.get('http://example.com')
            st.write(driver.page_source)
            browser = webdriver.Firefox(executable_path='/home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver')
        
        my_bar = st.progress(0)
        size_file = file_csv.size
        column1, column2 = st.columns(2)
        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                my_bar.progress((index + 1) / size_file)
                filename = ''
                # try:
                with webdriver.Chrome(options=options) as browser:
                    browser.get('http://example.com')
                    st.write(browser.page_source)
                
                    browser.get(row['url'])
                    browser.set_window_rect(width = 300, height = 1000)

                    title = browser.title
                    filename = title + ".jpg"

                    st.write(filename)

                    browser.save_screenshot(filename)

                    archive.write(filename)
                    os.remove(filename)
                # except:
                #     with column2:
                #         st.write("NOT FOUND - " + row['url'])
    
        with column1:
            with open("hello.zip", "rb") as file:
                st.balloons()
                st.download_button(
                    label="Download ZIP",
                    data=file,
                    file_name='ImagensZIP-pyService.zip',
                    mime="application/zip",
                )
    