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
import pyperclip
from slugify import slugify


def slug():
    st.markdown('#### &#x25A3; Slug de colunas')
    st.write('Copie duas colunas, confira o resultado e copie para a área de transferência.')
    
    value = clipboard()
    if value:
        TESTDATA = StringIO(value)
        
        global data_file
        data_file = pd.read_csv(TESTDATA, sep='\t', names=['txt1', 'txt2'])
        
        df = pd.DataFrame()
        df['slug'] = data_file['txt1'].map(str) + '-' + data_file['txt2'].map(str)
        df['slug'] = df['slug'].map(slugify)

        if st.button('Copiar'):
            pyperclip.copy(df.to_string(index=False, header=False))

        st.text("Origem")
        st.dataframe(data_file)

        st.text("Slug")
        st.dataframe(df)

        if st.button('Copiar '):
            pyperclip.copy(df.to_string(index=False, header=False))
