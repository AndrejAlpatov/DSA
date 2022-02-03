from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access

class OperatorOfMensaIntentHandler(AbstractRequestHandler):
    """Handler for OperatorOfMensaIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OperatorOfMensaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

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

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response