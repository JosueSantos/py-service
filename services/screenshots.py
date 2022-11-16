import streamlit as st
import pandas as pd

import zipfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from io import StringIO

import pyperclip


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
    
    st.write(pyperclip.paste())

    copy_button = Button(label="Get Clipboard Data")
    copy_button.js_on_event("button_click", CustomJS(code="""
        navigator.clipboard.readText().then(text => document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: text})))
        """))
    result = streamlit_bokeh_events(
        copy_button,
        events="GET_TEXT",
        key="get_text",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            df = pd.read_csv(StringIO(result.get("GET_TEXT")))
            st.table(df)
    # if st.button('Colar da área de transferência'):
    #     global data_file
    #     data_file = pd.read_clipboard(names=['url'])
    #     st.dataframe(data_file)

    # if st.button('Os dados estão corretos?'):
    #     st.warning('Aguarde o Botão Download aparecer.')
        
    #     my_bar = st.progress(0)
    #     size_file = data_file.size
    #     column1, column2 = st.columns(2)
    #     with zipfile.ZipFile("hello.zip", mode="w") as archive:
    #         for index, row in data_file.iterrows():
    #             my_bar.progress((index + 1) / size_file)
    #             filename = ''
    #             try:
    #                 with webdriver.Chrome(options=options) as browser:
    #                     browser.get(row['url'])

    #                     title = browser.title
    #                     filename = title + ".jpg"

    #                     browser.save_screenshot(filename)

    #                     archive.write(filename)
    #                     os.remove(filename)
    #             except:
    #                 with column2:
    #                     st.write("NOT FOUND - " + row['url'])
    
    #     with column1:
    #         with open("hello.zip", "rb") as file:
    #             st.balloons()
    #             st.download_button(
    #                 label="Download ZIP",
    #                 data=file,
    #                 file_name='ScreenshotZIP-pyService.zip',
    #                 mime="application/zip",
    #             )
    