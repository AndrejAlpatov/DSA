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

class PriceQuerySessionIntentHandler(AbstractRequestHandler):
    """Handler for PriceQuerySessionIntent."""

    def deactivate_session(self, db_collection_session):
        db_collection_session.update_one({"SESSION_ACTIVE": True}, {"$set": {"SESSION_ACTIVE": False}})

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PriceQuerySessionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get DB collections
        list_with_collections = data_bank_access(['sessions_price', 'answers_price'])
        db_collection_session = list_with_collections[0]
        db_collection_answers = list_with_collections[1]

        # Get documents from collections
        session_answers = db_collection_session.find_one({})
        answers = db_collection_answers.find_one({})

        # Get status of session
        session_status = session_answers['SESSION_ACTIVE']

        # check if the session is active
        if session_status == False:
            speech_text = "Die Session ist nicht aktiv."
            handler_input.response_builder.speak(speech_text).ask(speech_text)
            return handler_input.response_builder.response

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        membership = slots['membership_price_session'].value

        # membership student or studenten or studentin or studentinnen -> 3 euro
        if membership == "student" or membership == "studenten" or membership == "studentin" or membership == "studentinnen":
            # select answer
            speech_text = answers['STUDENT_ANSWER']

        #membership gast or gäste -> 5 euro
        elif membership == "gast" or membership == "gäste":
            speech_text = answers['GAST_ANSWER']

        # something went wrong
        else:
            speech_text = "Tut mir leid, aber diese Angehörigkeit gibt es nicht."

        # deactivate session before returning
        self.deactivate_session(db_collection_session)

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response