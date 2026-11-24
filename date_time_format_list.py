from __future__ import unicode_literals, print_function

import sys
from arrow.arrow import datetime

from workflow import Workflow
from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, DATE_TIME_MAPPINGS, DATE_MAPPINGS, TIME_MAPPINGS


def get_formatted_key(current_date_time, key, settings):
    return DATE_TIME_MAPPINGS[key]['date-time-format'](
        date=current_date_time.strftime(DATE_MAPPINGS[settings['date-format']]['date-format']),
        time=current_date_time.strftime(TIME_MAPPINGS[settings['time-format']]['time-format']))


def main(wf):
    # Get the current setting
    current_setting = wf.settings['date-time-format']

    # These are the date formats the workflow supports
    date_time = datetime.now()

    for key in sorted(DATE_TIME_MAPPINGS.keys()):
        # Indicate the current setting for the user
        if key == current_setting:
            title_setting = key + ' *'
        else:
            title_setting = key

        # You know what? There's not point letting them set the format to the current format. It's
        # a waste of effort.
        wf.add_item(title=title_setting, subtitle=get_formatted_key(date_time, key, wf.settings),
                    valid=(key != current_setting),
                    arg=key)

    wf.send_feedback()


if __name__ == '__main__':
    workFlow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workFlow.run(main))