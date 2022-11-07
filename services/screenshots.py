import streamlit as st
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

import zipfile
import os

@st.experimental_singleton
def installff():
  os.system('sbase install chromedriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')


def screenshots():
    _ = installff()
    st.markdown('#### &#x25A3; Download de Imagens de Screenshots')

    st.write('Arquivo CSV contendo os links. Screenshot realizado em 300px de largura e 1.000px de altura.')
    data_file = st.file_uploader("Upload arquivo CSV", type=['csv'])
    
    if data_file is not None:
        st.warning('Algumas janelas irão aparecer.')
        st.warning('Aguarde o Botão Download aparecer.')
        
        file_csv = pd.read_csv(data_file, names=['url'])

        service = Service(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service)

        my_bar = st.progress(0)
        size_file = file_csv.size
        column1, column2 = st.columns(2)
        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                my_bar.progress((index + 1) / size_file)
                filename = ''
                try:
                    browser.get(row['url'])
                    browser.set_window_rect(width = 300, height = 1000)

                    title = browser.title
                    filename = title + ".jpg"

                    browser.save_screenshot(filename)

                    archive.write(filename)
                    os.remove(filename)
                except:
                    with column2:
                        st.write("NOT FOUND - " + row['url'])
    
        with column1:
            with open("hello.zip", "rb") as file:
                st.download_button(
                    label="Download ZIP",
                    data=file,
                    file_name='ImagensZIP-pyService.zip',
                    mime="application/zip",
                )
    