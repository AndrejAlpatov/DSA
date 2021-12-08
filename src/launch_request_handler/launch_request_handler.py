from flask import Flask
from pymongo import MongoClient
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_supported_interfaces
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
import res
import json

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    apl_document_path = "res/launchAPLdocument.json"

    def _load_apl_document(self, file_path):
        # type: (str) -> Dict[str, Any]
        """Load the apl json document at the path into a dict object."""
        with open(file_path) as f:
            return json.load(f)

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Willkommen zum Mensa-Skill des studierenden Werk der Vorderpfalz! " \
                      "Wir bieten ihnen hier die Möglichkeit, Informationen zur Mensa und dem Kioskangebot zu erfragen. " \
                      "Fragen Sie mich zum Beispiel was es Heute zum essen gibt."

        #update_database() TODO: function in line 209

        # Abfrage ob das Gerät APL unterstützt
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            response_builder = handler_input.response_builder
            response_builder.add_directive(
                RenderDocumentDirective(
                    token="launchToken",
                    document=self._load_apl_document(self.apl_document_path)
                )
            )

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response