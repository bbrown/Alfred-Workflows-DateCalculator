import sys
from datetime import timedelta

from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, UNITS, MAX_LOOKAHEAD_DAYS
from date_formatters import DATE_FORMATTERS_MAP
from date_functions import EXCLUSION_MAP, get_time_format, get_full_format
from date_parser import DateParser
from dateutil.relativedelta import relativedelta
from utils import convert_date_time
from workflow import Workflow, ICON_ERROR


class CalculationError(Exception):
    """Its message is the answer to show, such as "All days excluded"."""


def delta_arithmetic(date_time, operand):
    sign = 1 if operand.operator == "+" else -1
    for timespan in operand.timeSpans:
        date_time += relativedelta(**{UNITS[timespan.span] + 's': sign * int(timespan.amount)})
    return date_time


def do_timespans(command, settings):
    date_time, output_format = convert_date_time(command.dateTime, settings)
    original_date_time = date_time

    for operand in command.operandList:
        date_time = delta_arithmetic(date_time, operand)

    date_time = exclusion_check(original_date_time, date_time, command, settings)

    if hasattr(command, "dateFormat"):
        return DATE_FORMATTERS_MAP[command.dateFormat.lower()](date_time)
    if output_format == get_time_format(settings) and date_time.date() != original_date_time.date():
        output_format = get_full_format(settings)  # a time alone would hide that the answer is on another day
    return date_time.strftime(output_format)


def do_subtraction(command, settings):
    date_time_1, _ = convert_date_time(command.dateTime1, settings)
    date_time_2, _ = convert_date_time(command.dateTime2, settings)

    # either date may have operands, as in "christmas + 1d - today"
    for operand in command.operandList1:
        date_time_1 = delta_arithmetic(date_time_1, operand)
    for operand in command.operandList2:
        date_time_2 = delta_arithmetic(date_time_2, operand)

    if hasattr(command, "exclusionCommands"):
        # the days after the earlier date, up to and including the later one, like a plain count of days
        excluded = get_exclusions(command, settings)
        first, last = sorted((date_time_1.date(), date_time_2.date()))
        return pluralize(sum(1 for day in days_after(first, last) if not excluded(day)), 'day')

    return normalised_days(command, date_time_1, date_time_2)


def days_after(start, end):
    """The days after start, up to and including end, going back in time when end is earlier."""
    step = 1 if end >= start else -1
    return (start + timedelta(days=n) for n in range(step, (end - start).days + step, step))


def get_exclusions(command, settings):
    """Returns a test for whether a day is one the exclusions after "x" leave out."""
    weekdays, dates, ranges = set(), set(), []
    for exclusion in command.exclusionCommands.exclusionList:
        if hasattr(exclusion, "exclusionRange"):
            ranges.append((convert_date_time(exclusion.exclusionRange.fromDateTime, settings)[0].date(),
                           convert_date_time(exclusion.exclusionRange.toDateTime, settings)[0].date()))
        elif hasattr(exclusion, "exclusionDateTime"):
            dates.add(convert_date_time(exclusion.exclusionDateTime, settings)[0].date())
        else:
            weekdays |= EXCLUSION_MAP[exclusion.exclusionMacro]

    if len(weekdays) >= 7:
        raise CalculationError("All days excluded")

    return lambda day: day.weekday() in weekdays or day in dates or any(low <= day <= high for low, high in ranges)


def exclusion_check(original_date_time, date_time, command, settings):
    if not hasattr(command, "exclusionCommands"):
        return date_time
    excluded = get_exclusions(command, settings)

    # Count the excluded days the sum passed, after the starting day. Whole days, so a typed time
    # can't move one in or out.
    extra_days = sum(1 for day in days_after(original_date_time.date(), date_time.date()) if excluded(day))

    # Then go on a day at a time, back in time when taking days away, until as many days that aren't excluded
    # make up for them.
    step = timedelta(days=1 if date_time >= original_date_time else -1)
    for _ in range(MAX_LOOKAHEAD_DAYS):
        if extra_days == 0:
            return date_time
        date_time += step
        if not excluded(date_time.date()):
            extra_days -= 1
    raise CalculationError("That's too far away")


def round_number(count):
    """At most two decimal places, without trailing zeros: 1.50 gives '1.5' and 2.00 gives '2'."""
    return ('%.2f' % count).rstrip('0').rstrip('.')


def pluralize(count, unit):
    return '%s %s%s' % (count, unit, '' if float(count) == 1 else 's')


def calculate_time_interval(interval, start_datetime, end_datetime):
    """
    Counts the whole intervals (year, month, week, day, hour, minute or second) from start to end.
    Returns the count and the date-time where the last whole interval ends, which is where the
    next, smaller interval carries on counting.
    """
    if interval in ('year', 'month'):  # uneven lengths, so count them from the start, without drift
        delta = relativedelta(end_datetime, start_datetime)
        count = delta.years if interval == 'year' else delta.years * 12 + delta.months
        return count, start_datetime + relativedelta(**{interval + 's': count})

    step = timedelta(**{interval + 's': 1})
    count = (end_datetime - start_datetime) // step
    return count, start_datetime + count * step


def normalised_days(command, date_time_1, date_time_2):
    if len(set(command.format)) < len(command.format):  # the parser checks the letters, but not repeats
        raise CalculationError("Invalid format")

    if command.format == "long":
        difference = relativedelta(date_time_1, date_time_2)
        return ', '.join(pluralize(abs(getattr(difference, unit + 's')), unit)
                         for unit in UNITS.values() if unit != 'week')

    start_date_time, end_date_time = sorted((date_time_1, date_time_2))
    units = [UNITS[x] for x in UNITS if x in command.format] or list(UNITS.values())
    elements = []

    for unit in units:
        count, start_date_time = calculate_time_interval(unit, start_date_time, end_date_time)

        if unit == units[-1]:
            # a fraction of the real next interval, so months and years keep their true lengths
            one = relativedelta(**{unit + 's': 1})
            count += (end_date_time - start_date_time) / (start_date_time + one - start_date_time)

        # With no format, leave out the zeros and the seconds. Seconds only show when the format asks for them.
        if command.format or (count > 0 and unit != 'second'):
            elements.append(pluralize(round_number(count), unit))

    return ', '.join(elements)


def main(wf):
    query = wf.args[0]
    error = None

    try:
        command = DateParser(wf.settings).parse_command(query)

        if hasattr(command, "dateTime"):
            output = do_timespans(command, wf.settings)
        else:
            output = do_subtraction(command, wf.settings)

    except SyntaxError:
        error = "Invalid Command"

    except ValueError:
        error = "Invalid Date/time"

    except CalculationError as e:
        error = str(e)

    if error:
        wf.add_item(title=". . .", subtitle=error, valid=False, arg=query, icon=ICON_ERROR)
    else:
        wf.add_item(title=output, subtitle="Copy to clipboard", valid=True, arg=output)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))
