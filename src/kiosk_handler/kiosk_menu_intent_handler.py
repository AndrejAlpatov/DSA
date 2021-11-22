from pymongo import MongoClient
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint


class KioskMenuIntentHandler(AbstractRequestHandler):
    """Handler for Question "gibt es was am Kiosk...?" """
    # TODO: Für Marco oder Danny Antworten in DB überprüfen und neue Varianten einfügen

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("KioskMenuIfIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get date bank access and then collections from DB
        client = MongoClient('mongodb+srv://Dev:MAHy87WAmv8NI6Kq@mensaskill.2yqml.mongodb.net/'
                             'myFirstDatabase?retryWrites=true&w=majority')
        database = client.get_database("MensaSkill")
        db_collection = database["kiosks_goods"]
        db_collection_answers = database["answers"]
        db_collection_prompts = database['prompts']

        # Get documents from collections
        goods = db_collection.find_one({})
        answers = db_collection_answers.find_one({})
        prompts = db_collection_prompts.find_one({})

        # Get lists with positive und negative answers
        speech_text_positive_answers_list = answers['KIOSK_MENU_POSITIVE']
        speech_text_negative_answers_list = answers['KIOSK_MENU_NEGATIVE']

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        food_type = slots['kiosk_menu'].value

        # If slot value has product name
        if food_type in goods['sweets'] or food_type in goods['hot_drinks'] or food_type in goods['cold_drinks']:
            # Zufällige Antwortauswahl aus der Liste
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index]

        # If slot value has sweets product group name
        elif food_type in goods['sweets_word']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['SWEET_CHOOSE']

            # Vorlage
            # reprompt = prompts['SWEET_CHOOSE']
            # handler_input.response_builder.speak(speech_text).ask(reprompt)
            # return handler_input.response_builder.ask(speech_text).response

        # If slot value has food product group name
        elif food_type in goods['food_word']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['FOOD_CHOOSE']

        # If slot value has drink product group name
        elif food_type in goods['drink_word']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['DRINK_CHOOSE']

        # If Product name is not in the lists
        else:
            # Zufällige Antwortauswahl aus der Liste
            list_index = randint(0, len(speech_text_negative_answers_list) - 1)
            speech_text = speech_text_negative_answers_list[list_index]

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
