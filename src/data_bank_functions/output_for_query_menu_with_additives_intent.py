from random import randint
from create_string_from_list_values import create_strings_from_list_values
from src.data_bank_functions.get_menu_from_db import get_menus_from_db
from src.data_bank_functions.output_of_all_collections import data_bank_access
import src.data_bank_functions.time_functions as time_func


def output_for_query_menu_with_additives_intent(date, additive, with_or_without):
    """
    Function to help us find the fitting output for the QueryMenuWithAdditivesIntent with the given Arguments.

    Args:
        date(string): A date in the DD.MM.YYYY format
        additive(string): One of the values that the ADDITIVE slot overs
        with_or_without(string): either has the value "mit" or "ohne"

    Returns:
        A fitting speech_text(String) for the given arguments.
    """

    # Get DB collection for negative answer
    list_with_collections = data_bank_access(['answers'])
    db_collection_answers = list_with_collections[0]

    # get list with predetermined answers
    answers = db_collection_answers.find_one({})
    speech_text_list = answers['MENSA_CLOSED_DAY_OFF']

    # random choose from list with answers
    list_index = randint(0, len(speech_text_list) - 1)
    speech_text_negative = speech_text_list[list_index]

    # week day for an output data
    week_day = time_func.week_day_for_date(date)
    week_day_as_str = time_func.convert_week_day_from_number_to_wort(week_day)

    # get menus as a list of strings from DB for particular date
    list_with_menus = get_menus_from_db(date)

    # Handle an error when no data is available for the required day
    if len(list_with_menus) == 0:
        # if Mensa is closed or an error occurred
        speech_text = speech_text_negative
        return speech_text

    week_number = time_func.week_number_for_date(date)

    # Get DB collection with menu for week "week_number"
    collections_with_week_number = data_bank_access([str(week_number)])
    db_collection_current_week_menu = collections_with_week_number[0]

    list_mensa_output = []  # list, to witch all arrays with ausgabe will be append

    # Get all documents from collection, where field "date" = date
    documents_from_collection = db_collection_current_week_menu.find({'date': date})

    # check value of with_or_without and append the mensa_output that fits the value of with or with_or_without
    if with_or_without == "mit":
        for document in documents_from_collection:
            if additive in document['zusatzstoffe']:
                list_mensa_output.append(document['ausgabe'])
            else:
                continue

    if with_or_without == "ohne":
        for document in documents_from_collection:
            if additive in document['zusatzstoffe']:
                continue
            else:
                list_mensa_output.append(document['ausgabe'])

    # Create a speech_text dependent on the length of the list_mensa_output
    if len(list_mensa_output) > 1:
        speech_text = "Am " + week_day_as_str + " den " + date + " gibt es an beiden Ausgaben ein essen " + \
                      with_or_without + " " + additive

    elif len(list_mensa_output) == 0:
        speech_text = "Am " + week_day_as_str + " den " + date + " gibt es kein essen " + with_or_without + \
                      " " + additive

    else:
        speech_text = "Am " + week_day_as_str + " den " + date + " gibt es an " + list_mensa_output[0] + \
                      " ein Gericht " + with_or_without + " " + additive

    return speech_text
