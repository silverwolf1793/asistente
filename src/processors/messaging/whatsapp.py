"""Este módulo envía mensajes por whatsapp"""
from pywhatkit import sendwhatmsg_instantly

from src.helpers.config.config_loader import config_loader

def whatsapp(message):
    """Espera 15 segundos despues de abrir whatsapp y envía un mensaje
    al número especificado"""
    cfg = config_loader("whatsapp")
    sendwhatmsg_instantly(cfg['cel'],message,15)
