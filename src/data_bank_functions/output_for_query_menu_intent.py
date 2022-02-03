from random import randint
from src.data_bank_functions.output_of_all_collections import data_bank_access
import src.data_bank_functions.time_functions as time_func
from src.data_bank_functions.get_menu_from_db import get_menus_from_db
import src.data_bank_functions.create_string_from_list_values as create_string


def output_for_query_menu_intent(slot_value_ausgabe, date_for_output):
    """

    Args:
        slot_value_ausgabe:
        date_for_output:

    Returns:

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
    week_day = time_func.week_day_for_date(date_for_output)
    week_day_as_str = time_func.convert_week_day_from_number_to_wort(week_day)

    # get menus as a list of strings from DB for particular date
    list_with_menus = get_menus_from_db(date_for_output)

    # Handle an error when no data is available for the required day
    if len(list_with_menus) == 0:
        # if Mensa is closed or an error occurred
        speech_text = speech_text_negative
        return speech_text

    # get menu 1 and menu 2 as string from DB for particular date
    string_for_output_ausgabe_1 = create_string.create_strings_from_list_values(list_with_menus)[0]
    string_for_output_ausgabe_2 = create_string.create_strings_from_list_values(list_with_menus)[1]

    if slot_value_ausgabe is None or slot_value_ausgabe == 'ausgabe 1' or slot_value_ausgabe == '1':
        # if slot_value_ausgabe is not defined or equal 'ausgabe 1'
        speech_text = "Am " + week_day_as_str + " den " + date_for_output + " gibt es " + \
                      string_for_output_ausgabe_1 + ' und dazu eine Tagessuppe und ein Dessert nach Wahl '

    elif slot_value_ausgabe == 'ausgabe 2' or slot_value_ausgabe == '2':
        # if slot_value_ausgabe is 'ausgabe 2'
        speech_text = "Am " + week_day_as_str + " den " + date_for_output + " gibt es " + \
                      string_for_output_ausgabe_2 + ' und dazu eine Tagessuppe und ein Dessert nach Wahl '
    else:
        # if Mensa is closed or ein error occurred
        speech_text = speech_text_negative

    return speech_text
