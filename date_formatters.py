from bisect import bisect

from date_format_mappings import DAYS

# The functions must all take a datetime object and they must all
# return a string


def week_number(date_time):
    return date_time.strftime("%V")


def week_day(date_time):
    return DAYS[date_time.weekday()][:3].upper()


def week_day_in_isoformat(date_time):
    return str(date_time.isoweekday())


def iso_format(date_time):
    return date_time.isoformat(timespec='seconds')


# Just for a laugh we'll add a function to find the star sign
# for a given date
def zodiac_sign(date_time):
    signs = [(1, 20, "Capricorn"), (2, 18, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
             (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
             (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
             (12, 31, "Capricorn")]
    return signs[bisect(signs, (date_time.month, date_time.day))][2]


# The parser tries these names in this order, so a name must come before
# any shorter name it starts with: 'wdi' before 'wd'.
DATE_FORMATTERS_MAP = {

    "wdi": week_day_in_isoformat,
    "wn": week_number,
    "wd": week_day,
    "!": week_number,
    "iso": iso_format,
    "sign": zodiac_sign
}
