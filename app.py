from src.kiosk_handler.namen_ausgeben_handler import NamenDerDBAusgebenHandler
#from src.xml_reader.XMLReader import XMLFileReader as XMLReader
#from src.ftp.FTPManager import *
from src.kiosk_handler.additional_kiosk_questions_handler import IsThereQuestionsHandler, OwnCupInKioskHandler
from src.kiosk_handler.kiosk_menu_intent_handler import KioskMenuWhatIntentHandler, KioskMenuIfIntentHandler
from src.opening_hours_handler.opening_hours_handler import OpeningHoursIntentHandler
from src.opening_hours_handler.opening_time_handler import OpeningTimesIntentHandler
from src.opening_hours_handler.closing_hours_handler import ClosingHoursIntentHandler
from src.studierendenwerk_handler.operator_of_mensa_intent_handler import OperatorOfMensaIntentHandler
from src.studierendenwerk_handler.studierendenwerk_activity_intent_handler import StudierendenWerkActivityIntentHandler
from src.studierendenwerk_handler.studierendenwerk_info_intent_handler import StudierendenwerkInfoIntentHandler
from src.studierendenwerk_handler.studierendenwerk_other_mensen_intent_handler import StudierendenwerkOtherMensenIntentHandler
from src.preis_handler.price_query_intent_handler import PriceQueryIntentHandler
from src.preis_handler.price_query_session_intent_handler import PriceQuerySessionIntentHandler
from src.mensa_handler.query_menu_intent_handler import QueryMenuIntentHandler
from src.launch_request_handler.launch_request_handler import LaunchRequestHandler
from flask import Flask
from pymongo import MongoClient
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response




app = Flask(__name__)

sb = SkillBuilder()


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


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

class RechenIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RechenIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        lhs = slots["lhs"].value
        rhs = slots["rhs"].value

        if rhs is None:
            speech_text = "Kein Ergebnis, einfach  " + str(int(lhs))
        else:
            speech_text = "Das Ergebnis ist " + str(int(lhs) + int(rhs))

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response

class NamenAufDBSchreibenHandler(AbstractRequestHandler):
    """Handler um einen Namen auf die DB zu schreiben."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NamenAufDBSchreiben")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        nameneu = slots["nameneu"].value

        xnameDoc = {
            'name': nameneu
        }

        xclient = MongoClient("mongodb+srv://testuser:12345@cluster0.ti92d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database = xclient.get_database("new")

        datumcol = database["neu"]
        datumcol.insert_one(xnameDoc)

        speech_text = "<prosody rate='x-fast' pitch='x-high'> Name " + nameneu + " auf Datenbank geschrieben </prosody>"

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response

class ReadNameFromDBHandler(AbstractRequestHandler):
    """Handler um einen Namen von der DB zu lesen."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ReadNameFromDB")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        xclient = MongoClient("mongodb+srv://testuser:12345@cluster0.ti92d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database = xclient.get_database("speiseplan")

        slots = handler_input.request_envelope.request.intent.slots
        name_in = slots["nameDB"].value

        datumcol = database["datum"]
        #document = datumcol.find({"name": name_in})            # brauchen wir hier nicht weil nicht auf die
                                                                # Daten zugegriffen wird

        #if document.count() > 0:           veraltet
        if datumcol.count_documents({"name": name_in}) > 0:     # neue Schreibweise um die Anzahl der gefundenen
                                                                # Dokumente zu erhalten
            speech_text = "Der Name " + name_in + " ist in der Datenbank enthalten."
        else:
            speech_text = "Der Name " + name_in + " ist nicht in der Datenbank enthalten."

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response

#TODO: implementation of update_database()
#def update_database():
    # tcpcon = tcpcon()
    # if(tcpcon.check_dir()): #true wenn datei vorhanden
        # filenames = tcpcon.get_filenames() -> liste aller dokumente?
        # download file -> for schleife die alle dokumente runterläd
        # for filename in filenames:
            # tcpcon.mv("filename,../Done") -> schleife die Files aus Filename in Done ordner verschiebt
        # xmlreader = xmlreader()
        # for filename in filenames:
            # xmlreader.get_data("res/"+filename) -> for schleife die aus allen neuen dokumenten die daten liest und auf db schreibt



sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

# test
sb.add_request_handler(RechenIntentHandler())
sb.add_request_handler(NamenAufDBSchreibenHandler())
sb.add_request_handler(ReadNameFromDBHandler())
sb.add_request_handler(NamenDerDBAusgebenHandler())
sb.add_request_handler(IsThereQuestionsHandler())
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


skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id=1, app=app)


@app.route('/', methods=['GET', 'POST'])
def invoke_skill():
    return skill_adapter.dispatch_request()


if __name__ == '__main__':
    app.run()