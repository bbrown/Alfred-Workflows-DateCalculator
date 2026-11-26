import sys
from datetime import datetime

from date_format_mappings import DATE_MAPPINGS, DEFAULT_WORKFLOW_SETTINGS
from workflow import Workflow


def main(wf):
    anniversaries = wf.settings["anniversaries"]
    date_format = DATE_MAPPINGS[wf.settings['date-format']]['date-format']

    for name in sorted(wf.filter(wf.args[0], anniversaries)):
        date = datetime.fromisoformat(anniversaries[name]).strftime(date_format)
        wf.add_item(title=name + " ➤ " + date, subtitle="Press alt to change, ctrl to delete", arg=name, valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))
