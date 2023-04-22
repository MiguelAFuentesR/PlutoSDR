from gtts import gTTS
import os
import playsound
import ctypes
import locale

# from gtts import lang
# print(lang.tts_langs()) # Test language


def Play_Audio(filename):
    playsound.playsound(filename)

# FUNCION APARTIR DE UNA CADENA DE TEXTO


def Text_Audio(text, language, Voice_filename):
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save(Voice_filename)

# FUNCION APARTIR DE UN ARCHIVO


def FileText_Audio(Read_filename, language, Voice_filename):
    file = open(Read_filename, "r").read().replace("\n", " ")
    speech = gTTS(text=str(file), lang=language, slow=False)
    speech.save(Voice_filename)


def Language_Test():
    language_global = locale.getdefaultlocale()
    language = str(language_global[0])
    system_language = language.lower()
    Language_end = system_language.replace("_", "-")
    return Language_end


#  ------------------- MODULE FUNCTIONS TEST ----------------------

# FileText_Audio("Text.txt", Language_Test(), "Prueba.wav")
# Text_Audio("Bonjuor .... ! Je suis Miguel", 'fr-fr', "Prueba.wav")
# Play_Audio("Prueba.wav")
