import sys

from date_format_mappings import DEFAULT_WORKFLOW_SETTINGS
from date_functions import get_date_format
from utils import convert_date_time
from workflow import Workflow
from macros_parser import MacrosParser

FOUR_DIGIT_DATE_ERROR = "Please ensure that you have set your date format to one that supports 4-digit years"


def main(wf):
    anniversaries = wf.settings["anniversaries"]

    try:
        command = MacrosParser(wf.settings).parse_command(wf.args[0])
        # names are saved in lower case, so check and delete them that way too
        name = command.anniversaryName.lower()

        if not hasattr(command, "delete") and "%Y" not in get_date_format(wf.settings):
            output = FOUR_DIGIT_DATE_ERROR
        elif hasattr(command, "add") and name in anniversaries:
            output = name + " already exists"
        elif not hasattr(command, "add") and name not in anniversaries:
            output = name + " does not exist"
        elif hasattr(command, "delete"):
            del anniversaries[name]
            wf.settings["anniversaries"] = anniversaries
            output = name + " deleted"
        else:
            anniversaries[name] = convert_date_time(command.dateTime, wf.settings)[0].isoformat()
            wf.settings["anniversaries"] = anniversaries
            output = name + (" added" if hasattr(command, "add") else " changed")

    except SyntaxError:
        output = "Invalid Command"

    except ValueError:
        output = "Invalid Date"

    print(output)


if __name__ == '__main__':
    workflow = Workflow(default_settings=DEFAULT_WORKFLOW_SETTINGS)
    sys.exit(workflow.run(main))
