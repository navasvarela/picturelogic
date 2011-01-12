import os
import logging
import logging.config 
from config import * 
import Image 
import picturedb   
from ExifTags import TAGS
from picturedb import get_connection, init_db


# create logger
logging.config.fileConfig(LOGGING_CONF) #@UndefinedVariable
logger = logging.getLogger("pictures")
  

image_exts = ['jpg', 'JPG', 'png', 'gif', 'tif', 'bmp', 'xpm']
EXIF_PARAMS = ['YResolution','ResolutionUnit','Make','Flash','DateTime','MeteringMode','XResolution','Orientation', 'ExposureTime', 'Model', 'ISOSpeedRatings', 'FNumber','FocalPlaneYResolution','FocalPlaneXResolution','FocalLength', 'DateTimeOriginal']
        


def get_pictures_insert_stmt(picture):
    return 'INSERT INTO PICTURES ( filename, path, thumbnail, raw_exif) VALUES (\'%(filename)s\',  \'%(path)s\', \'%(thumbnail)s\', \'%(raw_exif)s\')' % \
                        picture

def get_tags_insert_sql(tagname):
    return 'INSERT OR IGNORE INTO TAGS (name) VALUES (\'%s\')' % tagname

def get_pictures_with_tag_sql(tagname):
    return 'SELECT * FROM PICTURES WHERE pictureid IN (SELECT pictureid FROM PICTURETAGS WHERE tagid IN (SELECT tagid FROM TAGS WHERE name = \'%s\'))' % tagname
def get_picturetags_insert_sql(pictureid, tagname):
    return 'INSERT INTO PICTURETAGS (pictureid, tagid) VALUES ( %d, (SELECT ID FROM TAGS WHERE NAME = \'%s\'))' % (pictureid, tagname)

def select_pictures_sql():
    return 'SELECT * FROM PICTURES'

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
        cursor.execute(get_tags_insert_sql(tag))
        for pictureid in pictureids:
            cursor.execute(get_picturetags_insert_sql(pictureid, tag))
    connection.commit()
    cursor.close()        

def get_pictures_from_db():
    init_db()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(select_pictures_sql())
    list = []
    for row in cursor:
        list.append(row)
    return list

def get_tags_from_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM TAGS')
    list = []
    for tag in cursor:
        list.append(tag)
    return list

def get_pictures_with_tag(tagname):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(get_pictures_with_tag_sql(tagname))
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
                exif_str = ''
                for tag in EXIF_PARAMS:
                    if exif[tag] != '':
                        if isinstance(exif[tag], (list,tuple)):
                            exif[tag] = "%d / %d" % (exif[tag][0] ,exif[tag][1])
                        if isinstance(exif[tag],(int,long)):
                            exif[tag] = "%d" % exif[tag]
                        print exif[tag]
                        exif_str += '%%' + tag + '##'+ exif[tag] 
                picture['raw_exif'] = exif_str
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
    print ret
    return ret

def parse_db_exif(db_exif):
    exif = {}
    for pair_str in db_exif.split('%%'):
        if pair_str != '':
            pair = pair_str.split('##')
            print pair
            exif[pair[0]] = pair[1]
    return exif