import sys

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import os
import urllib.request
import zipfile
from urllib import request

import pandas as pd
import streamlit as st

from template.clipboard_paste import clipboard_paste


def download_img():
    st.markdown('#### &#x25A3; Download de Imagens & Renomea-las')
    st.write('Copie duas colunas, exatamente com a primeira linha contendo o nome e a segunda o link da imagem.')
    
    value = clipboard_paste()
    if value:
        TESTDATA = StringIO(value)
        
        global file_csv
        file_csv = pd.read_csv(TESTDATA, sep='\t', names=['name', 'url'])
        st.dataframe(file_csv)

    if st.button('Os dados estão corretos?'):
        st.warning('Aguarde o Botão Download aparecer.')

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                request.urlretrieve(row['url'], row['name']+".jpg")

                archive.write(row['name']+".jpg")
                os.remove(row['name']+".jpg")

        with open("hello.zip", "rb") as file:
            st.balloons()
            st.download_button(
                label="Download ZIP",
                data=file,
                file_name='ImagensZIP-pyService.zip',
                mime="application/zip",
            )