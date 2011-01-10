import os
import logging
import logging.config 
from sqlite3 import *
from config import * 
import Image    
from ExifTags import TAGS


# create logger
logging.config.fileConfig(LOGGING_CONF) #@UndefinedVariable
logger = logging.getLogger("pictures")
  

image_exts = ['jpg', 'JPG', 'png', 'gif', 'tif', 'bmp', 'xpm']
        
def get_connection():
    print "Connecting to DB: " + DB_FILE   #@UndefinedVariable
    return connect(DB_FILE)  #@UndefinedVariable

def execute_sql(sql):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()

def get_pictures_insert_stmt(picture):
    return 'INSERT INTO PICTURES ( filename, path, thumbnail) VALUES (\'%(filename)s\',  \'%(path)s\', \'%(thumbnail)s\')' % \
                        picture

def get_tags_insert_stmt(tagname):
    return 'INSERT OR IGNORE INTO TAGS (name) VALUES (\'%s\')' % tagname

def get_picturetags_insert_stmt(pictureid, tagname):
    return 'INSERT INTO PICTURETAGS (pictureid, tagid) VALUES ( %d, (SELECT ID FROM TAGS WHERE NAME = \'%s\'))' % (pictureid, tagname)

def select_pictures_stmt():
    return 'SELECT * FROM PICTURES'

def get_insert_exifs_stmt(exif, picture_path):
    return 'INSERT INTO EXIFS (pictureid, date, exposure, size) VALUES((SELECT ID FROM PICTURES WHERE PATH = \'%s\'), '

def insert_picture(picture):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(get_pictures_insert_stmt(picture))
    connection.commit()
    cursor.close()

def insert_tags(pictureids, tags):
    connection = get_connection()
    cursor = connection.cursor()
    for tag in tags.split(','):
        tag = tag.strip()
        cursor.execute(get_tags_insert_stmt(tag))
        for pictureid in pictureids:
            cursor.execute(get_picturetags_insert_stmt(pictureid, tag))
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
                exif = get_exif(picture['path'])
                print exif
                insert_picture(picture)
    logger.debug("Finished Importing pictures")
    

    
def is_image(file):
    for ext in image_exts:
        if ext in file: 
            return True
        
    return False  

def generate_and_save_thumbnail(imageFile, h, w, ext):
    logger.debug("generating thumbnail for file " + imageFile)
    image = Image.open(imageFile)
    image = image.resize((w, h), Image.ANTIALIAS)
    outFileLocation = "./thumbnails"
    outFile = outFileLocation + imageFile 
    dirname = os.path.dirname(outFile)
    if not os.path.exists(dirname):
        os.makedirs(dirname)        
    image.save(outFile)      
    return outFile

def get_exif(imageFile):
    logger.debug("extracting exif for file: " + imageFile)
    ret = {}
    i = Image.open(imageFile)
    info = i._getexif()
    if (info == None):
        logger.debug("No exif information found for file: " + imageFile)
        return
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
