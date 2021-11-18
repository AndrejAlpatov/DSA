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

class NamenDerDBAusgebenHandler(AbstractRequestHandler):
    """Handler um alle Namen der DB auszugeben."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NamenDerDBAusgeben")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        xclient = MongoClient("mongodb+srv://testuser:12345@cluster0.ti92d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        database = xclient.get_database("speiseplan")

        datumcol = database["datum"]
        query = {"name": {"$regex": ".*"}}                          # Treffer wenn Attribut 'name' vorhanden
        document = datumcol.find(query)                             # Cursor der Trefferdokumente
        document_size = datumcol.count_documents(query)             # neue Schreibweise um die Anzahl der
                                                                    # gefundenen Dokumente zu erhalten

        namen = ""
        for i in range(0, document_size):
            namen += document[i].__getitem__("name") + " "          # Namen anhaengen

        speech_text = "In der Datenbank sind die Namen " + namen + "enthalten."

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response

    def test(self):
        return 0