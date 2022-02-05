from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import src.data_bank_functions.time_functions as time_func
from src.data_bank_functions.output_for_query_menu_with_additives_intent \
    import output_for_query_menu_with_additives_intent


class QueryMenuWithAdditivesIntentHandler(AbstractRequestHandler):
    """Handler for Question "was gibt es heute mit [Zusatzstoff] zum essen" """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QueryMenuWithAdditives")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        """
        A Class for the "QueryMenuWithAdditivesIntent" in this class we check the value of DATEFORMENUQUERY, WEEKDAY,
        TIMEINDICATION, NUMBERSOFDAYSAHEAD if one of them is set we format them in the way DATEFORMENUQUERY is presented
        and then call the method output_for_query_menu_with_additives_intent
        Args:
            handler_input: The Utterance that triggers the Intent (6 slot values)
            Slot: DATEFORMENUQUERY: A date with format MM/DD/YYYY
            Slot: WEEKDAY: "Montag", "Dienstag", ...
            Slot: TIMEINDICATION: "morgen" , "gestern", ...
            Slot: NUMBEROFDAYSAHEAD: "1", "2",...
            Slot: WITHORWITHOUT: "mit", "ohne"
            Slot: ADDITIVES: "Süßungsmittel", "Schweinefleisch", "Fisch", "Nüsse",...
        Returns:
            handler_input.response_builder.ask(speech_text).response: A speech_text for the Alexa Output
        """

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        slot_value_date = slots['DATEFORMENUQUERY'].value
        slot_value_week_day = slots['WEEKDAY'].value
        slot_value_time_indication = slots['TIMEINDICATION'].value
        slot_value_days_ahead = slots['NUMBEROFDAYSAHEAD'].value
        slot_value_with_or_without = slots['WITHORWITHOUT'].value
        slot_value_for_additives = slots['ADDITIVES'].value

        if slot_value_date is not None:
            # if slot value is in "AMAZON.DATE format

            # convert to type DD:MM:YYYY
            date_as_string = time_func.correction_of_date_string(slot_value_date)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_with_additives_intent(date_as_string, slot_value_for_additives,
                                                                      slot_value_with_or_without)

        elif slot_value_week_day is not None:
            # If slot value a week day (Montag..Sonntag)

            # date of the week day received as an input parameter
            date_of_slot_value = time_func.get_date_for_week_day_of_current_week(slot_value_week_day)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_with_additives_intent(date_of_slot_value, slot_value_for_additives,
                                                                      slot_value_with_or_without)

        elif slot_value_time_indication is not None:
            # If slot value a time indication (ex. gestern, morgen)

            # date of the week day that was indicated with a slot value
            date_for_output = time_func.get_date_for_time_indication_values(slot_value_time_indication)
            # text for output according date and number of menu
            speech_text = output_for_query_menu_with_additives_intent(date_for_output, slot_value_for_additives,
                                                                      slot_value_with_or_without)

        elif slot_value_days_ahead is not None:
            # If slot value is a number of days ahead (ex. einem, 2, einer Woche)

            # date of the day, which is n-Days ahead from today
            date_for_output = time_func.get_date_for_days_ahead_intent(slot_value_days_ahead)

            speech_text = output_for_query_menu_with_additives_intent(date_for_output, slot_value_for_additives,
                                                                      slot_value_with_or_without)

        else:
            speech_text = 'Bei der Bearbeitung Ihrer Anfrage ist ein Fehler aufgetreten, bitte wiederholen'

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.ask(speech_text).response

    @staticmethod
    def test():
        return 0
