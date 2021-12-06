from src.data_bank_functions.output_of_all_collections import data_bank_access


def get_menu_from_db(date):



    # Get DB collection with menu for week "week_number"
    list_with_collections = data_bank_access([str(week_number)])
    db_collection_current_week_menu = list_with_collections[0]

    ausgbe_1 = db_collection_current_week_menu.find({''})