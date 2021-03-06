"""
This module contains a helper function for combining list elements
to one string, that gets appended to a new list
"""


def create_strings_from_list_values(list_menus):
    """
    Combines input parameter elements to one string, that gets appended to a new list

    Args:
        list_menus(List): A list with all menu components (database entries)

    Returns:
        list_with_menu_strings_to_be_returned(List): Shortened list with important menu components as strings
    """

    list_with_menu_strings_to_be_returned = []

    for element in list_menus:
        if element[4] == '':  # if menu comprises four parts
            string_with_menu = element[1] + ', ' + element[2]
        else:  # # if menu comprises five parts
            string_with_menu = element[1] + ', ' + element[2] + ', ' + element[3]
        # add string to a list, that will be returned
        list_with_menu_strings_to_be_returned.append(string_with_menu)

    return list_with_menu_strings_to_be_returned
