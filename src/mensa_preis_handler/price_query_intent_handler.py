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

    def activate_session(self, db_collection_session, user_id):
        # if this user has a session document
        if db_collection_session.count_documents({"USER_ID": user_id}) > 0:
            # set the SESSION_ACTICE to true, where the USER_ID is user_id
            db_collection_session.update_one({"USER_ID": user_id}, {"$set": {"SESSION_ACTIVE": True}})

        # otherwise create a session document
        else:
            session_doc = {
                "USER_ID": user_id,
                "SESSION_ACTIVE": True
            }
            db_collection_session.insert_one(session_doc)

    def deactivate_session(self, db_collection_session, user_id):
        # set the SESSION_ACTIVE to false, where the USER_ID is user_id
        db_collection_session.update_one({"USER_ID": user_id}, {"$set": {"SESSION_ACTIVE": False}})

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PriceQueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # get user id
        user_id = handler_input.request_envelope.context.system.user.user_id

        # Get DB collections
        list_with_collections = data_bank_access(['sessions_mensa_price', 'answers_mensa_price'])
        db_collection_session = list_with_collections[0]
        db_collection_answers = list_with_collections[1]

        # deactivate session if existing
        self.deactivate_session(db_collection_session, user_id)

        # Get documents from collections
        answers = db_collection_answers.find_one({})

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        day = slots['day_price'].value
        membership = slots['membership_price'].value
        timeindication = slots['timeindication_price'].value
        num_days = slots['num_days'].value

        # No slot given -> activate the price query session
        if day is None and membership is None and timeindication is None and num_days is None:
            # Select answer
            speech_text = answers['STD_ANSWER']
            # activate session
            self.activate_session(db_collection_session, user_id)

        # if any value for num_days is given
        elif num_days is not None:
            speech_text = answers['NUM_DAYS_ANSWER']
            self.activate_session(db_collection_session, user_id)

        # day_price between montag and freitag -> price everyday the same and activate the price query session
        elif day == "montag" or day == "dienstag" or day == "mittwoch" or day == "donnerstag" or day == "freitag":
            speech_text = answers['NUM_DAYS_ANSWER']
            self.activate_session(db_collection_session, user_id)

        # day_price samstag or sonntag -> no food at weekend
        elif day == "samstag" or day == "sonntag" or day == "wochenende":
            speech_text = answers['WEEKEND_ANSWER']

        # membership_price student or studenten or studentin or studentinnen -> 3 euro
        elif membership == "student" or membership == "studenten" or membership == "studentin" or membership == "studentinnen":
            speech_text = answers['STUDENT_ANSWER']

        # membership_price gast or gäste -> 5 euro
        elif membership == "gast" or membership == "gäste":
            speech_text = answers['GAST_ANSWER']

        # any timeindication -> activate the price query session
        elif timeindication is not None:
            speech_text = answers['TIMEINDIC_ANSWER']
            self.activate_session(db_collection_session, user_id)

        # something went wrong
        else:
            speech_text = "Die Preisabfrage ist leider schiefgelaufen."

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
