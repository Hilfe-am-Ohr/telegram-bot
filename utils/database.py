#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Lucas Costa Campos <rmk236@gmail.com>
#
# Distributed under terms of the MIT license.

from enum import Enum
import logging

# Add logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
class Request(object):

    """Docstring for Request. """

    def __init__(self, id_number, phone_number, assigned_chat):
        """TODO: to be defined.

        :phone_number: TODO
        :zip_code: TODO
        :id_number: TODO

        """
        self.id_number = id_number
        self.phone_number = phone_number
        self.assigned_chat = assigned_chat
        self.status = "OPEN"


class Requests(object):

    """Docstring for Requests. """

    def __init__(self):
        """TODO: to be defined. """
        self.requests = []

    def add_request(self, id_number, phone_number, volunteer_id):
        new_request = Request(id_number, phone_number, volunteer_id)
        self.requests.append(new_request)

    def check_user_asignment(self, request_id, chat_id):
        chat_id = str(chat_id)
        logging.info(f"Trying to find matching {request_id} and {chat_id} of types {type(request_id)} and {type(chat_id)}")
        for request in self.requests:
            logging.info(f"Matching with {request.id_number} and {request.assigned_chat} with types  {type(request.id_number)} and {type(request.assigned_chat)}")
            if request.assigned_chat == chat_id and request.id_number == request_id:
                logging.info("Found match!")
                return True
        logging.info("Match not found!")
        return False

    def get_request_with_id(self, request_id):
        logging.info(f"Looking for ID {request_id}")
        for request in self.requests:
            if request.id_number == request_id:
                logging.info("Found ID!")
                return request
        logging.info("ID not found!")
        # return [request for request in self.requests if request.id_number == request_id][0]

    def delete_id(self, request_id):
        logging.info(f"Looking for ID {request_id}")
        for idx, request in enumerate(self.requests):
            if request.id_number == request_id:
                break
        self.requests.pop(idx)


    def mark_request(self, request_id, status):
        for idx, request in enumerate(self.requests):
            if request.id_number == request_id:
                self.requests[idx].status = status

request_DB = Requests()
