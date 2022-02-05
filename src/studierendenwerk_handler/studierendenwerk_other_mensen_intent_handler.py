""" This module contains the handler for the StudierendenwerkOtherMensenIntent """

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access

class StudierendenwerkOtherMensenIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkOtherMensenIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkOtherMensenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method returns a list of other mensen, which are getting
        leaded by the Studierendenwerk.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (no slot values)

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get DB collections
        list_with_collections = data_bank_access(['answers_stud_werk'])
        db_collection_answers = list_with_collections[0]

        # Get documents from collections
        answers = db_collection_answers.find_one({})

        # List of all answers
        speech_text_list = answers['OTHER_MENSEN']

        # Select random answer
        list_index = randint(0, len(speech_text_list) - 1)
        speech_text = speech_text_list[list_index]

        # Select reprompt
        reprompt = answers['OTHER_MENSEN_REPROMPT']

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response
