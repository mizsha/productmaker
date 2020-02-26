import os
import sys
import logging

VERSION = os.environ.get('VERSION', "0.0.1")
TITLE = os.environ.get('TITLE', "productmaker")
DOMAIN = os.environ.get('DOMAIN', "productmaker.cz")
ENVIRONMENT = os.environ.get('ENVIRONMENT', "develop")
SESSION_HEADER = os.environ.get('SESSION_HEADER', "X-Authorization")

API_KEY = os.environ.get('API_KEY', "9414d36b-1da2-430a-b8c5-d0961dc37aa4")
API_URL = os.environ.get(
    'API_URL', "https://applifting-python-excercise-ms.herokuapp.com/api/v1/")

DEBUG = os.environ.get('DEBUG', False) in ["True", "yes", "on"]
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN', "michal.matous@gmail.com")

LOGFILE = os.environ.get('LOGFILE', None)
LOGFILE_FORMAT = '%(asctime)s %(filename)s %(lineno)d %(message)s'

DATABASE_URL = os.environ.get(
    'DATABASE_URL', 'postgres://root@localhost:26257/productmaker')

if LOGFILE:
    logging.basicConfig(
        filename=LOGFILE, level=logging.DEBUG, format=LOGFILE_FORMAT)
else:
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG, format=LOGFILE_FORMAT)
