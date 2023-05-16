# -*- coding: utf-8 -*-
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup


def data_card():
    st.markdown('#### &#x25A3; Raspagem de dados')
    st.write('Busca de informações sobre cartões no site https://creditis.com.br/')
    
    my_bar = st.progress(0)
    
    URL = "https://creditis.com.br/sitemap.xml"

    page = requests.get(URL)
    soup_map = BeautifulSoup(page.text, "lxml")

    cards = []
    urls = soup_map.find_all("url")

    total = len(urls)
    count = 0
    for xml_url in urls:
        count = count + 1
        my_bar.progress(count/total)
        
        URL = xml_url.find("loc").text

        if URL:
            page = requests.get(URL)
            soup = BeautifulSoup(page.text, "html.parser")
            print(URL)

            cardperfil = soup.select_one("main aside[class*='final_cardperfil']")

            if (cardperfil):
                cardinfo = soup.select_one("main section[class*='final_cardinfo']")

                name = cardinfo.select_one("h1").get_text()
                description = cardinfo.select_one("div div p").get_text()
                
                perfil = cardperfil.select_one("div div h5").get_text()
                informations = cardperfil.select_one("div.flex-column")
                informations_json = {}
                for item in informations:
                    title_information = item.select_one("span").get_text()
                    title_information = title_information.replace(":", "").strip()

                    item_information = item.select_one("p")
                    if(item_information):
                        type_card = item_information.select_one("img")
                        if(type_card):
                            item_information = type_card['title']
                        else:
                            item_information = item_information.get_text()
                    else:
                        item_information = item.select("span")[1].get_text()
                    
                    informations_json["info-" + title_information] = item_information
                
                descinject = soup.select_one("main section *[class*='final_descinject']")
                descinject_json = {}

                list_descinject = descinject.select("p")
                for item in list_descinject:
                    if(item):
                        if(item.select_one("strong")):
                            title_item = item.select_one("strong").get_text()
                            title_item = title_item.replace(":", "").strip()

                            text_item = item.find(text=True, recursive=False)

                            descinject_json["vant-" + title_item] = text_item
                
                listaben = soup.select("main section *[class*='final_listaben']")
                listaben_json = {}
                for ben in listaben:
                    title_ben = ben.select_one("h3").get_text()
                    title_ben = title_ben.replace(":", "").strip()

                    text_ben = ben.select_one("h3+div").get_text()

                    listaben_json["ben-" + title_ben] = text_ben

                row = {
                    "Nome do Cartão": name,
                    "Descrição": description,
                    "URL": URL,
                    "Perfil": perfil
                }

                row = {**row, **informations_json}
                row = {**row, **listaben_json}
                row = {**row, **descinject_json}

                cards.append(row)

    df = pd.DataFrame(cards)
    df = df.fillna("")

    st.dataframe(df)

    st.download_button(
        label="Download",
        data=df.to_csv().encode('utf-8'),
        file_name="Cards.csv",
        mime='text/csv',
    )
    