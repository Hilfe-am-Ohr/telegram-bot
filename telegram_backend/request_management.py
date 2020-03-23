import logging
import os
import re
import telegram
import requests
import utils.database as db
import utils.strings as strings

import telegram_backend.data as urls

lang = strings.English()
# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

def accept_request(bot, text, chat_id, msg_id):

    logging.info("User accepted request")
    words = text.split()
    if len(words) <= 1:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_accept_request_missing)
        return

    request_id = words[1]

    data = {
        "api_key": "telegram",
        "action": "accept"
    }

    if db.request_DB.check_user_asignment(request_id, chat_id):
        request = db.request_DB.get_request_with_id(request_id)
        bot.sendMessage(chat_id=chat_id, text=lang.callback_accept_request_success.format(phone_number = request.phone_number))
        url = f"{urls.db_link}/help_requests/{request_id}"
        logging.info(f"Setting request as accepted on URL: {url}")
        requests.put(url, data=data)
    else:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_accept_request_error)


def fulfill_request(bot, text, chat_id, msg_id):

    logging.info("User fulfilled request")
    words = text.split()
    if len(words) <= 1:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_fulfill_request_missing)
        return

    request_id = words[1]

    data = {
        "api_key": "telegram",
        "action": "fulfill"
    }

    if db.request_DB.check_user_asignment(request_id, chat_id):
        request = db.request_DB.get_request_with_id(request_id)
        bot.sendMessage(chat_id=chat_id, text=lang.callback_fulfill_request_success)
        logging.info("Setting request as fulfilled")
        url = f"{urls.db_link}/help_requests/{request_id}"
        logging.info(f"Setting fulfilled as accepted on URL: {url}")
        requests.put(url, data=data)
        db.request_DB.delete_id(request_id)
    else:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_fulfill_request_error)

def reject_request(bot, text, chat_id, msg_id):

    logging.info("Request rejected!")
    words = text.split()
    if len(words) <= 1:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_reject_request_missing)
        return

    data = {
        "api_key": "telegram",
        "action": "reject"
    }

    request_id = words[1]
    if db.request_DB.check_user_asignment(request_id, chat_id):
        request = db.request_DB.get_request_with_id(request_id)
        bot.sendMessage(chat_id=chat_id, text=lang.callback_reject_request_success)
        logging.info("Reopening request")
        url = f"{urls.db_link}/help_requests/{request_id}"
        logging.info(f"Setting rejected as accepted on URL: {url}")
        requests.put(url, data=data)
        db.request_DB.delete_id(request_id)
    else:
        bot.sendMessage(chat_id=chat_id, text=lang.callback_reject_request_error)
