#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rippleeffect.settings")

    # read environment variables from .env file
env_file = '.env'
try:
    env_vars = dict(line.strip('\n').split('=',1) for line in open(env_file,'rb'))
    for name, val in env_vars.items():
        os.environ.setdefault(name, val)
except:
    pass

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
