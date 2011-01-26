import os
import logging
import Image   
from ExifTags import TAGS
from core import picturedb
import config

# create logger
logger = logging.getLogger(__name__)
  

image_exts = ['jpg', 'JPG', 'png', 'gif', 'tif', 'bmp', 'xpm']
EXIF_PARAMS = ['YResolution','ResolutionUnit','Make','Flash','DateTime','MeteringMode','XResolution','Orientation', 'ExposureTime', 'Model', 'ISOSpeedRatings', 'FNumber','FocalPlaneYResolution','FocalPlaneXResolution','FocalLength', 'DateTimeOriginal']
        


def get_pictures_insert_stmt(picture):
    return 'INSERT OR IGNORE INTO PICTURES ( filename, path, thumbnail, raw_exif, width, height, twidth, theight) VALUES (\'%(filename)s\',  \'%(path)s\', \'%(thumbnail)s\', \'%(raw_exif)s\', \'%(width)s\', \'%(height)s\', \'%(twidth)s\', \'%(theight)s\')' % \
                        picture

def get_tags_insert_sql(tagname):
    return 'INSERT OR IGNORE INTO TAGS (name) VALUES (\'%s\')' % tagname

def get_pictures_with_tag_sql(tagname):
    return 'SELECT * FROM PICTURES WHERE id IN (SELECT pictureid FROM PICTURETAGS WHERE tagid IN (SELECT id FROM TAGS WHERE name = \'%s\'))' % tagname
def get_picturetags_insert_sql(pictureid, tagname):
    return 'INSERT INTO PICTURETAGS (pictureid, tagid) VALUES ( %d, (SELECT ID FROM TAGS WHERE NAME = \'%s\'))' % (pictureid, tagname)

def get_tags_for_picture_sql(pictureid):
    return 'SELECT name FROM TAGS WHERE ID IN (SELECT TAGID FROM PICTURETAGS WHERE PICTUREID = \'%s\')' % pictureid
def select_pictures_sql():
    return 'SELECT * FROM PICTURES'

def get_pictures_with_tag_fragment_sql(text):
    return 'SELECT * FROM PICTURES WHERE id IN (SELECT pictureid FROM PICTURETAGS WHERE tagid IN (select id from tags where name like lower(\'%%%s%%\')))' % text

def get_picture_with_path_sql(path):
    return 'SELECT * FROM PICTURES WHERE path = \'%s\'' % path
def select_all_tags_sql():
    return 'SELECT * FROM TAGS'

def insert_picture(picture):
    connection = picturedb.get_connection()
    cursor = connection.cursor()
    cursor.execute(get_pictures_insert_stmt(picture))
    connection.commit()
    cursor.close()

def insert_tags(pictureids, tags):
    connection = picturedb.get_connection()
    cursor = connection.cursor()
    for tag in tags.split(','):
        tag = tag.strip()
        cursor.execute(get_tags_insert_sql(tag))
        for pictureid in pictureids:
            cursor.execute(get_picturetags_insert_sql(pictureid, tag))
    connection.commit()
    cursor.close()        

def get_pictures_from_db():
    logger.debug("Getting pictures from DB")
    picturedb.init_db()
    connection = picturedb.get_connection()
    cursor = connection.cursor()
    cursor.execute(select_pictures_sql())
    list = []
    for row in cursor:
        list.append(row)
    return list

def get_tags_from_db():
    return picturedb.execute_sql_select('SELECT name FROM TAGS')
    

def get_tags_for_picture(pictureid):
    list  = []
    for tuple in picturedb.execute_sql_select(get_tags_for_picture_sql(pictureid)):
        list.append(tuple[0])
    return list

def get_pictures_with_tag(tagname):
    return picturedb.execute_sql_select(get_pictures_with_tag_sql(tagname))
 
def search_pictures_by_text(text):
    return picturedb.execute_sql_select(get_pictures_with_tag_fragment_sql(text))  
    
def is_picture_in_db(path):
    if not picturedb.execute_sql_select(get_picture_with_path_sql(path)):
        return False
    else:
        return True   
      

    
def is_image(file):
    for ext in image_exts:
        if ext in file: 
            return True
        
    return False  

def generate_and_save_thumbnail(image, imageFile, ext, picture):
    width = config.THUMB_SIZE * image.size[0] / max(image.size)
    height = config.THUMB_SIZE * image.size[1] / max(image.size)
    image = image.resize((width, height), Image.ANTIALIAS)
    picture['twidth'] = width
    picture['theight'] = height
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
    try:
        info = i._getexif()
        if (info == None):
            logger.debug("No exif information found for file: " + imageFile)
            return
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    except AttributeError:
        logger.debug("No exif information found for file: " + imageFile)
        return


def parse_db_exif(db_exif):
    exif = {}
    for pair_str in db_exif.split('%%'):
        if pair_str != '':
            pair = pair_str.split('##')
            exif[pair[0]] = pair[1]
    return exif