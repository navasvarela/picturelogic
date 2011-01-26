import os
import logging.config
# A set of globals used in the application
# DO NOT PLAY WITH THIS UNLESS YOU KNOW WHAT YOU ARE DOING
OS_NAME=os.name
print "OS_NAME:"+os.name
ROOT=os.path.dirname(__file__)
DB_FILE=os.path.join(ROOT,'db/picturelogic.db')
DB_STRUCT_FILE=os.path.join(ROOT,'db/structure.sql')
LOGGING_CONF=os.path.join(ROOT,'logging.conf')
THUMB_SIZE=360

# logging configuration
logging.config.fileConfig(LOGGING_CONF)
