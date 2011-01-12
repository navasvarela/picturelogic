import os
from sqlite3 import *
from config import *
import logging
import logging.config 

# create logger
logging.config.fileConfig(LOGGING_CONF) #@UndefinedVariable
logger = logging.getLogger("picturedb")

def get_connection():
    print "Connecting to DB: " + DB_FILE   #@UndefinedVariable
    return connect(DB_FILE)  #@UndefinedVariable

def execute_sql(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    
def init_db():
    try:
        logger.debug("Trying to open DB structure file. It must exist")
        structFile = open(DB_STRUCT_FILE, 'r') #@UndefinedVariable
        logger.debug("Trying to open DB file")
        dbFile = open(DB_FILE,'w+') #@UndefinedVariable
        if not dbFile.readline():
            logger.debug("DB file is either empty or non existent, creating empty database")
            connection = get_connection()
            cursor = connection.cursor()
            while True:
                line = structFile.readline()
                if not line: break
                cursor.execute(line)
            cursor.close()
    finally:
        
        structFile.close()
        dbFile.close()
    
