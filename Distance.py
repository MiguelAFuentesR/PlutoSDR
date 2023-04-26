import numpy as np
import cv2
import time
import os
import Detection as detection

# Video Calibrationimport cv2


def Capture_Video_Calibration(Path):

    # The duration in seconds of the video captured
    capture_duration = 5
    captura = cv2.VideoCapture(0)
    ret, im = captura.read()
    h, w, _ = im.shape
    fps = 20
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    filename = Path+'/Calibration_Frames/calibracion.mp4'

    salida = cv2.VideoWriter(filename, codec, fps, (w, h))
    start_time = time.time()

    while (int(time.time() - start_time) < capture_duration):
        ret, im = captura.read()
        if ret == True:
            salida.write(im)
            cv2.imshow('Video', im)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    captura.release()
    salida.release()
    cv2.destroyAllWindows()


def Frames_Calibration(Path):
    capture = cv2. VideoCapture(Path+'/Calibration_Frames/calibracion.mp4')
    path = Path+"/Calibration_Frames/"
    cont = 0
    while (capture. isOpened()):
        ret, frame = capture. read()
        if (ret == True):
            cv2.imwrite(path+'IMG_%04d.jpg' % cont, frame)
            cont += 1
            if (cv2.waitKey(1) == ord('s')):
                break
        else:
            break
    capture. release()
    cv2.destroyAllWindows()
    print("Existen "+str(cont)+" Frames")
    return cont


def Focal_lenght(Img_path, Object_parameters):

    # Estimar la distancia Focal de los frames obtenidos
    # Para estimar la distancia primero se requiere Identificar el objeto de calibracion
    # El objeto de calibracion es una hoja de 10 cm x 10 cm ,Situar el objeto a una distancia de 30 cm
    d = Object_parameters[0]  # Distancia cm
    W = Object_parameters[1]  # Object_width cm
    Object_height = Object_parameters[2]  # cm

    Muestras = Frames_Calibration(Img_path)
    Focales = []
    for i in range(Muestras):
        Ubi = "Calibration_Frames/" + 'IMG_%04d.jpg' % i
        # print(Ubi)
        parameters = dict(
            score_threshold=0.5,
            max_results=1,
            Img_path=Ubi,
            Model='models/efficientdet_lite2_uint8.tflite'
        )
        Informacion = detection.Processing_Detection(parameters)
        Clasificator = Informacion[1]

        for x in range(len(Clasificator)):
            # Comprobar si esta en la izquierda
            dicc = Clasificator[x]
            width = dicc["width"]
            Focal = (width*d)/W
            Focales.append(Focal)

    Focales.insert(0, np.mean(Focales))

    with open("Calibracion.txt", 'w') as f:
        for i in Focales:
            f.write(str(i)+"\n")

    return Focales


def Calculo_Distancia():
    with open("Calibracion.txt", "r") as archivo:
        focal_lenght = archivo.readline(10)
    print(focal_lenght)
    # d = W * focal_lenght / w


# ------------------- TEST ZONE ----------------
wd = os.getcwd()
# print("working directory is ", wd)
# Capture_Video_Calibration(wd)
# Frames_Calibration(wd)

# Focal = Focal_lenght(wd, [20, 11, 5.5])  # Distancia, width, height
# Calculo_Distancia()
