from pymongo import MongoClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint


class IsThereQuestionsHandler(AbstractRequestHandler):
    """Handler um auf die Verfügbarkeit des Kaffeeautomaten zu antworten"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("IsThereQuestions")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        client = MongoClient('mongodb+srv://Dev:MAHy87WAmv8NI6Kq@mensaskill.2yqml.mongodb.net/'
                             'myFirstDatabase?retryWrites=true&w=majority')
        database = client.get_database("MensaSkill")
        db_collection = database["answers"]
        answers = db_collection.find_one({})
        speech_text_list = answers['IS_KIOSK_KAFFEEAUTOMAT_ARRAY']

        list_index = randint(0, len(speech_text_list) - 1)
        speech_text = speech_text_list[list_index]

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0

