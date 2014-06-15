#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

    from django.core.management import execute_from_command_line

    print('Running Tests with timezone support disabled:')

    args = []
    args.append(sys.argv[0])
    args.append('test')
    args.append('--pythonpath=../')
    args.append('django_mixins')

    if len(sys.argv) > 1:

        args.extend(sys.argv[1:])

    execute_from_command_line(args)

