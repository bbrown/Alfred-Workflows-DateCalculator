# This file contains all the functions that the workflow
# uses for specialised dates.
from math import floor

from datetime import datetime, timedelta
from date_format_mappings import DATE_MAPPINGS, TIME_MAPPINGS, DATE_TIME_MAPPINGS, DAYS
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from dateutil.rrule import rrule, YEARLY


def get_date_format(settings):
    return DATE_MAPPINGS[settings['date-format']]['date-format']


def get_time_format(settings):
    return TIME_MAPPINGS[settings['time-format']]['time-format']


def get_full_format(settings):
    return DATE_TIME_MAPPINGS[settings['date-time-format']].format(date=get_date_format(settings),
                                                                   time=get_time_format(settings))


def get_date_format_regex(settings):
    return DATE_MAPPINGS[settings['date-format']]['regex']


def get_time_format_regex(settings):
    return TIME_MAPPINGS[settings['time-format']]['regex']


def get_full_format_regex(settings):
    return DATE_TIME_MAPPINGS[settings['date-time-format']].format(date=get_date_format_regex(settings),
                                                                   time=get_time_format_regex(settings))


def get_time_preprocessor(settings):
    return TIME_MAPPINGS[settings['time-format']]['pre-process']


def _get_current_date():
    return datetime.combine(datetime.today(), datetime.max.time())


def _get_current_time():
    return datetime.combine(datetime.today(), datetime.now().time())


def current_date(settings):
    return _get_current_date(), get_date_format(settings)


def current_time(settings):
    return _get_current_time(), get_time_format(settings)


def now(settings):
    return datetime.now(), get_full_format(settings)


def yesterday(settings):
    return _get_current_date() - timedelta(days=1), get_date_format(settings)


def tomorrow(settings):
    return _get_current_date() + timedelta(days=1), get_date_format(settings)


def days_from_today(delta):
    """Returns a function for a day relative to today, such as next Monday."""
    def _days_from_today(settings):
        return _get_current_date() + delta, get_date_format(settings)
    return _days_from_today


def next_rule(**rule):
    """Returns a function for the next date after today that a yearly rrule picks, such as the last Sunday in March."""
    def _next_rule(settings):
        return rrule(freq=YEARLY, **rule).after(_get_current_date()), get_date_format(settings)
    return _next_rule


def start_of_year(settings):
    return datetime(year=_get_current_date().year, day=1, month=1), get_date_format(settings)


def end_of_year(settings):
    return datetime(year=_get_current_date().year, day=31, month=12), get_date_format(settings)


def next_month(settings):
    return _get_current_date() + relativedelta(months=1, day=1), get_date_format(settings)


def next_passover(settings):
    """
    Credit goes to programmingpraxis.com for supplying
    the function for working out the date of the passover
    """

    def calc_passover_year(year):
        return datetime(year, 3, 21) + timedelta(rosh_hashanah(year))

    def rosh_hashanah(year):

        g = year % 19 + 1
        r = 12 * g % 19

        v = (floor(year / 100.0) - floor(year / 400.0) - 2)
        v += 765433.0 * r / 492480
        v += (year % 4) / 4.0
        v -= (313.0 * year + 89081) / 98496

        n = int(v)
        f = v - n

        # Monday .. Sunday = 0..6
        dow = (datetime(year, 8, 31).weekday() + n) % 7

        if dow in (2, 4, 6):
            n += 1
        elif dow == 0 and f >= 23269.0 / 25920 and r > 11:
            n += 1
        elif dow == 1 and f >= 1367.0 / 2160 and r > 6:
            n += 2

        return n

    # Just need the year of the current date
    passover_date = calc_passover_year(_get_current_date().year)

    # if we've already gone past it then we need to try for the following year.
    if passover_date >= _get_current_date():
        return passover_date, get_date_format(settings)
    else:
        return calc_passover_year(_get_current_date().year + 1), get_date_format(settings)


DATE_FUNCTION_MAP = {

    "date": current_date,
    "today": current_date,
    "*": current_date,
    "time": current_time,
    "&": current_time,
    "now": now,
    "#": now,
    "yesterday": yesterday,
    "<": yesterday,
    "tomorrow": tomorrow,
    ">": tomorrow,
    "easter": next_rule(byeaster=0),
    "start bst": next_rule(bymonth=3, byweekday=SU(-1)),
    "end bst": next_rule(bymonth=10, byweekday=SU(-1)),
    "start year": start_of_year,
    "end year": end_of_year,
    "next month": next_month,
    "passover": next_passover,
    "pancake day": next_rule(byeaster=-47),
    "lent": next_rule(byeaster=-46),
    "mlk": next_rule(bymonth=1, byweekday=MO(3)),
    "mum": next_rule(byeaster=-21),  # Mothering Sunday in the UK
    "mom": next_rule(bymonth=5, byweekday=SU(2)),  # Mother's Day in the US
    "mutter": next_rule(bymonth=5, byweekday=SU(2))
}

for n, day in enumerate(DAYS):
    DATE_FUNCTION_MAP['next ' + day[:3]] = days_from_today(relativedelta(days=+1, weekday=n))
    DATE_FUNCTION_MAP['prev ' + day[:3]] = days_from_today(relativedelta(days=-1, weekday=(MO, TU, WE, TH, FR, SA, SU)[n](-1)))


def _exclusion_map():
    """Maps each exclusion word to the weekdays it excludes, numbered from Monday as 0."""
    workdays, weekend = frozenset(range(5)), frozenset({5, 6})
    exclusions = {'weekdays': workdays, 'wkdy': workdays, 'weekends': weekend, 'wknd': weekend,
                  'all except weekdays': weekend, 'xwkdy': weekend,
                  'all except weekends': workdays, 'xwknd': workdays}
    for n, day in enumerate(DAYS):
        exclusions[day + 's'] = exclusions[day[:3]] = frozenset({n})
        # the short "except" forms for Saturday and Sunday have always been exsat and exsun
        exclusions['all except ' + day + 's'] = exclusions[('ex' if n >= 5 else 'x') + day[:3]] = frozenset(range(7)) - {n}
    return exclusions


EXCLUSION_MAP = _exclusion_map()
