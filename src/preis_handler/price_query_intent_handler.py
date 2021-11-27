from flask import Flask
from pymongo import MongoClient
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access

class PriceQueryIntentHandler(AbstractRequestHandler):
    """Handler for PriceQueryIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PriceQueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        # Get DB collections
        list_with_collections = data_bank_access(['answers_stud_werk'])
        db_collection_answers = list_with_collections[0]

        # Get documents from collections
        answers = db_collection_answers.find_one({})

        # List of all answers
        speech_text_list = answers['OPERATOR_OF_MENSA']

        # Select random answer
        list_index = randint(0, len(speech_text_list) - 1)
        speech_text = speech_text_list[list_index]

        # Select reprompt
        reprompt = answers['OPERATOR_OF_MENSA_REPROMPT']
        """

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        day = slots['day_price'].value
        membership = slots['membership_price'].value
        timeindication = slots['timeindication_price'].value

        # No slot given -> start the price query session
        if day is None and membership is None and timeindication is None:
            speech_text = "Es gibt verschiedene Preise. Bist du Student oder Gast?"

        # day_price between montag and freitag -> price everyday the same
        elif day == "montag" or day == "dienstag" or day == "mittwoch" or day == "donnerstag" or day == "freitag":
            speech_text = "Die Preise für das Essen sind jeden Tag gleich. Bist du Student oder Gast?"

        # day_price samstag or sonntag -> no food at weekend
        elif day == "samstag" or day == "sonntag" or day == "wochenende":
            speech_text = "Am Wochenende wird kein Essen ausgegeben."

        # membership_price student or studenten or studentin or studentinnen -> 3 euro
        elif membership == "student" or membership == "studenten" or membership == "studentin" or membership == "studentinnen":
            speech_text = "Für Studenten und Studentinnen kostet das Essen insgesamt drei Euro."

        # membership_price gast or gäste -> 5 euro
        elif membership == "gast" or membership == "gäste":
            speech_text = "Für Gäste kostet das Essen insgesamt fünf Euro."

        # any timeindication
        elif timeindication is not None:
            speech_text = "Die Preise für das Essen sind jeden Tag gleich. Bist du Student oder Gast?"

        # something went wrong
        else:
            speech_text = "Etwas ist bei der Preisabfrage schief gelaufen!"

        reprompt = speech_text

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response