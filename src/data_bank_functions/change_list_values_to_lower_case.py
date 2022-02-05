""" This module contains a helper function for list value manipulations """

def list_value_to_low_case(list_in):
    """
    Get a string from lowercase and uppercase characters and returns a new
    one which consists only of a lowercase characters
    Args:
        list_in(list): list with strings

    Returns:
        list that comprises strings in lower case
    """

    # list for output
    return_list = []

    # append to output lists strings in lowercase
    for entity in list_in:
        return_list.append(entity.lower())

    return return_list
