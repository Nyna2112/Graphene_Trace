#!/usr/bin/env python
import os
import sys

<<<<<<< HEAD
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

=======

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphene_trace.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


>>>>>>> 97d8f1e099dcb14aee571f3435fdeabc74c65f11
if __name__ == '__main__':
    main()
