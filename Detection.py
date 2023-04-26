# STEP 1: Modulos Necesarios

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from Visualizacion import *
from googletrans import Translator
import cv2
import time
inicio = time.time()


def traducir(Text, lenguage):
    translater = Translator()
    out = translater.translate(Text, dest=lenguage)
    return out


def Object_Detection(parameters):
    Image_file = parameters['Img_path']
    model = parameters['Model']

    # cv2.imshow('Imagen', img)
    VisionRunningMode = mp.tasks.vision.RunningMode
    BaseOptions = mp.tasks.BaseOptions
    ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
    ObjectDetector = mp.tasks.vision.ObjectDetector

    options = ObjectDetectorOptions(
        base_options=BaseOptions(model_asset_path=model),
        score_threshold=parameters['score_threshold'],
        max_results=parameters['max_results'],
        running_mode=VisionRunningMode.IMAGE)

    detector = ObjectDetector.create_from_options(options)

    # 3: Cargar la imagen.
    image = mp.Image.create_from_file(Image_file)

    # 4: Detectar objetos en la imagen.
    detection_result = detector.detect(image)

    # 5:  Procesos para el procesamiento de los resultados (Almacenar ultima Imagen Procesada)
    image_copy = np.copy(image.numpy_view())
    annotated_image = visualize(image_copy, detection_result)
    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('Deteccion.jpeg', rgb_annotated_image)
    # cv2.imshow('Ventana', rgb_annotated_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return detection_result


def Processing_Detection(parameters):
    Info_Detection = Object_Detection(parameters)
    # print(Info_Detection)

    # Lista con cada uno de los elementos detectados
    Resultado = Info_Detection.detections

    # Cada elemento detectado posee una serie de caracteristicas :
    '''
    BoundingBox : Contiene la informacion de la posicion del objeto detectado:
                    origin_x : Posicion Inicial en X dentro de la Imagen
                    origin_y : Posicion Inicial en y dentro de la Imagen
                    width    : Ancho del objeto detectado
                    height   : Alto del objeto detectado
    categories :  Contiene la informacion del tipo de objeto detectado:
                    index
                    score
                    display_name
                    category_name

    Se crea una lista que tendra todos los elementos, en dicha lista se tendran diccionarios
    que almacenaran las caracteristicas de cada objeto
    '''
    # Para el almacenamiento de los resultados :
    Clasificaciones = []
    for x in range(len(Resultado)):
        # Creacion de un diccionario para Elemento :
        Bounding_Box = Resultado[x].bounding_box
        Categories = Resultado[x].categories
        if Categories[0].category_name == "tv":
            Categories[0].category_name = "screen"
        Elemento = dict(
            score=Categories[0].score,
            category_name=Categories[0].category_name,
            origin_x=Bounding_Box.origin_x,
            fin_x=Bounding_Box.origin_x + Bounding_Box.width,
            origin_y=Bounding_Box.origin_y,
            fin_y=Bounding_Box.origin_x + Bounding_Box.height,
            width=Bounding_Box.width,
            height=Bounding_Box.height)

        Clasificaciones.append(Elemento)
        # print(Elemento)

    Imagen_Data = Zone_Clasificator(Clasificaciones, parameters)
    Informacion = [Imagen_Data, Clasificaciones]
    return Informacion


def Zone_Clasificator(Clasificaciones, parameters):
    # 1. Determinar el tamaño total de la Imagen
    img = cv2.imread(parameters['Img_path'])
    height, width, channel = img.shape

    Data = dict(
        Dim_x=width,
        Dim_y=height,
        Canal=channel
    )

    # print("Region1 entre "+str(0)+" y " + str(int(width/3)))
    # print("Region2 entre "+str(int(width/3))+" y " + str(int(2*width/3)))
    # print("Region3 entre "+str(int(2*width/3))+" y " + str(int(width)))
    # 2.  Seccionamiento por 3 regiones :

    for x in range(len(Clasificaciones)):
        # Comprobar si esta en la izquierda
        dicc = Clasificaciones[x]

        if (dicc["origin_x"] < int(width/3)) and (dicc["fin_x"] < int(width/3)):
            # print("El "+dicc[x]["category_name"]+" Esta a la izquierda")
            # print(str(dicc[x]["origin_x"]) +"  "+str(dicc[x]["fin_x"]))
            Sentido = "Izquierda"
        # Comprobar si esta en la derecha
        elif (dicc["origin_x"] > int(2*width/3)) and (dicc["fin_x"] < width):
            # print("El "+dicc[x]["category_name"]+" Esta a la derecha")
            # print(str(dicc[x]["origin_x"]) +"  "+str(dicc[x]["fin_x"]))
            Sentido = "Derecha"
        else:
            # Comprobar si esta en la región central
            # print("El "+dicc[x]["category_name"]+" Esta en el centro")
            # print(str(dicc[x]["origin_x"]) +"  "+str(dicc[x]["fin_x"]))
            Sentido = "Frente"

        dicc.update({'Ubicacion': Sentido})
    return Data


def Distance_Estimation(Clasificator, Data_Img):

    for x in range(len(Clasificator)):
        dicc = Clasificator[x]
        width = dicc["width"]
        height = dicc["height"]
        Relacion = width/Data_Img["Dim_x"]
        # Distancia Estimada en Pulgadas :
        distance = ((2*3.14*180)/(width+height*360))*1000 + 3
        print("La relacion es de : " + str(Relacion))
        print("Dimensiones objeto  : "+str(width)+" Alto :"+str(height))
        print("Se tiene una distancia en in  : "+str(distance))
        # Distancia Estimada en mts :
        distance_m = distance/39.37
        print("Se tiene una distancia de : "+str(distance_m))


def Traducir_Salidas(Clasificator, languague):
    for x in range(len(Clasificator)):
        dicc = Clasificator[x]
        texto = traducir(dicc["category_name"], languague).text
        dicc["category_name"] = texto


# --------------------- TEST ZONE -------------------------------
'''
parameters = dict(
    score_threshold=0.48,
    max_results=3,
    Img_path='calle_2.jpg',
    Model='models/efficientdet_lite2_uint8.tflite'
)

Clasificator = Processing_Detection(parameters)
# print(Clasificator)
Traducir_Salidas(Clasificator, "es")
# print(Clasificator)
message = Message(Clasificator)
print(message)
fin = time.time()
print(fin-inicio)

'''
