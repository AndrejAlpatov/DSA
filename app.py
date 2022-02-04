from src.kiosk_handler.additional_kiosk_questions_handler import OwnCupInKioskHandler
from src.kiosk_handler.kiosk_menu_intent_handler import KioskMenuWhatIntentHandler, KioskMenuIfIntentHandler
from src.opening_hours_handler.opening_hours_handler import OpeningHoursIntentHandler
from src.opening_hours_handler.opening_time_handler import OpeningTimesIntentHandler
from src.opening_hours_handler.closing_hours_handler import ClosingHoursIntentHandler
from src.studierendenwerk_handler.operator_of_mensa_intent_handler import OperatorOfMensaIntentHandler
from src.studierendenwerk_handler.studierendenwerk_activity_intent_handler import StudierendenWerkActivityIntentHandler
from src.studierendenwerk_handler.studierendenwerk_info_intent_handler import StudierendenwerkInfoIntentHandler
from src.studierendenwerk_handler.studierendenwerk_other_mensen_intent_handler import StudierendenwerkOtherMensenIntentHandler
from src.mensa_preis_handler.price_query_intent_handler import PriceQueryIntentHandler
from src.mensa_preis_handler.price_query_session_intent_handler import PriceQuerySessionIntentHandler
from src.mensa_handler.query_menu_intent_handler import QueryMenuIntentHandler
from src.mensa_handler.query_menu_with_additives_handler import QueryMenuWithAddativesIntentHandler
from src.launch_request_handler.launch_request_handler import LaunchRequestHandler
from src.unvalid_question_handler.unvalid_question_intent_handler import UnvalidQuestionIntentHandler
from src.help_intent_handler.help_intent_handler import HelpIntentHandler
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


app = Flask(__name__)

sb = SkillBuilder()


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        app.logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


# add handlers to the skill builder
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(OwnCupInKioskHandler())
sb.add_request_handler(KioskMenuWhatIntentHandler())
sb.add_request_handler(KioskMenuIfIntentHandler())
sb.add_request_handler(OpeningHoursIntentHandler())
sb.add_request_handler(OpeningTimesIntentHandler())
sb.add_request_handler(ClosingHoursIntentHandler())
sb.add_request_handler(OperatorOfMensaIntentHandler())
sb.add_request_handler(StudierendenWerkActivityIntentHandler())
sb.add_request_handler(StudierendenwerkInfoIntentHandler())
sb.add_request_handler(StudierendenwerkOtherMensenIntentHandler())
sb.add_request_handler(PriceQueryIntentHandler())
sb.add_request_handler(PriceQuerySessionIntentHandler())
sb.add_request_handler(QueryMenuIntentHandler())
sb.add_request_handler(UnvalidQuestionIntentHandler())
sb.add_request_handler(QueryMenuWithAddativesIntentHandler())

skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id=1, app=app)


@app.route('/', methods=['GET', 'POST'])
def invoke_skill():
    return skill_adapter.dispatch_request()


if __name__ == '__main__':
    app.run()
