import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import streamlit as st
import urllib.request
import pandas as pd
from urllib import request
import zipfile
import os
from template.clipboard import clipboard


def test():
    st.markdown('#### &#x25A3; Download de Imagens & Renomear')
    st.write('Copie duas colunas, exatamente com a primeira linha contendo o nome e a segunda o link da imagem.')
    
    value = clipboard()
    if value:
        TESTDATA = StringIO(value)
        
        global data_file
        data_file = pd.read_csv(TESTDATA, sep='\t', names=['name', 'url'])
        st.dataframe(data_file)

    if st.button('Os dados estão corretos?'):
        st.warning('Aguarde o Botão Download aparecer.')

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in data_file.iterrows():
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