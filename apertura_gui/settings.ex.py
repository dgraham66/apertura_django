import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from .common_settings import *

# Rename this file to settings.py to deploy this app.

# The common settings file has defaults for development.
# Before deploying to production, uncomment and configure the following:

#DEBUG = False
#ALLOWED_HOSTS = []

#DATABASE=...

ADMINS = [
    #('Admin Name', 'adminemail@example.com'),
]

