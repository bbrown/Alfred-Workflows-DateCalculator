from datetime import datetime, date
import re
from date_format_mappings import WN_FUNCTION_REGEX, DAYS

from date_functions import DATE_FUNCTION_MAP, get_date_format, get_time_format, get_full_format, \
    get_time_preprocessor
from dateutil.rrule import rrule, YEARLY


# package for general utility stuff
from parsedatetime import parsedatetime


def get_anniversary(date_object):
    # All at midnight, whatever time was saved, so today's own anniversary never counts: its next is a year away.
    midnight = datetime.min.time()
    anniversary_rule = rrule(bymonthday=date_object.day, bymonth=date_object.month, freq=YEARLY,
                             dtstart=datetime.combine(date_object, midnight))
    return anniversary_rule.after(datetime.combine(datetime.today(), midnight))


def process_macros(date_time_str, anniversaries):
    """The date of a saved anniversary: its next one, or with "^" in front, the original date. None if not saved."""
    name = date_time_str.lstrip("^")
    if name not in anniversaries:
        return None
    anniversary_date = datetime.fromisoformat(anniversaries[name])  # saved with isoformat()
    return anniversary_date if date_time_str.startswith("^") else get_anniversary(anniversary_date)


def natural_parser(date_time, settings):
    """
    This is a bit clever. We've found a python lib that can translate
    """
    # This is a list of the error codes and matching formats that will be used
    # depending on what is returned by the parser
    format_map = {
        1: get_date_format(settings),
        2: get_time_format(settings),
        3: get_full_format(settings)
    }

    # remove the first character and send attempt to translate it
    date_time_to_parse = date_time[1:-1]
    cal = parsedatetime.Calendar()
    date_time_parsed = cal.parseDT(date_time_to_parse)

    # This parser handily sends back an error code, just in case
    error_code = date_time_parsed[1]

    if error_code == 0:
        raise ValueError
    if error_code == 1:  # a date alone is at midnight, like typed dates, not parsedatetime's 9am
        return datetime.combine(date_time_parsed[0], datetime.min.time()), format_map[1]
    return date_time_parsed[0], format_map[error_code]


def get_date_from_week_number(date_time):
    # defaults come from the ISO calendar, whose year differs from the calendar year around New Year
    iso_year, iso_week, iso_day = date.today().isocalendar()
    match = re.match(WN_FUNCTION_REGEX, date_time)
    year = int(match.group('year') or iso_year)
    week_number = int(match.group('week_number') or iso_week)
    day = match.group('day')
    week_day = [d[:3] for d in DAYS].index(day.lower()) + 1 if day else iso_day  # Monday is 1
    return date.fromisocalendar(year, week_number, week_day)


# noinspection PyCallingNonCallable
def convert_date_time(date_time, settings):
    # first of all, what format are we using.
    # We use the longer format if the date contains an ampersand
    # Remember at this point we know that the format is correct.
    date_format = get_date_format(settings)
    time_format = get_time_format(settings)
    full_format = get_full_format(settings)

    # Okay, Does the date command start with a " symbol?
    if date_time.startswith('"'):
        return natural_parser(date_time, settings)

    #How about a date from a week number and a year
    if date_time.startswith("wn"):
        return datetime.combine(get_date_from_week_number(date_time), datetime.min.time()), date_format

    date_time_str = str(date_time)

    if date_time_str.lower() in DATE_FUNCTION_MAP.keys():
        return DATE_FUNCTION_MAP[date_time_str.lower()](settings)  # its dates are at midnight, like typed ones

    anniversary_date = process_macros(date_time_str.lower(), settings['anniversaries'])

    if anniversary_date is not None:
        return datetime.combine(anniversary_date, datetime.min.time()), date_format

    # Try the date and time, then the date, then the time. Upper case, because strptime only reads AM and PM
    # in capitals, and we don't want to make the user type them that way.
    date_time_str = get_time_preprocessor(settings)(date_time_str).upper()
    try:
        return datetime.strptime(date_time_str, full_format), full_format
    except ValueError:
        pass
    try:
        return datetime.strptime(date_time_str, date_format), date_format  # at midnight
    except ValueError:
        pass
    return datetime.combine(datetime.today(), datetime.strptime(date_time_str, time_format).time()), time_format
