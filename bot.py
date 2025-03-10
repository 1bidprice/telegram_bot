import telebot
from flask import Flask, request
import os

# Διαβάζουμε το TOKEN από τις μεταβλητές περιβάλλοντος για ασφάλεια
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Δημιουργία εφαρμογής Flask για χρήση Webhook
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-render-url.onrender.com/' + TOKEN)
    return 'Webhook Set', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Γεια σου! Το bot λειτουργεί σωστά!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
