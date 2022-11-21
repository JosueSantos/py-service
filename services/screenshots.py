import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import streamlit as st
import pandas as pd

import zipfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from template.clipboard import clipboard


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=800x1280")
options.add_argument("--disable-features=VizDisplayCompositor")


def screenshots():
    st.markdown('#### &#x25A3; Download de Imagens de Screenshots')
    st.write('Copie os links. Screenshot realizado em 800px de largura e 1280px de altura.')
    
    value = clipboard()
    if value:
        TESTDATA = StringIO(value)
        
        global file_csv
        file_csv = pd.read_csv(TESTDATA, sep='\t', names=['url'])
        st.dataframe(file_csv)

    if st.button('Os dados estão corretos?'):
        st.warning('Aguarde o Botão Download aparecer.')
        
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
    