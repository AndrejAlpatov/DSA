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

class OperatorOfMensaIntentHandler(AbstractRequestHandler):
    """Handler for OperatorOfMensaIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OperatorOfMensaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text_list = ["Die Mensa wird von dem Studierendenwerk Vorderpfalz betrieben.",
                            "Die Mensa wird von dem Studierendenwerk Vorderpfalz geleitet.",
                            "Das Studierendenwerk Vorderpfalz ist für die Mensa verantwortlich.",
                            "Die Mensa gehört dem Studierendenwerk Vorderpfalz."]

        list_index = randint(0, len(speech_text_list) - 1)

        speech_text = speech_text_list[list_index]

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response