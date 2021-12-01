from src.data_bank_functions.file_for_internal_usage import client_mongoDB


def data_bank_access(collections_names_in):
    # Get date bank access and then collections from DB
    # TODO write comments
    client = client_mongoDB
    database = client.get_database("MensaSkill")

    all_collections_list = []
    collections_to_be_returned = []

    collections_names = database.list_collection_names()

    for collection_name in collections_names:
        all_collections_list.append(database[collection_name])

    for collection_name_in in collections_names_in:
        if collection_name_in in collections_names:
            collections_to_be_returned.append(database[collection_name_in])

    return collections_to_be_returned
