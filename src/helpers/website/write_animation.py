"""Este módulo contiene lo necesario para realizar animaciones de escritura"""
from time import sleep
from selenium.webdriver.remote import webelement

def write_animation(element: webelement, query: str):
    """
    escribimos dentro del elemento el query letra a letra
    dejando un pequeño tiempo de espera entre letras para que parezca
    una animación de escritura
    """
    for char in query:
        element.send_keys(char)
        sleep(0.2)
