import logging
import os
import re
import telegram
import requests
import utils.database as db
import utils.strings as strings

import telegram_backend.data as urls

lang = strings.English()
identify_zip_code = re.compile("(?!01000|99999)(0[1-9]\d{3}|[1-9]\d{4})")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

def new_user(bot, text, chat_id, msg_id):

    logging.info("Trying to register new user")
    words = text.split()
    if len(words) <= 1:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_new_user_missing_zip)
        return

    zip_code = words[1]

    match = identify_zip_code.match(zip_code)
    if match is not None:
        logging.info(f"Added user with ZIP code {zip_code} and chat_id {chat_id}")
        data = {
            "id_at_source": chat_id,
            "postal_code": zip_code,
            "api_key": "telegram",
            "status": "active"
        }
        url = f"{urls.db_link}/volunteers"
        logging.info(f"Registering user at {url}")
        r = requests.post(url, data = data)
        bot.sendMessage(chat_id=chat_id, text=lang.callback_new_user_success.format(zip_code=zip_code))
    else:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_new_user_error)

def change_user_status(bot, text, chat_id, msg_id, new_status):

    logging.info("Trying make user {chat_id} {new_status}")
    data = {
        "status": new_status,
        "api_key" : "telegram"
    }
    url = f"{urls.db_link}/volunteers/{chat_id}"
    logging.info(f"Changing status at {url}")
    r = requests.put(url, data = data)
    bot.sendMessage(chat_id=chat_id, text=lang.callback_change_status_success.format(new_status=new_status))

def remove_user(bot, text, chat_id, msg_id):

    logging.info("Trying remove user {chat_id}")

    url = f"{urls.db_link}/volunteers/{chat_id}"
    data = {
        "api_key" : "telegram"
    }
    logging.info(f"Changing status at {url}")
    r = requests.delete(url, data=data)
    bot.sendMessage(chat_id=chat_id, text=lang.callback_remove_user_success)

