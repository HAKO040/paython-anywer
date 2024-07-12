import telebot
import requests

ap = 'https://pythonanywhere.os74.repl.co'
tok= input("bot token: ")
bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def send_data_from_api(message):
    bot.send_message(message.chat.id, "جاري البدء")
    response = requests.get(ap)
    bot.send_message(message.chat.id, response.text)
    
bot.infinity_polling()