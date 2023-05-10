from flask import Flask, request
import telegram
import os
import requests

app = Flask(__name__)

bot = telegram.Bot(token='AAFRX4cn8zsZ9EkJ1BCz8X9zoZg4fxtsh8M')

# Set up webhook (should only be done once)
webhook_url = 'https://maheshdudala.pythonanywhere.com/{}'.format(bot.token)
response = requests.get('https://api.telegram.org/bot{}/deleteWebhook'.format(bot.token))
response = requests.post('https://api.telegram.org/bot{}/setWebhook?url={}'.format(bot.token, webhook_url))

@app.route('/{}'.format(bot.token), methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file_size = update.message.document.file_size
    file_link = bot.get_file(file_id).file_path
    if file_size > 2000000000:
        bot.send_message(chat_id=chat_id, text='File size exceeds 2GB. Cannot convert.')
    else:
        bot.send_message(chat_id=chat_id, text='Converting file. Please wait.')
        link = 'https://api.telegram.org/file/bot{}/{}'.format(bot.token, file_link)
        bot.send_message(chat_id=chat_id, text=link)
    return 'ok'

if __name__ == '__main__':
    app.run()
