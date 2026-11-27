from bisect import bisect
from datetime import datetime

from date_format_mappings import DAYS

# The functions must all take a datetime object and they must all
# return a string


def week_number(date_time):
    return date_time.strftime("%V")


def week_day(date_time):
    return DAYS[date_time.weekday()][:3].upper()


def week_day_in_isoformat(date_time):
    return str(date_time.isoweekday())


def day_of_year(date_time):
    return str(date_time.timetuple().tm_yday)


def iso_format(date_time):
    return date_time.isoformat(timespec='seconds')


def unix_time(date_time):
    return str(int(date_time.timestamp()))


# Just for a laugh we'll add a function to find the star sign
# for a given date
def zodiac_sign(date_time):
    signs = [(1, 20, "Capricorn"), (2, 18, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
             (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
             (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
             (12, 31, "Capricorn")]
    return signs[bisect(signs, (date_time.month, date_time.day))][2]


LUNAR_MONTH = 29.530588853  # days, on average
MOON_PHASES = ('🌑 New moon', '🌒 Waxing crescent', '🌓 First quarter', '🌔 Waxing gibbous',
               '🌕 Full moon', '🌖 Waning gibbous', '🌗 Last quarter', '🌘 Waning crescent')


def moon_phase(date_time):
    # shortcut: counts average lunar months from a known new moon, so a phase can show a day or so early or late;
    # use an ephemeris if the exact day matters
    age = (date_time - datetime(2000, 1, 6, 18, 14)).total_seconds() / 86400 % LUNAR_MONTH
    return MOON_PHASES[round(age / LUNAR_MONTH * 8) % 8]


# The parser tries these names in this order, so a name must come before
# any shorter name it starts with: 'wdi' before 'wd'.
DATE_FORMATTERS_MAP = {

    "wdi": week_day_in_isoformat,
    "wn": week_number,
    "wd": week_day,
    "!": week_number,
    "doy": day_of_year,
    "iso": iso_format,
    "unix": unix_time,
    "sign": zodiac_sign,
    "moon": moon_phase
}
