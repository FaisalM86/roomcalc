
# config.py
# Configuration settings for the RoomCalc application

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
DATABASE_NAME = "RoomCalc.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)
DATABASE_URL = "sqlite:///" + DATABASE_PATH

# Security settings
SECRET_KEY = "your_secret_key_here"  # Change this to a random, secure value in production

# Logging configuration
LOG_FILE = "roomcalc.log"
LOG_LEVEL = "DEBUG"  # Can be set to DEBUG, INFO, WARNING, ERROR, or CRITICAL

# Application settings
DEFAULT_AMBIENT_TEMP_SUMMER = 25.0  # Default ambient temperature in summer (Celsius)
DEFAULT_AMBIENT_TEMP_WINTER = -5.0  # Default ambient temperature in winter (Celsius)
DEFAULT_U_VALUE = 2.5  # Default U-value (W/m^2K)

# User access levels
ACCESS_LEVELS = {
    'admin': {
        'read': True,
        'write': True,
        'delete': True
    },
    'user': {
        'read': True,
        'write': True,
        'delete': False
    },
    'guest': {
        'read': True,
        'write': False,
        'delete': False
    }
}
