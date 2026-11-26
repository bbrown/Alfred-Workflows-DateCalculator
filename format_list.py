"""The choices for one format setting, for the dcalcset keywords: /usr/bin/python3 format_list.py date-format"""
import sys
from datetime import datetime

from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS, SETTING_MAPPINGS
from date_functions import get_date_format, get_time_format
from workflow import Workflow


def main(wf):
    setting = wf.args[0]
    choices = SETTING_MAPPINGS[setting]
    current = wf.settings[setting]
    now = datetime.now()

    for key in sorted(choices):
        if setting == 'date-time-format':  # each layout, filled in with the current date and time
            subtitle = choices[key].format(date=now.strftime(get_date_format(wf.settings)),
                                           time=now.strftime(get_time_format(wf.settings)))
        else:
            subtitle = choices[key]['name']

        # choosing the format that's already set would change nothing
        wf.add_item(title=key + (' *' if key == current else ''), subtitle=subtitle, valid=key != current, arg=key)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))
