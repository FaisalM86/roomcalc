
# utils.py
# Utility functions for the RoomCalc application

import os
from datetime import datetime
from config import BASE_DIR

def get_current_time():
    """ Returns the current time formatted as a string """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(event_message):
    """ Logs an event to a file """
    log_file_path = os.path.join(BASE_DIR, 'logs', 'application.log')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{get_current_time()} - {event_message}\n")

def validate_input(input_value, data_type):
    """
    Validates the input based on the expected data type.
    Returns True if valid, False otherwise.
    """
    if data_type == 'int':
        try:
            int(input_value)
            return True
        except ValueError:
            return False
    elif data_type == 'float':
        try:
            float(input_value)
            return True
        except ValueError:
            return False
    elif data_type == 'str':
        if isinstance(input_value, str):
            return True
        else:
            return False
    return False

def create_directory_if_not_exists(directory_path):
    """ Creates a directory if it does not exist """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def initialize_log_directory():
    """ Initializes the log directory """
    log_directory = os.path.join(BASE_DIR, 'logs')
    create_directory_if_not_exists(log_directory)
    log_event("Log directory initialized.")

# Ensure the log directory is initialized when this module is imported
initialize_log_directory()

