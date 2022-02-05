from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, get_supported_interfaces
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from src.data_bank_functions.output_of_all_collections import data_bank_access
import json
from pathlib import Path
from src.ftp import FTPManager
from src.xml_handler import XMLManager

RELATIVE_PATH = '../../res/launchAPLdocument.json'
path = Path(__file__).parent / RELATIVE_PATH


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    apl_document_path = path

    def load_apl_document(self, file_path):
        # type: (str) -> Dict[str, Any]
        """
        The method loads the apl json document at the path into a dict object.

        Args:
            file_path(string): The path to the apl json document.

        Returns:
            json.load(f)(dictionary): The apl document
        """

        with open(file_path) as f:
            return json.load(f)

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        The method greets the user and additionally explains the functionality of the skill,
        if that user launches the skill for the fist time.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (no slot values)

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # get user id
        user_id = handler_input.request_envelope.context.system.user.user_id

        # deactivate price_session if one is active
        # 1. Get DB collections
        list_with_collections = data_bank_access(['sessions_mensa_price'])
        db_collection_session = list_with_collections[0]
        # 2. set the SESSION_ACTIVE to false, where the USER_ID is user_id
        db_collection_session.update_one({"USER_ID": user_id}, {"$set": {"SESSION_ACTIVE": False}})

        # Get DB collections
        list_with_collections = data_bank_access(['answers_launch'])
        db_collection_answers = list_with_collections[0]

        # Get documents from collections answer
        answers = db_collection_answers.find_one({})

        # Insert a user profile document in DB
        user_profiles_collection_list = data_bank_access(['user_profiles'])
        user_profiles_collection = user_profiles_collection_list[0]
        # check if there is already a UserProfile with the user_id Varibale
        if user_profiles_collection.find_one({'user_id': user_id}) is None:
            user_profile_doc = {
                'user_id': user_id
            }
            user_profiles_collection.insert_one(user_profile_doc)

            speech_text = answers['STD_ANSWER']

        else:
            # create KnownUser because there already is a UserProfile
            speech_text = answers['USER_KNOWN_ANSWER']

        # create a list with files that need to be read by the XMLReader
        files_to_read = FTPManager.check_for_new_data()
        # creat XMLReader to Read XML Files
        reader = XMLManager.XMLFileReader()
        # if there are no files in files to read we dont need to commit to the for loop
        if len(files_to_read) > 0:
            # reader will read every document in the res ordner that is in the list and create databank entries
            for file in files_to_read:
                reader.get_data("res\\" + file)

        # Abfrage ob das Gerät APL unterstützt
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            response_builder = handler_input.response_builder
            response_builder.add_directive(
                RenderDocumentDirective(
                    token="launchToken",
                    document=self.load_apl_document(self.apl_document_path)
                )
            )

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response
