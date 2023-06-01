import telebot
import threading
import cv2
import os
import datetime
bot=telebot.TeleBot("6210335951:AAFFb3NdgdQl0OO4VenEuiXqoWa0I7I0I4Y")#token del chat
# idchat=(4546546546)#numero del chat
stop_detector_movimiento = False
@bot.message_handler(commands=["start"])
def cmd_message(message):
    texto = '¡Bienvenido!, Soy un bot que te detecta el movimiento desde tu camára de seguridad\n\n' + '• /Foto - 📷 Recibe una foto.\n\n'+'• /Video - 📹 Recibe un video .\n\n'+'• /Alarma - Activar la cámara de seguridad.'+ '• /Stop - Desactivar la cámara de seguridad.'
    bot.send_message(message.chat.id, texto,parse_mode="html") 
    
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    if message.text.startswith("/Foto"):
        threading.Thread(target=fotografiar, args=(message.chat.id,)).start()
        
    elif message.text.startswith("/Video"):
        threading.Thread(target=video, args=(message.chat.id,)).start()

    elif message.text.startswith("/Alarma"):
        texto = 'Alarma Activada'
        bot.send_message(message.chat.id, texto,parse_mode="html")
        threading.Thread(target=detector_movimiento, args=(message.chat.id,)).start()

    elif message.text.startswith("/Stop"):
        stop_detection()
        bot.send_message(message.chat.id, "Alarma detenida.")
    else:
        texto1 = '¿Qué acción desea realizar?\n\n' + '• /Foto - 📷 Recibe una foto.\n\n'+'• /Video - 📹 Recibe un video .\n\n'+'• /Alarma - Activar la cámara de seguridad.\n\n' + '• /Stop - Desactivar la cámara de seguridad.'
        bot.send_message(message.chat.id, texto1,parse_mode="html")


def recibir_mensajes():
    bot.infinity_polling()

def detector_movimiento(chat_id):
    def detect_motion(frame1, frame2):
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contornos, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contornos
    # def reproducir_mp3(ruta_archivo):
    #     pygame.mixer.init()
    #     pygame.mixer.music.load(ruta_archivo)
    #     pygame.mixer.music.play()

    cap = cv2.VideoCapture(0)
    _, frame1 = cap.read()
    _, frame2 = cap.read()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    global stop_detector_movimiento
    stop_detector_movimiento = False
    while cap.isOpened() and stop_detector_movimiento == False:
        contornos = detect_motion(frame1, frame2)
        for contour in contornos:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 9000:
                continue
            # Si se detectó movimiento
            hora = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            alerta = 'Alerta' + hora + '.avi'
            out = cv2.VideoWriter(alerta, fourcc, 20.0, (640, 480))
            i = 1
            while i < 200:
                cv2.imshow("Motion Detection", frame1)
                frame1 = frame2
                _, frame2 = cap.read()
                out.write(frame1)
                i = i + 1           
            out.release()
            videoa = open(alerta, "rb")
            bot.send_video(chat_id, videoa, caption="Si no estás en casa cuidaico aes")
            videoa.close()
            # os.remove(alerta)
        cv2.imshow("Motion Detection", frame1)
        frame1 = frame2
        _, frame2 = cap.read()

    cap.release()
    cv2.destroyAllWindows()


def fotografiar(chat_id):

    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    # Generar un nombre de archivo único basado en la fecha y hora actual
    hora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    foto = f"foto_{hora}.jpg"
    # Guardar la imagen capturada
    cv2.imwrite(foto, frame)
    # Cerrar la cámara
    cap.release()
    # Enviar la foto al chat correspondiente
    with open(foto, "rb") as foto:
        bot.send_photo(chat_id, foto)
    # Eliminar el archivo de la foto después de enviarla
    os.remove(foto)
    cap.release()
    cv2.destroyAllWindows()
def video(chat_id):
    cap = cv2.VideoCapture(0)
    _, frame1 = cap.read()
    _, frame2 = cap.read()
    
    hora = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = 'VideoActual_'+hora+'.avi'
    out = cv2.VideoWriter(video, fourcc, 20.0, (640, 480))
    i = 1
    while i < 200:
        cv2.imshow("Cam Detector de movimiento", frame1)
        frame1 = frame2
        _, frame2 = cap.read()
        out.write(frame1)
        i = 1 + i 
    cap.release()

    with open(video, "rb") as video:
        bot.send_video(chat_id, video, caption="Video realizado")

    os.remove(video)
    cap.release()
    cv2.destroyAllWindows()
def stop_detection():
        global stop_detector_movimiento
        stop_detector_movimiento = True

if __name__ == '__main__':
    print ('Iniciando el bot')
    hilo_bot = threading.Thread(name ="hilo_bot",target = recibir_mensajes)
    hilo_bot.start()
    print ('Bot iniciado')

