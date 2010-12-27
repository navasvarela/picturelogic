import os
# A set of globals used in the application
# DO NOT PLAY WITH THIS UNLESS YOU KNOW WHAT YOU ARE DOING
ROOT=os.path.dirname(__file__)
DB_FILE=os.path.join(ROOT,'db/picturelogic.db')
LOGGING_CONF=os.path.join(ROOT,'logging.conf')