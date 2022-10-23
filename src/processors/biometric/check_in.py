"""Este módulo realiza el reconocimiento biométrico"""
import os
import face_biometric_recognition as face_recognition

from src.helpers.config.config_loader import config_loader
from src.helpers.image.capture_frame import capture_frame

def check_in():
    """Dentro de esta función que realiza el faceID"""
    capture_frame("./memory/image/unknown.png")
    cfg = config_loader("assistant")

    print("comenzar reconocimiento de imágen")
    # cargamos la foto de un usuario "registrado", la cual es una selfie de la persona
    known_image = face_recognition.load_image_file(cfg['selfie_path'])
    known_image_encoding = face_recognition.face_encodings(known_image)[0]

    # cargamos la foto tomada desde la webcam
    uknown_image = face_recognition.load_image_file("./memory/image/unknown.png")
    uknown_image_encoding = face_recognition.face_encodings(uknown_image)

    # removemos la imágen temporal y comparamos todas las caras que encontró
    # para ver si es la del usuario registrado
    # os.remove("./memory/image/unknown.png")

    if len(uknown_image_encoding) > 0:
        result = False
        for unknown in uknown_image_encoding:
            result = face_recognition.compare_faces([known_image_encoding], unknown)[0]
            if result:
                return "person_in_photo"
        return "person_not_in_photo"
    return "no_faces_detected"
