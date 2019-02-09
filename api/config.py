"""
This is the centralized project configuration
"""

import os

############# Postgres database settings #################

POSTGRES_HOST = os.environ.get('CMPUT404_POSTGRES_HOST', None)
POSTGRES_PORT = os.environ.get('CMPUT404_POSTGRES_PORT', None)
POSTGRES_NAME = os.environ.get('CMPUT404_POSTGRES_NAME', None)
POSTGRES_USER = os.environ.get('CMPUT404_POSTGRES_USER', None)
POSTGRES_PASSWORD = os.environ.get('CMPUT404_POSTGRES_PASSWORD', None)


############ App environment variables ###################

HYPERION_HOSTNAME = os.environ.get('CMPUT404_HYPERION_HOSTNAME',
                                   'https://cmput404-front.herokuapp.com')
