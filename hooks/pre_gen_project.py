import re
import sys

name = "{{ cookiecutter.project_slug }}"

if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]+$", name):
    print(
        "ERROR: Not a valid python package name: %s\n"
        "       Use '_' instead of '-' and start with a letter." % name
    )
    sys.exit(1)
