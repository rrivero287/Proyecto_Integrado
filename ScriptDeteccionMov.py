# import cv2
# import os
# import datetime

# def detect_motion(frame1, frame2):
#     diff = cv2.absdiff(frame1, frame2)
#     gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#     dilated = cv2.dilate(thresh, None, iterations=3)
#     contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     return contours

# cap = cv2.VideoCapture(0)
# _, frame1 = cap.read()
# _, frame2 = cap.read()
# fourcc = cv2.VideoWriter_fourcc(*'XVID')

# start_time = None
# recording = False
# while cap.isOpened():
#     contours = detect_motion(frame1, frame2)
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         if cv2.contourArea(contour) < 9000:
#             continue
#         cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
#         # Si se detectó movimiento
#         if not recording:
#             # Si no se estaba grabando, comenzar la grabación
#             start_time = datetime.datetime.now()
#             recording = True
#             hora = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#             output = 'Alerta' + hora + '.avi'
#             out = cv2.VideoWriter(output, fourcc, 20.0, (640, 480))
#         i = 1
#         while i < 200:
#             cv2.imshow("Motion Detection", frame1)
#             frame1 = frame2
#             _, frame2 = cap.read()
#             out.write(frame1)
#             i = i + 1 
#         elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
 
#         # if elapsed_time <= 10:
#         #     # Si el tiempo transcurrido es menor o igual a 10 segundos, escribir el fotograma en el video
#         #     out.write(frame1)
#         #     i = i +1
#         #     print (i)
#         # else:
#             # Si el tiempo transcurrido es mayor a 10 segundos, detener la grabación y liberar el objeto VideoWriter
#         recording = False
#         out.release()

#     cv2.imshow("Motion Detection", frame1)
#     frame1 = frame2
#     _, frame2 = cap.read()

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
        # if not recording:
        #     start_time = datetime.datetime.now()
        #     recording = True
        # elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        # if elapsed_time < 15:
        #     out.write(frame1)
        # else:
        #     recording = False
        #     out.release()
        #     out = cv2.VideoWriter('alerta.avi', fourcc, 20.0, (640, 480))

#     cv2.imshow("Motion Detection", frame1)
#     frame1 = frame2
#     _, frame2 = cap.read()

#     if contours:
#         cv2.imwrite('motion_detected.jpg', frame1)

#     if cv2.waitKey(1) & 0xFF == ord('w'):
#         current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         file_name = f"{current_time}.jpg"
#         cv2.imwrite(file_name, frame1)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# out.release()
# cv2.destroyAllWindows()

# Importar los módulos necesarios
import cv2
import datetime
import os

# Abrir la cámara para capturar el video
cap = cv2.VideoCapture(0)
# Leer los primeros dos frames
_, frame1 = cap.read()
_, frame2 = cap.read()

# Configurar el formato del video de salida
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Variable para controlar la grabación
recording = False

# Bucle principal para la detección de movimiento
while cap.isOpened():
    # Detectar contornos de movimiento en los frames
    contours = detect_motion(frame1, frame2)
    
    # Iterar sobre los contornos detectados
    for contour in contours:
        # Obtener las coordenadas y dimensiones del contorno
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # Descartar contornos pequeños
        if cv2.contourArea(contour) < 9000:
        
            # Dibujar un rectángulo alrededor del contorno en el frame actual
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Generar un nombre de archivo para el video de salida
            hora = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output = 'Alerta' + hora + '.avi'        
            # Crear un objeto VideoWriter para escribir el video de salida
            out = cv2.VideoWriter(output, fourcc, 20.0, (640, 480))
        
            # Grabar 200 frames
            i = 1
            while i < 200:
                # Mostrar el frame actual en una ventana
                cv2.imshow("Motion Detection", frame1)       
                # Actualizar los frames
                frame1 = frame2
                _, frame2 = cap.read()  
                # Escribir el frame en el video de salida
                out.write(frame1)
                i += 1
        
            # Finalizar la grabación y liberar los recursos
            recording = False
            out.release()
            os.remove(output)
    
    # Mostrar el frame actual en una ventana
    cv2.imshow("Motion Detection", frame1)
    
    # Actualizar los frames
    frame1 = frame2
    _, frame2 = cap.read()

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
