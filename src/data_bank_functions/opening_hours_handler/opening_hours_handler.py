# from pymongo import MongoClient
# from ask_sdk_core.dispatch_components import AbstractRequestHandler
# from ask_sdk_core.utils import is_intent_name
# from ask_sdk_core.handler_input import HandlerInput
# from ask_sdk_model import Response
# from random import randint
# from src.kiosk_handler.file_for_internal_usage import PASS, USER
#
#
# def data_bank_access():
#     # Get date bank access and then collections from DB
#     client = MongoClient('mongodb+srv://' + USER + ':' + PASS + ':XXX@mensaskill.2yqml.mongodb.net/'
#                          'myFirstDatabase?retryWrites=true&w=majority')
#     database = client.get_database("MensaSkill")
#     db_collection = database["kiosks_goods"]
#     db_collection_answers = database["answers"]
#     db_collection_prompts = database['prompts']
#
#     return db_collection, db_collection_answers, db_collection_prompts
#
#
# class OpeningHoursIntentIntentHandler(AbstractRequestHandler):
#     """ """
#
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("OpeningHoursIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#
#         # Get DB collections
#         db_collection, db_collection_answers, db_collection_prompts = data_bank_access()
#
#         # Get documents from collections
#         goods = db_collection.find_one({})
#         answers = db_collection_answers.find_one({})
#         # prompts = db_collection_prompts.find_one({})
#
#         # Get lists with answers for menu categories and negative answers
#         speech_text_food_answers_list = answers['WHAT_FOOD_KIOSK']
#         speech_text_drink_answers_list = answers['WHAT_DRINKS_KIOSK']
#         speech_text_sweets_answers_list = answers['WHAT_SWEETS_KIOSK']
#         speech_text_negative_answers_list = answers['KIOSK_MENU_WHAT_NEGATIVE']
#
#         # get lists of categories names
#         food_words = goods['FOOD_WORD']
#         drink_words = goods['DRINK_WORD']
#         sweets_words = goods['SWEETS_WORD']
#
#         # get lists of goods pro category
#         food = (goods['FOOD'])
#         drinks = (goods['HOT_DRINKS'] + goods['COLD_DRINKS'])
#         sweets = (goods['SWEETS'])
#
#         # Get slots values
#         slots = handler_input.request_envelope.request.intent.slots
#         food_type = slots['kiosk_menu'].value
#
#         # If slot value is food category name
#         if food_type in food_words:
#             # Zufällige Antwortauswahl aus der Liste
#             list_index = randint(0, len(speech_text_food_answers_list) - 1)
#
#             # make string with all good's values for specific category
#             string_for_food_list = ''
#             for entry in food:
#                 string_for_food_list = string_for_food_list + entry + ', '
#
#             speech_text = speech_text_food_answers_list[list_index] + ' ' + string_for_food_list
#
#         # If slot value is drink category name
#         elif food_type in drink_words:
#             # Zufällige Antwortauswahl aus der Liste
#             list_index = randint(0, len(speech_text_drink_answers_list) - 1)
#
#             # make string with all good's values for specific category
#             string_for_drink_list = ''
#             for entry in drinks:
#                 string_for_drink_list = string_for_drink_list + entry + ', '
#
#             speech_text = speech_text_drink_answers_list[list_index] + ' ' + string_for_drink_list
#
#         # If slot value is sweets category name
#         elif food_type in sweets_words:
#             # Zufällige Antwortauswahl aus der Liste
#             list_index = randint(0, len(speech_text_sweets_answers_list) - 1)
#
#             # make string with all good's values for specific category
#             string_for_sweets_list = ''
#             for entry in sweets:
#                 string_for_sweets_list = string_for_sweets_list + entry + ', '
#
#             speech_text = speech_text_sweets_answers_list[list_index] + ' ' + string_for_sweets_list
#
#         # If Product group name is not present in Kiosk
#         else:
#             # Zufällige Antwortauswahl aus der Liste
#             list_index = randint(0, len(speech_text_negative_answers_list) - 1)
#             speech_text = speech_text_negative_answers_list[list_index]
#
#         handler_input.response_builder.speak(speech_text)
#         return handler_input.response_builder.ask(speech_text).response
#
#     @staticmethod
#     def test():
#         return 0