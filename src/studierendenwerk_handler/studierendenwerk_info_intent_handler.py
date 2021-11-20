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

class StudierendenwerkInfoIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkInfoIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text_list = []
        speech_text = ""
        reprompt = ""

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response