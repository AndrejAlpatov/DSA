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
from src.data_bank_functions.output_of_all_collections import data_bank_access

class StudierendenwerkInfoIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkInfoIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get DB collections
        list_with_collections = data_bank_access(['answers_stud_werk'])
        db_collection_answers = list_with_collections[0]

        # Get documents from collections
        answers = db_collection_answers.find_one({})

        # Select answer
        speech_text = answers['INFO_STUD_WERK']

        # Select reprompt
        reprompt = answers['INFO_STUD_WERK_REPROMPT']

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response