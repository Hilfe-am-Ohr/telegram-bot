from flask import Flask, request, jsonify
import logging
import os
import re
import telegram
import requests
import utils.database as db
import utils.strings as strings

import telegram_backend.request_management as rm
import telegram_backend.user_management as um
import telegram_backend.data as urls

lang = strings.English()

# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

logging.info("Importing token")
if os.getenv("BOT_TOKEN") is not None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
else:
    try:
        from telegram_backend.secrets import BOT_TOKEN
    except Exception as e:
        print(e)

logging.info(f"Imported token {BOT_TOKEN}")
global bot

bot = telegram.Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(BOT_TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    logging.info(f"got text message : {update}")
    try:
        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8').decode()

        words = text.split()
        if len(words) == 0:
            logging.debug("Empty message!")
            return 'not ok'

        command = words[0]
        if command == '/register':
            um.new_user(bot, text, chat_id, msg_id)
        elif command == '/activate':
            um.change_user_status(bot, text, chat_id, msg_id, "active")
        elif command == '/deactivate':
            um.change_user_status(bot, text, chat_id, msg_id, "inactive")
        elif command == '/quit':
            um.remove_user(bot, text, chat_id, msg_id)
        elif command == '/accept':
            rm.accept_request(bot, text, chat_id, msg_id)
        elif command == '/reject':
            rm.reject_request(bot, text, chat_id, msg_id)
        elif command == '/fulfill':
            rm.fulfill_request(bot, text, chat_id, msg_id)
        elif command == '/help':
            send_help(bot, text, chat_id, msg_id)
        elif command == '/start':
            init_bot(bot, text, chat_id, msg_id)
        else:
            unknown(bot, text, chat_id, msg_id)
        return 'ok'
    except AttributeError:
        return "not okay"

def init_bot(bot, text, chat_id, msg_id):
    init_msg = \
    """
    Welcome! Thank you for helping!

    You can register to help with /register ZIPCODE, or /help to see all the commands
    """
    bot.sendMessage(chat_id=chat_id, text=init_msg)


def send_help(bot, text, chat_id, msg_id):
    help_text = \
    """ Thank you for using the HotVsVirus bot! You can use the following commands:
    /register <ZIP Code>
    \t Register you with your zip code.
    /quit
    \t Exits the program
    /deactivate
    \t Temporarily deactivates requests from the app
    /activate
    \t Reeanables requests from the app
    /help
    \t Shows this message.
    """

    bot.sendMessage(chat_id=chat_id, text=help_text)

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    logging.info("Setting webhook")
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=urls.URL, HOOK=BOT_TOKEN))
    if s:
        logging.info("Setting webhook DONE")
        return "webhook setup ok"
    else:
        logging.info("Setting webhook FAILED")
        return "webhook setup failed"

@app.route('/request_callback', methods=['POST'])
def service_callback():
    json = request.get_json(force=True)
    logging.info(f"Got this message from call back {json}")

    phone_number = json["phone_number"]
    chat_id = json["matched_volunteer_id"]
    request_id = json["id"]

    db.request_DB.add_request(request_id, phone_number, chat_id)
    bot.sendMessage(chat_id=chat_id, text=lang.new_request.format(id_number = request_id))

    return jsonify(json)

@app.route('/')
def index():
    return '.'




# Handle unknown commands
def unknown(bot, text, chat_id, msg_id):
    bot.sendMessage(chat_id=chat_id, text="Sorry, I didn't understand that command. Maybe try /help?")
