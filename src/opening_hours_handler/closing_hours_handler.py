from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access
import src.data_bank_functions.time_functions as time_func


class ClosingHoursIntentHandler(AbstractRequestHandler):
    """Handler for ClosingHoursIntent """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ClosingHoursIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method returns closing hours, in relation to the given department.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (1 slot values)
            Slot: mensa_department: 'mensa', 'kiosk', ...

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # Get current week day. Values from 0 (Monday) to 6 (Sunday)
        current_week_day = time_func.current_week_day()

        # Get DB collections
        list_with_collections = data_bank_access(['answers', 'slot_values'])
        db_collection_answers = list_with_collections[0]
        db_collection_slot_values = list_with_collections[1]

        # Get documents from collections
        answers = db_collection_answers.find_one({})
        slot_values = db_collection_slot_values.find_one({})

        # Get lists with answers for opening hours
        speech_text_kiosk_close_hours_answers = answers['KIOSK_CLOSE_HOURS']
        speech_text_kiosk_close_friday_hours__answers = answers['KIOSK_CLOSE_HOURS_FR']
        speech_text_kiosk_close_weekend_hours_answers = answers['KIOSK_OPEN_TIMES']
        speech_text_mensa_close_hours_answers = answers['MENSA_CLOSE_HOURS']

        # Get lists with answers if mensa department is not in the list
        speech_text_mensa_department_negative = answers['MENSA_DEPARTMENT_NEGATIVE']

        # Get lists with mensa departments
        slot_values_for_kiosk = slot_values['MENSA_DEPARTMENT_KIOSK']
        slot_values_for_mensa = slot_values['MENSA_DEPARTMENT_MENSA']

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        mensa_department = slots['mensa_department'].value

        # If slot value is kiosk
        if mensa_department in slot_values_for_kiosk:

            # for Friday
            if current_week_day == 4:
                # Zufällige Antwortauswahl aus der Liste
                list_index = randint(0, len(speech_text_kiosk_close_friday_hours__answers) - 1)
                speech_text = speech_text_kiosk_close_friday_hours__answers[list_index]

            # from Monday to Thursday
            elif current_week_day in range(0, 4):
                # Zufällige Antwortauswahl aus der Liste
                list_index = randint(0, len(speech_text_kiosk_close_hours_answers) - 1)
                speech_text = speech_text_kiosk_close_hours_answers[list_index]

            # for weekend
            else:
                # Zufällige Antwortauswahl aus der Liste
                list_index = randint(0, len(speech_text_kiosk_close_weekend_hours_answers) - 1)
                speech_text = speech_text_kiosk_close_weekend_hours_answers[list_index]

        # If slot value is mensa
        elif mensa_department in slot_values_for_mensa:
            # Zufällige Antwortauswahl aus der Liste
            list_index = randint(0, len(speech_text_mensa_close_hours_answers) - 1)
            speech_text = speech_text_mensa_close_hours_answers[list_index]

        # If slot value not presented in mensa_department
        else:
            speech_text = speech_text_mensa_department_negative

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
