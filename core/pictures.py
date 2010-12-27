import os
import Image
import logging
import logging.config 
from sqlite3 import *
from config import * 

# create logger
logging.config.fileConfig(LOGGING_CONF) #@UndefinedVariable
logger = logging.getLogger("pictures")
  

image_exts = ['jpg', 'JPG','png', 'gif', 'tif', 'bmp', 'xpm']
        
def get_connection():
    print "Connecting to DB: " + DB_FILE   #@UndefinedVariable
    return connect(DB_FILE)  #@UndefinedVariable

def get_pictures_insert_stmt(picture):
    return 'INSERT INTO PICTURES ( filename, path, thumbnail) VALUES (\'%(filename)s\',  \'%(path)s\', \'%(thumbnail)s\')' % \
                        picture

def select_pictures_stmt():
    return 'SELECT * FROM PICTURES'

def insert_picture(picture):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(get_pictures_insert_stmt(picture))
    connection.commit()
    cursor.close()


def get_pictures_from_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(select_pictures_stmt())
    list = []
    for row in cursor:
        list.append(row)
    return list
def import_from_folder(folder):
    for root, dirs, files in os.walk(folder): #@UnusedVariable
        for file in files:
            if is_image(file):
                picture = {}
                picture['filename'] = file
                picture['path'] = os.path.join(root, file)
                picture['thumbnail'] = generate_and_save_thumbnail(picture['path'], 120, 160, ".jpg")
                insert_picture(picture)
    print "Finished Importing pictures"
    

    
def is_image(file):
    for ext in image_exts:
        if ext in file: 
            return True
        
    return False  

def generate_and_save_thumbnail(imageFile, h, w, ext):
    logger.debug("generating thumbnail for file "+imageFile)
    image = Image.open(imageFile)
    image = image.resize((w, h), Image.ANTIALIAS)
    outFileLocation = "./thumbnails"
    outFile = outFileLocation + imageFile 
    dirname = os.path.dirname(outFile)
    if not os.path.exists(dirname):
        os.makedirs(dirname)        
    image.save(outFile)      
    return outFile