"""Este módulo buscará en amazon lo que le pidas"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.helpers.config.config_loader import config_loader
from src.helpers.website.open_chrome import open_chrome
from src.helpers.website.write_animation import write_animation

def amazon(query):
    """
    Esta función crea una nueva instancha de chrome, ingresa a amazon
    y posteriormente realiza una búsqueda con el query tras lo cual
    retorna la url
    """
    cfg = config_loader('amazon')
    driver = open_chrome(cfg['url'])
    search = driver.find_element(By.XPATH, cfg['paths']['search'])
    write_animation(search, query)
    search.send_keys(Keys.RETURN)

    return driver.current_url
