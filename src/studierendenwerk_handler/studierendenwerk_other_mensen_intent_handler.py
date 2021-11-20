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

class StudierendenwerkOtherMensenIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkOtherMensenIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkOtherMensenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Liste möglicher Antworten
        speech_text_list = ["Das Studierendenwerk ist nicht nur in Worms tätig. Es betreut auch "
                            "Mensen in Landau, Ludwigshafen, Germersheim, in den Weinbergen um "
                            "Neustadt an der Weinstraße und eine mobile Mensa, welche Currywurst "
                            "verkauft.",
                            "Das Studierendenwerk Vorderpfalz betreut mehrere Mensen und Cafeterien "
                            "bei den Standorten Landau, Ludwigshafen, Worms, Germersheim, in den Weinbergen "
                            "um Neustadt an der Weinstraße und eine mobile Mensa, welche an verschiedenen "
                            "Orten sein kann.",
                            "Das Studierendenwerk Vorderpfalz betreut insgesamt sieben Mensen und "
                            "Cafeterien. Zwei in Landau, zwei in Ludwigshafen, eine in Worms, "
                            "eine in Germersheim und eine in den Weinbergen um Neustadt an der Weinstraße."]

        list_index = randint(0, len(speech_text_list) - 1)

        # zufällige Antwort ausgeben
        speech_text = speech_text_list[list_index]
        reprompt = "Wenn du wissen willst, was das Studierendenwerk noch macht, sage \"Mit was " \
                   "beschäftigt sich das Studierendenwerk Vorderpfalz noch?\""

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response