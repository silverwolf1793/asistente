"""Este módulo crea instancias de chrome"""
from selenium import webdriver
from src.helpers.config.config_loader import config_loader

def open_chrome(url: str):
    """esta función crea una nueva instancia de chrome"""
    cfg = config_loader('chrome')
    options = webdriver.ChromeOptions()
    # este argumento evita que algunas webs detecten la automatización
    options.add_argument("--disable-blink-features=AutomationControlled")
    # este elemento evita que la ventana se cierre al terminar la función
    options.add_experimental_option("detach", True)

    # creamos una nueva instancia con las opciones anteriores especificando
    # el lugar en dónde se encuentra el driver
    driver = webdriver.Chrome(
        options=options,
        executable_path=cfg['path'],
    )
    # maximizamos la ventana
    driver.maximize_window()
    # ingresamos a la página solicitada
    driver.get(url)
    return driver
