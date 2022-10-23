"""Este módulo abrirá una página de youtube y buscará un video"""
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.helpers.website.write_animation import write_animation
from src.helpers.config.config_loader import config_loader
from src.helpers.website.open_chrome import open_chrome

def youtube(query):
    """
    Esta función inicia una instancia de chrome y abre youtube, tras lo cual
    escribe dentro del cuadro de búsqueda el query, simula la tecla "enter",
    espera para que cargue la página y finalmente da click en el primer video,
    tras lo cual retorna la URL del video en que haya hecho click
    """
    cfg = config_loader('youtube')
    driver = open_chrome(cfg['url'])
    search = driver.find_element(By.XPATH, cfg['paths']['search'])
    write_animation(search, query)
    search.send_keys(Keys.RETURN)
    sleep(2)
    video = driver.find_element(By.XPATH,  cfg['paths']['first_video'])
    url = video.get_attribute("href")
    sleep(1)
    driver.get( url)
    return driver.current_url
