from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access


class IsThereQuestionsHandler(AbstractRequestHandler):
    """Handler um auf die Verfügbarkeit des Kaffeeautomaten zu antworten"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("IsThereQuestions")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get DB collections
        list_with_collections = data_bank_access(['answers'])
        db_collection_answers = list_with_collections[0]

        answers = db_collection_answers.find_one({})
        speech_text_list = answers['IS_KIOSK_KAFFEEAUTOMAT_ARRAY']

        # Zufällige Antwortauswahl aus der Liste
        list_index = randint(0, len(speech_text_list) - 1)
        speech_text = speech_text_list[list_index]

        # Output
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0


# TODO: Passwort weglassen
class OwnCupInKioskHandler(AbstractRequestHandler):
    """Handler fuer die Erlaubnis eigener Tasse am Kiosk Fragen"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OwnCupInKiosk")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

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
