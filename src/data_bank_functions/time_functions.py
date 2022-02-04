from datetime import datetime, timedelta


def current_week_day():
    """
    The function returns the current week day

    Returns:
        weekday(int): The number from 0 to 6, which refers to the current week day
    """

    return datetime.date(datetime.now()).weekday()


def convert_string_to_datetime_object(date_as_string):
    """
    Converts a string in format DD.MM.YYYY to a datetime-object

    Args:
        date_as_string(string): String in format DD.MM.YYYY, that have to be converted to datetime-object

    Returns:
        date(datetime-object): date as datetime-object
    """

    return datetime.strptime(date_as_string, '%d.%m.%Y')


def convert_datetime_object_to_string(date_as_object):
    """
    Converts datetime object to a string in format DD.MM:YYYY

    Args:
        date_as_object(datetime): date as a datetime object

    Returns:
        date(string): date in a string format DD.MM:YYYY
    """

    return date_as_object.strftime('%d.%m.%Y')


def week_day_for_date(date_as_str):
    """
    Returns week day for particular date. Values from 0 (Monday) to 6 (Sunday)

    Args:
        date_as_str(string): date in a string format DD.MM.YYY

    Returns:
        weekday(int): Values in range from 0 to 6
    """

    # convert date in a string format to datetime object
    date_obj = convert_string_to_datetime_object(date_as_str)

    return date_obj.weekday()


def current_week_number():
    """
    Returns current calendar week number
    Returns:
        calendar_week(int): calendar week number in range from 1 bis 53
    """

    return datetime.date(datetime.now()).isocalendar()[1]


def week_number_for_date(date_as_str):
    """
    Returns calendar week number for particular date

    Args:
        date_as_str(string): date in a string format DD.MM.YYY

    Returns:
        calendar_week(int): calendar week number in range from 1 bis 53
    """

    # get date object from string in format DD.MM.YYYY
    date_obj = convert_string_to_datetime_object(date_as_str)
    # get week number from date object
    week_number = date_obj.isocalendar()[1]

    return week_number


def correction_of_date_string(date_as_str):
    """
    Corrects string from not complete format to DD.MM.YYYY format

    Args:
        date_as_str(string): Date in formats like XXXX-XX-11

    Returns:
        date(string): date as a string in format XX.XX.XXXX
    """

    # get day from input parameter
    day_str = date_as_str[-2:]

    # If there is not year in input parameter, year and month will be set to current values
    if date_as_str.startswith('X'):
        month_str = datetime.date(datetime.now()).month
        year_str = datetime.date(datetime.now()).year
    else:  # get year and month from input parameter
        month_str = date_as_str[5:7]
        year_str = date_as_str[:4]

    # put all extracted values in one string
    date_string_in_new_format = str(day_str) + '.' + str(month_str) + '.' + str(year_str)

    return date_string_in_new_format


def convert_week_day_from_number_to_wort(day_as_number):
    """
    change week day as number(0..6) in natural language (Montag..Sonntag)

    Args:
        day_as_number()int: Day of the week as a number in a range 0..6 (Montag..Sonntag)

    Returns:
        day(string): Values from Montag to Sonntag
    """

    list_with_days_names = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    return list_with_days_names[day_as_number]


def get_dates_for_current_week():
    """
    Returns dates (as a list) for all days of the current week

    Returns:
        dates(list): Dates of the current week as a string in a list []
    """

    week_dates = []  # list for return value

    # get current day
    current_date = datetime.date(datetime.now())
    # get date for Monday
    date_monday = (current_date - timedelta(days=(current_date.weekday()) % 7))

    # (date_monday + timedelta(days=i))
    # append dates for all days a week to list
    for i in range(0, 6):
        week_dates.append(convert_datetime_object_to_string(date_monday + timedelta(days=i)))

    return week_dates


def get_date_for_week_day_of_current_week(week_day):
    """
    Returns date for week day of current week. ex for Friday

    Args:
        week_day(string): Week days as a string value e.g. donnerstag, sonntag

    Returns:
        date(string): date as s string for input week day
    """

    # get dates (as a list) for all days of the current week
    week_dates = get_dates_for_current_week()
    list_with_days_names = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
    # index of day(input parameter) from 0 (Monday) to 6 (Sunday)
    index_of_week_day = list_with_days_names.index(week_day)

    return week_dates[index_of_week_day]


def get_date_for_time_indication_values(time_indication):
    """
    Returns date for a day, which specified by value of parameter which is a Alexa slot type time_indication
    Args:
        time_indication(string): time indication such as "heute", "morgen"

    Returns:
        date(string): date for a day that indicated relative to current date e.g. tomorrow, yesterday
    """

    # get current day
    current_date = datetime.date(datetime.now())
    delta = 0  # difference in days to current day

    if time_indication == 'jetzt' or time_indication == 'heute':
        delta = 0
    elif time_indication == 'morgen':
        delta = 1
    elif time_indication == 'übermorgen':
        delta = 2
    elif time_indication == 'gestern':
        delta = -1
    elif time_indication == 'vorgestern':
        delta = -2

    date_of_day_denoted_with_time_indication_as_obj = current_date + timedelta(days=delta)
    date_of_day_denoted_with_time_indication_as_str = \
        convert_datetime_object_to_string(date_of_day_denoted_with_time_indication_as_obj)

    return date_of_day_denoted_with_time_indication_as_str


def get_date_for_days_ahead_intent(days_ahead_in):
    """
    Returns date for a day, which is n-days ahead, where n is a slot value from intent
    Args:
        days_ahead_in: could be a number from 2 to 5, einem oder "einer woche"

    Returns:
        date(string): date for the date, which is indicates with parameter related to current day
    """

    # get current day
    current_date = datetime.date(datetime.now())
    days_ahead = 0  # the number of days ahead

    if days_ahead_in == 'einem':
        days_ahead = 1
    elif days_ahead_in == '2':
        days_ahead = 2
    elif days_ahead_in == '3':
        days_ahead = 3
    elif days_ahead_in == '4':
        days_ahead = 4
    elif days_ahead_in == '5':
        days_ahead = 5
    elif days_ahead_in == 'einer Woche':
        days_ahead = 7

    date_of_day_which_n_days_ahead_as_obj = current_date + timedelta(days=days_ahead)
    date_of_day_which_n_days_ahead_as_str = \
        convert_datetime_object_to_string(date_of_day_which_n_days_ahead_as_obj)

    return date_of_day_which_n_days_ahead_as_str
