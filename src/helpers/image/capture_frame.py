"""Este módulo captura frames de la cámara"""
import cv2

from src.helpers.config.config_loader import config_loader

def capture_frame(path:str):
    """
    Esta función carga la cámara, la configura y graba un segundo de video
    para estabilizarlo, tras lo cual captura el último frame y lo guarda
    como una imágen temporal
    """
    cfg = config_loader('camera')
    print("configurando la cámara")
    cam = cv2.VideoCapture(cfg['port'])
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,cfg['width'])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,cfg['height'])
    print("capturando video")
    for _ in range(cfg['framerate']):
        _, frame = cam.read()
    print("salvando el último frame")
    cv2.imwrite(path, frame)
