import streamlit as st
import urllib.request
import pandas as pd
from urllib import request
import zipfile
import os

def main():
    st.set_page_config(
        page_title='Serviços Python'
    )

    st.header('Serviços Python')
    st.caption('by. Josué Santos')

    st.markdown('#### &#x25A3; Download de Imagens via arquivo CSV')
    st.write('Arquivo separado por vírgulas com a primeira linha contendo o nome e a segunda o link da imagem.')
    data_file = st.file_uploader("Upload arquivo CSV", type=['csv'])
    if data_file is not None:
        file_details = {"FileName":data_file.name, "FileType":data_file.type}
        st.warning('Aguarde o Botão Download aparecer.')
        
        file_csv = pd.read_csv(data_file, names=['name', 'url'])

        with zipfile.ZipFile("hello.zip", mode="w") as archive:
            for index, row in file_csv.iterrows():
                response = request.urlretrieve(row['url'], row['name']+".jpg")
                archive.write(row['name']+".jpg")
                os.remove(row['name']+".jpg")

        with open("hello.zip", "rb") as file:
            st.download_button(
                label="Download ZIP",
                data=file,
                file_name='ImagensZIP-pyService.zip',
                mime="application/zip",
            )

if __name__ == '__main__':
    main()
