from datetime import datetime, timedelta


# Get current week day. Values from 0 (Monday) to 6 (Sunday)
def current_week_day():
    return datetime.date(datetime.now()).weekday()


# convert a string in format DD.MM.YYYY to a datetime obj
def convert_string_to_datetime_object(date_as_string):
    return datetime.strptime(date_as_string, '%d.%m.%Y')


# convert datetime object to a string in format DD.MM:YYYY
def convert_datetime_object_to_string(date_as_object):
    return date_as_object.strftime('%d.%m.%Y')


# Get week day for particular date. Values from 0 (Monday) to 6 (Sunday)
def week_day_for_date(date_as_str):
    # get date object from string in format DD.MM.YYYY
    date_obj = convert_string_to_datetime_object(date_as_str)

    return date_obj.weekday()


# Get current calendar week number
def current_week_number():
    return datetime.date(datetime.now()).isocalendar()[1]


# Get calendar week number for particular date
def week_number_for_date(date_as_str):

    # get date object from string in format DD.MM.YYYY
    date_obj = convert_string_to_datetime_object(date_as_str)
    # get week number from date object
    week_number = date_obj.isocalendar()[1]

    return week_number


# correct type AMAZON.DATE to DD.MM.YYYY format
def correction_of_date_string(date_as_str):
    # get day from input parameter
    day_str = date_as_str[-2:]

    # If there is not year in input parameter, year and month will be set to current values
    if date_as_str.startswith('X'):
        month_str = datetime.date(datetime.now()).month
        year_str = datetime.date(datetime.now()).year
    else:  # # get year and month from input parameter
        month_str = date_as_str[5:7]
        year_str = date_as_str[:4]

    # put all extracted values in one string
    date_string_in_new_format = str(day_str) + '.' + str(month_str) + '.' + str(year_str)

    return date_string_in_new_format


# change week day as number(0..6) in natural language (Montag..Sonntag)
def convert_week_day_from_number_to_wort(day_as_number):

    list_with_days_names = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    return list_with_days_names[day_as_number]


# get dates (as a list) for all days of the current week
def get_dates_for_current_week():

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


# get date for week day of current week. ex for Friday
def get_date_for_week_day_of_current_week(week_day):

    # get dates (as a list) for all days of the current week
    week_dates = get_dates_for_current_week()
    list_with_days_names = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
    # index of day(input parameter) from 0 (Monday) to 6 (Sunday)
    index_of_week_day = list_with_days_names.index(week_day)

    return week_dates[index_of_week_day]


# get date for a day, which specified by value of slot type time_indication
def get_date_for_time_indication_values(time_indication):

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


# get date for a day, which is n-days ahead, where n is a slot value from intent
def get_date_for_days_ahead_intent(days_ahead_in):

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
