#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # append parent dir of parent dir to PYTHONPATH
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
