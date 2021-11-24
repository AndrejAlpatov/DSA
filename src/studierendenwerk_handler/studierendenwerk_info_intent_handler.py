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

class StudierendenwerkInfoIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkInfoIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text = "Das Studierendenwerk Vorderpfalz ist eine rechtsfähige Anstalt des öffentlichen Rechts. " \
                      "Ich kann dir Informationen zu den Themen und Aktivitäten oder anderen Standorten " \
                      "von Mensen und Cafeterien mitteilen."
        reprompt = "Sage zum Beispiel \"Was macht das Studierendenwerk Vorderpfalz?\""

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response