import telebot
import threading
bot=telebot.TeleBot("TokenhttpAPI")#token del chat
idchat=(4546546546)#numero del chat

@bot.message_handler(commands=["start"])
def cmd_message(message):
    texto = 'Bienvenido, que acción desea realizar:' + '\n' + '<b>/foto</b>' + '\n' + '<b>/video</b>'
	bot.send_message(message.chat.id, texto,parse_mode="html")
@bot.message_handler(content_types=["text"]) "lo que queremos que devuelva
def bot_mensajes_texto(message):
	if message.text.startswith("/foto"):
        foto = open("rutafoto","rb")
		bot.send_photo(message.chat.id, foto , caption="Foto realizada")
	else if message.text.startswith("/video"):	
		video = open("rutavideo","rb")
		bot.send_video(message.chat.id, video , caption="Video realizado")
def recibir_mensajes():
    bot.infinity_polling() 

if __name__ == '__main__':
    print ('Iniciando el bot')
    hilo_bot = threading.Thread(name ="hilo_bot",target = recibir_mensajes)
    print('Fin'   )