from imports import os
from django.core.management import execute_from_command_line
from setup import show_dialog

def self_destruct():
    try:
        # Delete the script file
        script_path = os.path.abspath(__file__)
        os.remove(script_path)
    except Exception as e:
        show_dialog(f"{e}")
def run_migrations(): 
    try:
    # Run migrations using manage.py
        execute_from_command_line(['manage.py', 'migrate'])
    except Exception as e:
        show_dialog(f"{e}")
# Call the function to run migrations   

run_migrations()
show_dialog("Success db set up")
self_destruct()