#!/usr/bin/env python
import os
import sys

# bodge to access work with django-websockets for now
WS_DIR = os.path.join(os.path.dirname(__file__), '..', 'django-websockets')
sys.path.append(WS_DIR)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "userchat.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
