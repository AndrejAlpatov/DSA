from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from src.data_bank_functions.output_of_all_collections import data_bank_access

class PriceQuerySessionIntentHandler(AbstractRequestHandler):
    """Handler for PriceQuerySessionIntent."""

    def deactivate_session(self, db_collection_session, user_id):
        """
        The method deactivates price sessions of the user, using the database.

        Args:
            db_collection_session(): An object of a DB collection, which stores user session documents
            user_id(string): A unique user identifier

        Returns:
            void
        """
        # set the SESSION_ACTIVE to false, where the USER_ID is user_id
        db_collection_session.update_one({"USER_ID": user_id}, {"$set": {"SESSION_ACTIVE": False}})

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PriceQuerySessionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        """
        If the user has an active price session, the method returns the price of the meal,
        in relation to the given membership.

        Args:
            handler_input(HandlerInput): The utterance that triggered the Intent (1 slot value)
            Slot: membership_price_session: 'Student', 'Gast', ...

        Returns:
            handler_input.response_builder.response(Response): Response for the Intent
        """

        # get user id
        user_id = handler_input.request_envelope.context.system.user.user_id

        # Get DB collections
        list_with_collections = data_bank_access(['sessions_mensa_price', 'answers_mensa_price'])
        db_collection_session = list_with_collections[0]
        db_collection_answers = list_with_collections[1]

        # Get documents from collection_session if this user has a session document
        if db_collection_session.count_documents({"USER_ID": user_id}) > 0:
            session_answers = db_collection_session.find_one({"USER_ID": user_id})

        # otherwise return
        else:
            speech_text = "Damit kann ich Ihnen leider nicht weiterhelfen."
            handler_input.response_builder.speak(speech_text).ask(speech_text)
            return handler_input.response_builder.response

        # Get documents from collection_answers
        answers = db_collection_answers.find_one({})

        # Get status of session
        session_status = session_answers['SESSION_ACTIVE']

        # check if the session is false -> return
        if session_status == False:
            speech_text = "Damit kann ich Ihnen leider nicht weiterhelfen."
            handler_input.response_builder.speak(speech_text).ask(speech_text)
            return handler_input.response_builder.response

        # Get slots values
        slots = handler_input.request_envelope.request.intent.slots
        membership = slots['membership_price_session'].value

        # membership student or studenten or studentin or studentinnen -> 3 euro
        if membership == "student" or membership == "studenten" or membership == "studentin" or membership == "studentinnen":
            # select answer
            speech_text = answers['STUDENT_ANSWER']

        # membership gast or gäste -> 5 euro
        elif membership == "gast" or membership == "gäste":
            speech_text = answers['GAST_ANSWER']

        # something went wrong
        else:
            speech_text = "Tut mir leid, aber diese Angehörigkeit gibt es nicht."

        # deactivate session before returning
        self.deactivate_session(db_collection_session, user_id)

        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response
