import streamlit as st
import pandas as pd

import re
import urllib.request

from html2image import Html2Image

import zipfile
import os


@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')


def screenshots():
    _ = installff()
    st.markdown('#### &#x25A3; Download de Imagens de Screenshots')

    st.write('Arquivo CSV contendo os links. Screenshot realizado em 300px de largura e 1.000px de altura.')
    data_file = st.file_uploader("Upload arquivo CSV", type=['csv'])
    
    if data_file is not None:
        st.warning('Algumas janelas irão aparecer.')
        st.warning('Aguarde o Botão Download aparecer.')
        
        file_csv = pd.read_csv(data_file, names=['url'])

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        my_bar = st.progress(0)
        size_file = file_csv.size
        column1, column2 = st.columns(2)
        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                my_bar.progress((int(index) + 1) / size_file)
                filename = ''
                # try:
                result = urllib.request.urlopen(row['url'])
                al = result.read().decode('utf-8')
                d = re.split('<\W*title\W*(.*)</title', al, re.IGNORECASE)
                title = d[1]
                filename = title + ".jpg"

                hti = Html2Image()
                hti.firefox_path = "/home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver"
                hti.screenshot(html_str=al, save_as=filename, size=(300, 550))

                archive.write(filename)
                os.remove(filename)
                # except:
                #     with column2:
                #         st.write("NOT FOUND - " + row['url'])
    
        with column1:
            with open("hello.zip", "rb") as file:
                st.download_button(
                    label="Download ZIP",
                    data=file,
                    file_name='ImagensZIP-pyService.zip',
                    mime="application/zip",
                )
    