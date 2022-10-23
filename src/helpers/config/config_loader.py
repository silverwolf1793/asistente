"""This module has everything related to configurations"""
from json import load
def config_loader(config_name: str):
    """
    This function loads the configuration file and sends the configuration
    sent on the argument if exists else return None
    """
    with open('./config.json','r',encoding='utf-8') as raw_config:
        main_config = load(raw_config)
    if config_name in main_config.keys():
        return main_config[config_name]
    return None
