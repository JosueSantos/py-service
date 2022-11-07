import streamlit as st
import pandas as pd

import zipfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=300x550")
options.add_argument("--disable-features=VizDisplayCompositor")


def screenshots():
    st.markdown('#### &#x25A3; Download de Imagens de Screenshots')

    st.write('Arquivo CSV contendo apenas os links. Screenshot realizado em 300px de largura e 550px de altura.')
    data_file = st.file_uploader("Upload arquivo CSV", type=['csv'])
    
    if data_file is not None:
        st.warning('Aguarde o Botão Download aparecer.')
        
        file_csv = pd.read_csv(data_file, names=['url'])
        
        my_bar = st.progress(0)
        size_file = file_csv.size
        column1, column2 = st.columns(2)
        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                my_bar.progress((index + 1) / size_file)
                filename = ''
                try:
                    with webdriver.Chrome(options=options) as browser:
                        browser.get(row['url'])

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
                st.balloons()
                st.download_button(
                    label="Download ZIP",
                    data=file,
                    file_name='ScreenshotZIP-pyService.zip',
                    mime="application/zip",
                )
    