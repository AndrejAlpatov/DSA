from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from src.data_bank_functions.output_of_all_collections import data_bank_access

class StudierendenwerkInfoIntentHandler(AbstractRequestHandler):
    """Handler for StudierendenwerkInfoIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("StudierendenwerkInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method returns an general expanation about the Studierendenwerk.

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

        # Select answer
        speech_text = answers['INFO_STUD_WERK']

        # Select reprompt
        reprompt = answers['INFO_STUD_WERK_REPROMPT']

        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response
