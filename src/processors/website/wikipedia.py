"""Este módulo realiza búsquedas en wikipedia"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.helpers.config.config_loader import config_loader
from src.helpers.website.open_chrome import open_chrome
from src.helpers.website.write_animation import write_animation

def wikipedia(query):
    """Se abrirá wikipedia y buscará lo que se encuentra en el query"""
    cfg = config_loader('wikipedia')
    driver = open_chrome(cfg['url'])
    search = driver.find_element(By.XPATH, cfg['paths']['search'])
    write_animation(search,query)
    search.send_keys(Keys.RETURN)
    return driver.current_url
