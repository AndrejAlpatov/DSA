""" This module contains the handler for the OwnCupInKioskHandler """

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access


class OwnCupInKioskHandler(AbstractRequestHandler):
    """ Handler for OwnCupInKioskHandler """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OwnCupInKiosk")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method answers the question if it's allowed to bring a own cup into the mensa.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (no slot values)

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get DB collections
        list_with_collections = data_bank_access(['answers'])
        db_collection_answers = list_with_collections[0]

        answers = db_collection_answers.find_one({})
        speech_text_list = answers['IF_OWN_CUP_IN_KIOSK']

        # Zufällige Antwortauswahl aus der Liste
        list_index = randint(0, len(speech_text_list) - 1)
        speech_text = speech_text_list[list_index]

        # Output
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
