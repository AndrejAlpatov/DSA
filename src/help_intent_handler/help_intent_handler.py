from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method explains the skill functionality and gives a list of utterance examples to the user,
        if the user needs help.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (no slot values)

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get DB collections
        list_with_collections = data_bank_access(['answers_help'])
        db_collection_answers = list_with_collections[0]

        # Get documents from collections
        answers = db_collection_answers.find_one({})

        # List of all answers
        speech_text_list = answers['STD_ANSWERS']
        transfer_sentence = answers['TRANS_SENTENCE']
        example_question_list = answers['EXAMPLE_QUESTIONS']

        # Select random std_answer
        list_index = randint(0, len(speech_text_list) - 1)
        std_answer = speech_text_list[list_index]

        # Select two random example_questions
        while True:
            list_index1 = randint(0, len(example_question_list) - 1)
            list_index2 = randint(0, len(example_question_list) - 1)
            # Check if the random indices aren't equal
            if list_index1 != list_index2:
                break
        example_question1 = example_question_list[list_index1]
        example_question2 = example_question_list[list_index2]

        # join the strings to an answer
        speech_text = std_answer + " " + transfer_sentence + " " \
                            "\"" + example_question1 + "\" oder \"" + example_question2 + "\""

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response
