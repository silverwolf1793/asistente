"""Este módulo realiza un reconocimiento de objetos por medio de inteligencia artificial"""
from subprocess import Popen
import json
import os
from imageai.Detection import ObjectDetection

from src.helpers.image.capture_frame import capture_frame

def object_detection():
    """
    Esta función utiliza la webcam para tomar una fotografía
    tras lo cual la analiza y coloca sus resultados en la memoria
    dentro de ./memory/object_detection/results
    """
    # ahora vamos a declarar donde viven los recurso que necesitamos
    model_path = "./memory/object_detection/models/resnet50_coco_best_v2.1.0.h5"
    input_path =  "./memory/object_detection/results/unknown.png"
    output_path =  "./memory/object_detection/results/scanned.png"
    text_output_path = os.path.abspath("./memory/object_detection/results/results.txt")

    capture_frame(input_path)

    # Inicializamos el objeto encargado de realizar el escaneo
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()

    # Finalmente la IA comenzará a buscar los objetos que encuentre
    detections = detector.detectObjectsFromImage(
        input_image=input_path,
        output_image_path=output_path
    )

    # Y ahora guardamos todos los resultados de la búsqueda
    with open(text_output_path,'w',encoding="utf-8") as file:
        file.write(json.dumps(detections,indent=4))

    with Popen(r'explorer /select,"'+text_output_path+'"'):
        pass
