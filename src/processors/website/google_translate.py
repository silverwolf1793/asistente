"""Este módulo traduce la frase que le envíes"""
from selenium.webdriver.common.by import By
from src.helpers.config.config_loader import config_loader
from src.helpers.website.write_animation import write_animation
from src.helpers.website.open_chrome import open_chrome

def google_translate(query):
    """
    Esta función crea una nueva instancha de chrome, ingresa a google translate,
    da click para traducir del español al inglés y finalmente traduce el texto
    """
    cfg = config_loader('google_translate')
    driver = open_chrome(cfg['url'])
    driver.find_element(By.XPATH, cfg['paths']['set_english_btn']).click()
    search = driver.find_element(By.XPATH, cfg['paths']['text_to_translate_area'])
    write_animation(search, query)

    return driver.current_url
