from datetime import datetime


# Get current week day. Values from 0 (Monday) to 6 (Sunday)
def current_week_day():
    return datetime.date(datetime.now()).weekday()


# Get current calendar week number
def current_week_number():
    return datetime.date(datetime.now()).isocalendar()[1]


# Get calendar week number for particular date
def week_number_for_date(date_as_str):

    # get date object from string in format DD.MM.YYYY
    date_obj = datetime.strptime(date_as_str, '%d.%m.%Y')
    # get week number from date object
    week_number = date_obj.isocalendar()[1]

    return week_number
