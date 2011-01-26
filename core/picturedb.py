from sqlite3 import *
from config import *
import logging

# create logger
logger = logging.getLogger(__name__)

def get_connection():
    logger.debug("Connecting to DB: " + DB_FILE)   #@UndefinedVariable
    return connect(DB_FILE)  #@UndefinedVariable

def execute_sql_update(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    
def execute_sql_select(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rowlist = []
    for row in cursor:
        rowlist.append(row)
    cursor.close()
    return rowlist
    
def init_db():
    try:
        structFile = open(DB_STRUCT_FILE, 'r') #@UndefinedVariable
        execute_sql_update('SELECT * FROM VOLUMES')
        
    except OperationalError:
        logger.debug("DB file is either empty or non existent, creating empty database")
        print "Creating empty database"
        connection = get_connection()
        cursor = connection.cursor()
        while True:
            line = structFile.readline()
            if not line: break
            cursor.execute(line)
        cursor.close()
    finally:      
        structFile.close()
       
    
