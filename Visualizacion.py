import cv2
import numpy as np
import os
MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red

wd = os.getcwd()
print("working directory is ", wd)


def Crear_Archivo():
    global file
    file = open("Text.txt", "w")
    # file.write("Te doy la Bienvenida al Sistema de detección automática de objetos :"+"\n")
    # file.write(latex(""))


def Escribir_Archivo(cadena):
    file.write(cadena)


def Cerrar_Archivo():
    file.write("Espero te sirviera mi ayuda")
    file.close()


def visualize(
    image,
    detection_result
) -> np.ndarray:

    for detection in detection_result.detections:
        # Dibujando un cuadro para el objeto detectado
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        # Dibujando un elemento para indicar el score y nombre de la detección
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x,
                         MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image


def Message(Clasificator):
    Estruc_1 = " Tienes un "
    Estruc_2 = " Tienes una "
    Con_1 = " a tu "
    Con_2 = " al "
    Con_3 = " apróximadamente  a "
    Dist = 0
    Con_4 = " metros "
    mensaje = []
    for x in range(len(Clasificator)):
        dicc = Clasificator[x]
        Clase = dicc["category_name"]
        Ubic = dicc["Ubicacion"]
        if Ubic == "Frente":

            if Clase[-1] == "a":
                Mensaje = Estruc_2 + Clase + Con_2 + \
                    Ubic + Con_3 + str(Dist) + Con_4
                # print("Femenino  :" + Clase)
            else:
                Mensaje = Estruc_1 + Clase + Con_2 + \
                    Ubic + Con_3 + str(Dist) + Con_4
                # print("Masculino :" + Clase)
        else:
            if Clase[-1] == "a":
                Mensaje = Estruc_2 + Clase + Con_1 + \
                    Ubic + Con_3 + str(Dist) + Con_4
                # print("Femenino  :" + Clase)
            else:
                Mensaje = Estruc_1 + Clase + Con_1 + \
                    Ubic + Con_3 + str(Dist) + Con_4
        mensaje.append(Mensaje)
    # print(mensaje)

    return mensaje
