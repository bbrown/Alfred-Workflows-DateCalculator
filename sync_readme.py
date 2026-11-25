"""Copies README.md into info.plist, where Alfred keeps the workflow's help: /usr/bin/python3 sync_readme.py

Only the readme string is replaced, because rewriting the whole file with plistlib would also reformat its numbers.
"""
import os
import re
from xml.sax.saxutils import escape

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('README.md', encoding='utf-8') as f:
    readme = f.read()
with open('info.plist', encoding='utf-8') as f:
    plist = f.read()

plist, found = re.subn(r'(<key>readme</key>\s*<string>).*?(</string>)', lambda m: m.group(1) + escape(readme) + m.group(2),
                       plist, count=1, flags=re.DOTALL)
assert found == 1, 'info.plist has no readme string'
with open('info.plist', 'w', encoding='utf-8') as f:
    f.write(plist)
print("Alfred's help in info.plist now matches README.md")
