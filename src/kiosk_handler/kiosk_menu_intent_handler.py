""" This module contains the handler for the KioskMenuIfIntent and the KioskMenuWhatIntent """

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access
from src.data_bank_functions.change_list_values_to_lower_case import list_value_to_low_case


class KioskMenuIfIntentHandler(AbstractRequestHandler):
    """Handler for KioskMenuIfIntent """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("KioskMenuIfIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method returns 'Ja, ...' or 'Nein, ...' if special products are available in the kiosk or not.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (1 slot values)
            Slot: kiosk_menu: 'zum trinken', 'süßwaren', ...

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get DB collections
        list_with_collections = data_bank_access(['kiosks_goods', 'answers', 'prompts'])
        db_collection_goods = list_with_collections[0]
        db_collection_answers = list_with_collections[1]
        db_collection_prompts = list_with_collections[2]

        # Get documents from collections
        goods = db_collection_goods.find_one({})
        answers = db_collection_answers.find_one({})
        prompts = db_collection_prompts.find_one({})

        # Get lists with positive und negative answers
        speech_text_positive_answers_list = answers['KIOSK_MENU_POSITIVE']
        speech_text_negative_answers_list = answers['KIOSK_MENU_NEGATIVE']

        # Get lists from "goods" document in lower case for correctness of further comparisons
        sweets = list_value_to_low_case(goods['SWEETS'])
        hot_drinks = list_value_to_low_case(goods['HOT_DRINKS'])
        cold_drinks = list_value_to_low_case(goods['COLD_DRINKS'])
        food = list_value_to_low_case(goods['FOOD'])

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        food_type = slots['kiosk_menu'].value

        # If slot value has product name
        if food_type in sweets or food_type in hot_drinks or food_type in cold_drinks or food_type in food:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index]

        # If slot value has sweets product group name
        elif food_type in goods['SWEETS_WORD']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['SWEET_CHOOSE']

            # Vorlage
            # reprompt = prompts['SWEET_CHOOSE']
            # handler_input.response_builder.speak(speech_text).ask(reprompt)
            # return handler_input.response_builder.ask(speech_text).response

        # If slot value has food product group name
        elif food_type in goods['FOOD_WORD']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['FOOD_CHOOSE']

        # If slot value has drink product group name
        elif food_type in goods['DRINK_WORD']:
            list_index = randint(0, len(speech_text_positive_answers_list) - 1)
            speech_text = speech_text_positive_answers_list[list_index] + ' ' + prompts['DRINK_CHOOSE']

        # If Product name is not in the lists
        else:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_negative_answers_list) - 1)
            speech_text = speech_text_negative_answers_list[list_index]

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0


class KioskMenuWhatIntentHandler(AbstractRequestHandler):
    """Handler for KioskMenuWhatIntent """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("KioskMenuWhatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method returns a list of available products in the kiosk, in relation to the given product category.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (1 slot values)
            Slot: kiosk_menu: 'zum trinken', 'süßwaren', ...

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get DB collections
        list_with_collections = data_bank_access(['kiosks_goods', 'answers'])
        db_collection = list_with_collections[0]
        db_collection_answers = list_with_collections[1]

        # Get documents from collections
        goods = db_collection.find_one({})
        answers = db_collection_answers.find_one({})
        # prompts = db_collection_prompts.find_one({})

        # Get lists with answers for menu categories and negative answers
        speech_text_food_answers_list = answers['WHAT_FOOD_KIOSK']
        speech_text_drink_answers_list = answers['WHAT_DRINKS_KIOSK']
        speech_text_sweets_answers_list = answers['WHAT_SWEETS_KIOSK']
        speech_text_negative_answers_list = answers['KIOSK_MENU_WHAT_NEGATIVE']
        """test comment for variable"""

        # get lists of categories names
        food_words = goods['FOOD_WORD']
        drink_words = goods['DRINK_WORD']
        sweets_words = goods['SWEETS_WORD']

        # get lists of goods pro category
        food = (goods['FOOD'])
        drinks = (goods['HOT_DRINKS'] + goods['COLD_DRINKS'])
        sweets = (goods['SWEETS'])

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        food_type = slots['kiosk_menu'].value
        print(slots)

        # If slot value is food category name
        if food_type in food_words:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_food_answers_list) - 1)

            # make string with all good's values for specific category
            string_for_food_list = ''
            for entry in food:
                string_for_food_list = string_for_food_list + entry + ', '

            speech_text = speech_text_food_answers_list[list_index] + ' ' + string_for_food_list

        # If slot value is drink category name
        elif food_type in drink_words:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_drink_answers_list) - 1)

            # make string with all good's values for specific category
            string_for_drink_list = ''
            for entry in drinks:
                string_for_drink_list = string_for_drink_list + entry + ', '

            speech_text = speech_text_drink_answers_list[list_index] + ' ' + string_for_drink_list

        # If slot value is sweets category name
        elif food_type in sweets_words:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_sweets_answers_list) - 1)

            # make string with all good's values for specific category
            string_for_sweets_list = ''
            for entry in sweets:
                string_for_sweets_list = string_for_sweets_list + entry + ', '

            speech_text = speech_text_sweets_answers_list[list_index] + ' ' + string_for_sweets_list

        # If slot value is None (empty) Says all product categories
        elif food_type is None:
            speech_text = 'Am Kiosk kannst du warme und kalte Getränke sowie eine kleine Auswahl an Snacks kaufen'

        # If Product group name is not present in Kiosk
        else:
            # Random answer selection from the list
            list_index = randint(0, len(speech_text_negative_answers_list) - 1)
            speech_text = speech_text_negative_answers_list[list_index]

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
