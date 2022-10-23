"""Módulo del asistente"""
import json
from os.path import exists
import random
import speech_recognition as sr
import pyttsx3

from src.helpers.image.capture_frame import capture_frame
from src.helpers.config.config_loader import config_loader
from .processors.object_detection.object_detection import object_detection
from .processors.messaging.whatsapp import whatsapp
from .processors.biometric.check_in import check_in
from .processors.website.amazon import amazon
from .processors.website.google_translate import google_translate
from .processors.website.youtube import youtube
from .processors.website.wikipedia import wikipedia
from .processors.website.linkedin import linkedin


class Assistant:
    """La clase asistente es la que contiene la logística principal del código"""
    def __init__ (self, name, phrase_time_limit):
        self.cfg = config_loader("assistant")
        self.name = name
        self.phrase_time_limit = phrase_time_limit
        self.command_list = self._load_json(self.cfg['command_list_path'])
        self.config_path = self.cfg['config_path']
        self._load_speaker(self.config_path)

    def _load_json(self,path):
        with  open(path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)

    def _load_speaker(self, path):
        """
        Esta función extrae el nombre del hablante, si existe, caso contrario
        lo insta a registrarse
        """
        if exists(path):
            self.speaker = self._load_json(path)['speaker']
            self._assistant_speaks("greetings","known_speaker")
        else:
            self._assistant_speaks("greetings","unknown_speaker")
            self.speaker = self._get_audio()
            self._assistant_speaks("greetings","unknown_speaker_register_photo")
            capture_frame(self.cfg['selfie_path'])
            config_file = json.dumps({
                'speaker':self.speaker
            })

            with open(self.config_path, 'w', encoding="utf-8") as file:
                file.write(config_file)
                self._assistant_speaks("greetings","unknown_speaker_registered")

    def _assistant_speaks(self, command, phrases):
        """
        Esta función selecciona aleatoriamente una linea de la lista seleccionada
        tras lo cual reemplaza los nombres del asistente y del hablante respectivamente
        """
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        engine.setProperty('voices',voices[2].id)
        engine.setProperty('rate',140)

        selected_line = random.choice(self.command_list[command]['lines'][phrases])

        if hasattr(self,'speaker'):
            selected_line = selected_line.replace("<speaker>", self.speaker)
        if hasattr(self,'name'):
            selected_line = selected_line.replace("<name>", self.name)

        engine.say(selected_line)
        engine.runAndWait()

    def _get_audio(self):
        """Esta función captura la voz y la convierte a texto"""
        listener = sr.Recognizer()
        text = ''
        while text != 'cancela' or text == '':
            with sr.Microphone() as source:
                print("Habla...")
                audio = listener.listen(source, phrase_time_limit = self.phrase_time_limit)
                print("Stop.")
            try:
                text = listener.recognize_google(audio, language ='es-MX')
                print("Dijiste : ", text)
                return text.lower()
            except:
                self._assistant_speaks("not_understood","main")

    def _get_wakeup(self):
        """Esta función comprueba continuamente que no le hayas hablado al asistente"""
        listener = sr.Recognizer()

        with sr.Microphone() as source:
            print("Habla...")
            audio = listener.listen(source, phrase_time_limit = self.phrase_time_limit)
            print("Stop.")
        try:
            text = listener.recognize_google(audio, language ='es-MX')
            if self.name in text:
                return True
        except:
            pass

        return False

    def _whatsapp(self, url):
        whatsapp(self.command_list["whatsapp"]["lines"]["main_message"][0] + url)
        return True

    def _youtube(self):
        self._assistant_speaks("youtube","main")
        sub_instruction = self._get_audio()
        url = youtube(sub_instruction)
        self._whatsapp(url)
        self._assistant_speaks("youtube","done")
        return True

    def _wikipedia(self):
        self._assistant_speaks("wikipedia","main")
        sub_instruction = self._get_audio()
        url = wikipedia(sub_instruction)
        whatsapp("Te recomiendo que revises esta página web: " + url)
        self._assistant_speaks("wikipedia","done")
        return True

    def _grumpy(self):
        self._assistant_speaks("grumpy","main")
        return True

    def _translate(self):
        self._assistant_speaks("translate","main")
        sub_instruction = self._get_audio()
        google_translate(sub_instruction)
        self._assistant_speaks("translate","done")
        return True

    def _linkedin(self):
        self._assistant_speaks("linkedin","main")
        linkedin()
        self._assistant_speaks("linkedin","done")
        return True

    def _amazon(self):
        self._assistant_speaks("amazon", "main")
        sub_instruction = self._get_audio()
        amazon(sub_instruction)
        self._assistant_speaks("amazon", "done")
        return True

    def _face_id(self):
        self._assistant_speaks("face_id","main")
        sub_instruction = check_in()
        if sub_instruction == "person_in_photo":
            self._assistant_speaks("face_id","done_positive")
        elif sub_instruction == "person_not_in_photo":
            self._assistant_speaks("face_id","done_negative")
        elif sub_instruction == "no_faces_detected":
            self._assistant_speaks("face_id","done_none")
        return True

    def _object_recognition(self):
        self._assistant_speaks("object_recognition","main")
        object_detection()
        self._assistant_speaks("object_recognition","done")
        return True

    def _exit(self):
        self._assistant_speaks("exit","main")
        return False

    def _default(self):
        self._assistant_speaks("default","main")
        return True

    def _random_greetings(self):
        self._assistant_speaks("random_greetings","main")
        return True

    def _selector(self, issued_keyphrase):
        """
        Esta función luce algo compleja pero es sencilla en realidad, itera sobre
        de la lista de comandos buscando si la frase de comando recibida existe dentro de alguno de los
        métodos, si existe, extrae de la clave del comando el nombre del método correcto y lo manda a
        llamar dinámicamente, si la frase no existe, retorna el default
        """
        # Cree una pequeña función para poder interrumpir el loop en cuanto se encuentre una coincidencia
        def _search_for_command():
            for key, command in self.command_list.items():
                for keyphrase in command['keyphrases']:
                    if keyphrase in issued_keyphrase:
                        return "_" + key
            return "_default"

        method_name = _search_for_command()
        method = getattr(self, method_name)
        return method()

    def main(self):
        """Función principal que activa al asistente"""
        active = True
        while active:
            if self._get_wakeup():
                self._assistant_speaks("main","activated")
                instruccion = self._get_audio()
                active = self._selector(instruccion)
