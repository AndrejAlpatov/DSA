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

class OperatorOfMensaIntentHandler(AbstractRequestHandler):
    """Handler for OperatorOfMensaIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OperatorOfMensaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response


        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response