import json
import os
import sys


_SETTINGS_DEFAULT_LOCATION = os.path.join(os.getcwd(), "settings.py")


def import_settings():

    # Set this environment variable to the settings.py config file location
    settings_file_location = os.path.abspath(
        os.environ.get("TRELLO_GESTION_SETTINGS_FILE", _SETTINGS_DEFAULT_LOCATION)
    )

    # The settings file must be a python file
    if not settings_file_location.endswith(".py"):
        raise ValueError("Settings file must be a .py file!")

    # Append the path to the python runtime
    directory_location = os.path.dirname(settings_file_location)
    sys.path.insert(1, directory_location)

    # Import the settings file
    settings_file_name = os.path.relpath(settings_file_location, directory_location)
    settings = __import__(settings_file_name.strip(".py"))

    sys.path.remove(directory_location)

    return settings


settings = import_settings()
