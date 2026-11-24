"""Stdlib replacement for the parts of deanishe's alfred-workflow (Python 2 only) that these scripts use.

Reads and writes the same settings.json in Alfred's workflow data folder, so saved anniversaries
and format choices carry over from the old library.
"""
import copy
import json
import os
import sys
import traceback
import unicodedata

ICON_ERROR = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns'
MATCH_STARTSWITH = 1  # the only match mode the scripts use


class Settings(dict):
    """Saved to disk whenever a key is assigned, so in-place edits of a value need a re-assignment."""

    def __init__(self, path, defaults):
        super().__init__(copy.deepcopy(defaults))
        self.path = path
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                super().update(json.load(f))

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(self, f, indent=2, sort_keys=True)
        os.replace(tmp, self.path)  # atomic, so an interrupted save can't corrupt the anniversaries


class Workflow:
    def __init__(self, default_settings=None):
        self.args = [unicodedata.normalize('NFC', a) for a in sys.argv[1:]]
        self.settings = Settings(os.path.join(os.environ['alfred_workflow_data'], 'settings.json'),
                                 default_settings or {})
        self._items = []

    def add_item(self, title, subtitle='', arg=None, valid=False, icon=None):
        item = {'title': title, 'subtitle': subtitle, 'valid': valid}
        if arg is not None:
            item['arg'] = arg
        if icon:
            item['icon'] = {'path': icon}
        self._items.append(item)

    def send_feedback(self):
        json.dump({'items': self._items}, sys.stdout)

    def filter(self, query, items, key=lambda x: x, match_on=MATCH_STARTSWITH):
        return [i for i in items if key(i).lower().startswith(query.lower())]

    def run(self, func):
        try:
            func(self)
            return 0
        except Exception as e:
            traceback.print_exc()  # shows up in Alfred's workflow debugger
            self._items = []
            self.add_item("Error in workflow 'Date Calculator'", str(e) or type(e).__name__, icon=ICON_ERROR)
            self.send_feedback()
            return 1


if __name__ == '__main__':  # self-check: python3 workflow.py
    import contextlib
    import io
    import tempfile

    with tempfile.TemporaryDirectory() as data_dir:
        os.environ['alfred_workflow_data'] = data_dir
        sys.argv[1:] = ['café']
        defaults = {'anniversaries': {'xmas': '1900-12-25T00:00:00'}}
        wf = Workflow(default_settings=defaults)
        assert wf.args == ['caf\xe9']
        wf.settings['anniversaries']['bday'] = '2000-01-01T00:00:00'
        wf.settings['anniversaries'] = wf.settings['anniversaries']
        assert defaults['anniversaries'] == {'xmas': '1900-12-25T00:00:00'}  # defaults not mutated
        assert Workflow().settings == wf.settings  # saved and reloaded
        assert wf.filter('X', ['xmas', 'bday']) == ['xmas']
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            assert wf.run(lambda _: 1 / 0) == 1
        assert json.loads(out.getvalue())['items'][0]['subtitle'] == 'division by zero'
    print('workflow.py self-check passed')
