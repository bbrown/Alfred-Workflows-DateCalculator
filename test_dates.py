"""Self-check for the date maths, and that info.plist matches the README and code: /usr/bin/python3 test_dates.py

Each check is a case that once gave a wrong answer. The dates are fixed, so the checks don't depend on today.
"""
import contextlib
import copy
import io
import os
import plistlib
from datetime import date, datetime, timedelta

import date_calculator
import date_functions
import set_anniversary
import utils
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, SETTING_MAPPINGS


class FakeWorkflow:
    """Just enough of workflow.Workflow for a script's main(): one query in, the first item's text out.

    An error row's message comes out as "error: " plus the message, so a check can tell it from an answer
    that Enter would copy.
    """

    def __init__(self, query, settings):
        self.args, self.settings, self.items = [query], settings, []

    def add_item(self, title, subtitle='', arg=None, valid=False, icon=None):
        self.items.append(title if valid else 'error: ' + subtitle)

    def send_feedback(self):
        pass


def settings(**changes):
    result = copy.deepcopy(DEFAULT_WORKFLOW_SETTINGS)
    result.update(changes)
    return result


def dcalc(query, workflow_settings=None):
    wf = FakeWorkflow(query, workflow_settings or settings())
    date_calculator.main(wf)
    return wf.items[0]


def dcalcset_list(query, workflow_settings):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        set_anniversary.main(FakeWorkflow(query, workflow_settings))
    return out.getvalue().strip()


# Holiday dates sit at the end of the day, like typed dates, so countdowns aren't a day short
for name in ('easter', 'passover', 'end year', 'mom'):
    assert utils.convert_date_time(name, settings())[0].time() == datetime.max.time(), name

# Decimals use the real lengths of years and months
assert dcalc('20.12.26 - 01.01.26 y') == '0.97 years'
assert dcalc('31.01.26 - 01.01.26 m') == '0.97 months'
assert dcalc('01.07.27 - 01.01.26 y') == '1.5 years'

# Months are counted without drifting after a short month, so md agrees with long
assert dcalc('30.03.26 - 31.01.26 md') == '1 month, 30 days'

# Seconds show when the format asks for them, and a long span in seconds answers at once
assert dcalc('09:00 - 17:30 s') == '30600 seconds'
assert dcalc('01.01.00 - 01.01.26 s') == '820540800 seconds'

# Anniversary names have one spelling, and mistakes give a message instead of a crash
four_digit_years = settings(**{'date-format': 'dd.mm.yyyy'})
assert dcalcset_list('add Christmas 01.01.2000', four_digit_years) == 'christmas already exists'
assert four_digit_years['anniversaries']['christmas'] == DEFAULT_WORKFLOW_SETTINGS['anniversaries']['christmas']
assert dcalcset_list('delete nosuch', four_digit_years) == 'nosuch does not exist'
assert dcalcset_list('add newone', four_digit_years) == 'Invalid Date'

# A name that starts another name doesn't hide it
for added in ('bday 03.03.1990', 'bdaytwo 04.04.1991', 'mum_bday 01.02.1950'):
    assert dcalcset_list('add ' + added, four_digit_years).endswith(' added'), added
assert dcalc('^bdaytwo', four_digit_years) == '04.04.1991'
assert dcalc('mum_bday', four_digit_years).startswith('01.02.')  # its next 1 February
first_of_next_month = (date.today().replace(day=1) + timedelta(days=32)).replace(day=1)
assert dcalc('next month') == first_of_next_month.strftime('%d.%m.%y')
assert dcalc('*wd') in ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
assert dcalc('+1d', settings(anniversaries={})) == 'error: Invalid Command'
real_current_date = date_functions._get_current_date
date_functions._get_current_date = lambda: datetime(2026, 12, 15, 23, 59, 59, 999999)
assert date_functions.next_month(settings())[0].date() == date(2027, 1, 1)
date_functions._get_current_date = real_current_date

# Week numbers: capitals, subtraction, and the ISO year around New Year
assert dcalc('wn 2015 5 SUN') == '01.02.15'
assert dcalc('wn 2015 5 sun - 08.02.15') == '1 week'

# Format options read the answer itself, so a two-digit year can't move it into 1969-2068 (25.12.1900 was a Tuesday)
assert dcalc('^christmas wd') == 'TUE'
assert dcalc('01.01.26 + 50y wd') == 'WED'
assert dcalc('25.12.26 iso') == '2026-12-25T23:59:59'  # whole seconds; a date sits at the end of its day


class December29(date):  # 29.12.2025 is in ISO week 1 of 2026
    @classmethod
    def today(cls):
        return cls(2025, 12, 29)


real_date, utils.date = utils.date, December29
assert utils.get_date_from_week_number('wn') == date(2025, 12, 29)
utils.date = real_date

# Excluding days works when a time is typed (27.11.26 is a Friday)
assert dcalc('27.11.26@10:00 + 1d x weekends') == '30.11.26@10:00'

# Each exclusion's day names match its rule, and a long name isn't read as a shorter one
assert dcalc('27.11.26 + 1d x exsun sundays') == 'error: All days excluded'
assert dcalc('27.11.26 + 1d x saturdays') == '29.11.26'

# Exclusions count whole days, backwards when taking days away, and a typed time can't land on an excluded date
assert dcalc('24.11.26 - 5d x weekends') == '17.11.26'
assert dcalc('30.11.26 - 1d x weekends') == '27.11.26'
assert dcalc('27.11.26@10:00 + 3d x 30.11.26') == '01.12.26@10:00'

# A long excluded range is skipped in either direction, and only moving the answer over 100 years is too far
assert dcalc('27.11.26 - 1d x 01.01.25 to 26.11.26') == '31.12.24'
assert dcalc('26.11.26 + 1d x 27.11.26 to 30.12.27') == '31.12.27'
assert dcalc('26.11.2026 + 1d x 27.11.2026 to 31.12.2200', four_digit_years) == "error: That's too far away"

# The exclude keyword is a whole word: "xmon" without it isn't read as "x mon" (exclude Mondays)
assert dcalc('24.11.26 + 5d xmon') == 'error: Invalid Command'
assert dcalc('24.11.26 + 5d x xmon') == '28.12.26'

# Alfred's help (the readme in info.plist) is a copy of README.md, so they can't drift apart
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'info.plist'), 'rb') as plist, open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    info = plistlib.load(plist)
    assert info['readme'] == f.read(), "Alfred's help is out of date: run /usr/bin/python3 sync_readme.py"

# the Configure Workflow pickers offer exactly the formats the code knows, with the same defaults
for item in info['userconfigurationconfig']:
    key = item['variable'].replace('_', '-')
    assert item['config']['default'] == DEFAULT_WORKFLOW_SETTINGS[key], key
    assert sorted(value for _, value in item['config']['pairs']) == sorted(SETTING_MAPPINGS[key]), key

# every script Alfred runs is here, and format_list.py gets a setting it knows
for obj in info['objects']:
    words = obj['config'].get('script', '').split()
    if words[:1] == ['/usr/bin/python3']:
        assert os.path.exists(os.path.join(here, words[1])), words
        assert words[1] != 'format_list.py' or words[2] in SETTING_MAPPINGS, words

print('test_dates.py self-check passed')
