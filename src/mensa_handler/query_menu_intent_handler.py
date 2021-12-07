from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import src.data_bank_functions.time_functions as time_func
from src.data_bank_functions.output_for_query_menu_intent import output_for_query_menu_intent


class QueryMenuIntentHandler(AbstractRequestHandler):
    """Handler for Question "was gibt es heute zum essen" """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QueryMenuIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        slot_value_date_for_menu_query = slots['date_for_menu_query'].value
        slot_value_ausgabe = slots['ausgabe'].value
        slot_value_week_day = slots['week_day'].value
        slot_value_time_indication = slots['time_indication'].value

        if slot_value_date_for_menu_query is not None:
            # if slot value is in "AMAZON.DATE format

            # convert to type DD:MM:YYYY
            date_as_string = time_func.correction_of_date_string(slot_value_date_for_menu_query)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_intent(slot_value_ausgabe, date_as_string)

        elif slot_value_week_day is not None:
            # If slot value a week day (Montag..Sonntag)

            # date of the week day received as an input parameter
            date_of_slot_value = time_func.get_date_for_week_day_of_current_week(slot_value_week_day)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_intent(slot_value_ausgabe, date_of_slot_value)

        elif slot_value_time_indication is not None:
            # If slot value a time indication (ex. gestern, morgen)

            # date of the week day that was indicated with a slot value
            date_for_output = time_func.get_date_for_time_indication_values(slot_value_time_indication)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_intent(slot_value_ausgabe, date_for_output)
        else:
            speech_text = 'Bei der Bearbeitung Ihrer Anfrage ist ein Fehler aufgetreten, bitte wiederholen'

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
