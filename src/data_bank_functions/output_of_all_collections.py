from src.data_bank_functions.file_for_internal_usage import client_mongoDB


def data_bank_access(collections_names_in):
    """
    Returns collections which names were passed as a list of strings
    Args:
        collections_names_in(list): List of a strings. Strings are the names of collections that have to be returned

    Returns:
        Collections from MongoDB which names a passed as a parameter
    """

    # Get date bank access and then collections from DB
    client = client_mongoDB
    database = client.get_database("MensaSkill")

    # Initialisation of local variables
    all_collections_list = []
    collections_to_be_returned = []

    # list of a names of all collections in DB
    collections_names = database.list_collection_names()

    # Makes a list of all collections in MongoDB
    for collection_name in collections_names:
        all_collections_list.append(database[collection_name])

    # Creates a list of collections which names are passed as a parameter
    for collection_name_in in collections_names_in:
        if collection_name_in in collections_names:
            collections_to_be_returned.append(database[collection_name_in])

    return collections_to_be_returned
