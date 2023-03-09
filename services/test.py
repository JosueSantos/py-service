import sys

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

import pandas as pd
import streamlit as st
from slugify import slugify

from template.clipboard_paste import clipboard_paste


def test():
    st.markdown('#### &#x25A3; Slug de colunas')
    st.write('Copie duas colunas, confira o resultado e copie para a área de transferência.')
    
    value = clipboard_paste()
    if value:
        TESTDATA = StringIO(value)
        
        global data_file
        data_file = pd.read_csv(TESTDATA, sep='\t', names=['txt1', 'txt2'])
        
        df = pd.DataFrame()
        df['slug'] = data_file['txt1'].map(str) + '-' + data_file['txt2'].map(str)
        df['slug'] = df['slug'].map(slugify)

        st.text("Origem")
        st.dataframe(data_file)

        st.text("Slug")
        st.dataframe(df)
        