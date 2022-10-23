"""Este módulo simplemente abre la página de linkedin"""
from src.helpers.config.config_loader import config_loader
from src.helpers.website.open_chrome import open_chrome

def linkedin():
    """Solo abre la página de linkedin"""
    cfg = config_loader('linkedin')
    driver = open_chrome(cfg['url'])
    return driver.current_url
