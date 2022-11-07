import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

st.balloons()
with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
    url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
    driver.get(url)
    xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
    # Wait for the element to be rendered:
    element = WebDriverWait(driver, 10).until(lambda x: x.find_elements(by=By.XPATH, value=xpath))
    name = element[0].get_property('attributes')[0]['name']
    st.write(name)

    driver.get('http://example.com')
    st.write(driver.page_source)

from partials.navbar import streamlit_menu
from services.download_img import download_img
from services.screenshots import screenshots
from selenium import webdriver


def main():
    st.set_page_config(
        page_title='Serviços Python'
    )

    st.header('Serviços Python')
    st.caption('by. Josué Santos')

    selected = streamlit_menu()

    if selected == "Download de Imagens":
        download_img()
    if selected == "Screenshots":
        screenshots()

if __name__ == '__main__':
    main()
