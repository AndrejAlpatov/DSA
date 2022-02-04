from src.data_bank_functions.output_of_all_collections import data_bank_access
import src.data_bank_functions.time_functions as time_func


def get_menus_from_db(date_as_str):
    """
    Returns all values for key value 'menu' from DB-collection,
     where collection name ist equal to calender week of input parameter date_as_str

    Args:
        date_as_str(string): date value as a string in format DD.MM.YYYY

    Returns:
        A list with all menu values
    """

    week_number = time_func.week_number_for_date(date_as_str)

    # Get DB collection with menu for week "week_number"
    list_with_collections = data_bank_access([str(week_number)])
    db_collection_current_week_menu = list_with_collections[0]

    # Get all documents from collection, where field "date" = date_as_str
    documents_from_collection = db_collection_current_week_menu.find({'date': date_as_str})

    list_with_menus = []  # list, to witch all arrays with menu will be append

    # extract menu-arrays from documents and append to list
    for document in documents_from_collection:
        list_with_menus.append(document['menue'])

    return list_with_menus
