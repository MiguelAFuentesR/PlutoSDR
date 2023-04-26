import os
import Audio_Translate as audio
import Detection as detection
import Distance as dist
from Visualizacion import *
import time
inicio = time.time()
wd = os.getcwd()

# ---------------- TEST -----------

# Path = wd+"/Calibration_Frames/"
parameters = dict(
    score_threshold=0.4,
    max_results=5,
    # Img_path='Calibration_Frames/IMG_0001.jpg',
    Img_path='test.jpeg',
    Model='models/efficientdet_lite2_uint8.tflite'
)
# print(Path+'IMG_0000.jpg')

Informacion = detection.Processing_Detection(parameters)
Data_Img = Informacion[0]
print(Data_Img)
Clasificator = Informacion[1]
detection.Traducir_Salidas(Clasificator, "es")
message = Message(Clasificator)

detection.Distance_Estimation(Clasificator, Data_Img)


Crear_Archivo()
for x in range(len(message)):
    Escribir_Archivo(message[x]+". ")
Cerrar_Archivo()

# --------------- Distance -------------

# dist.Focal_lenght(wd, 30)
#
# audio.FileText_Audio("Inicio.txt", audio.Language_Test(), "Bienvenida.wav")
audio.FileText_Audio("Text.txt", audio.Language_Test(), "Prueba.wav")
fin = time.time()
print(Clasificator)
print(fin-inicio)

# audio.Play_Audio("Bienvenida.wav")
# audio.Play_Audio("Prueba.wav")
