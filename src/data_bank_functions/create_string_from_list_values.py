def create_strings_from_list_values(list_menus):
    # makes strings from list for every element in input parameter

    list_with_menu_strings_to_be_returned = []

    for element in list_menus:
        if element[4] == '':  # if menu comprise four parts
            string_with_menu = element[1] + ', ' + element[2]
        else:  # # if menu comprise five parts
            string_with_menu = element[1] + ', ' + element[2] + ', ' + element[3]
        # add string to a list, that will be returned
        list_with_menu_strings_to_be_returned.append(string_with_menu)

    return list_with_menu_strings_to_be_returned
