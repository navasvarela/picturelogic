import os
from sqlite3 import *

image_exts = ['jpg','png','gif','tif','bmp','xpm']
        
def get_connection():
    return connect('../db/picturelogic.db')

def get_pictures_insert_stmt(picture):
    return 'INSERT INTO PICTURES ( filename, path) VALUES (\'%(filename)s\',  \'%(path)s\')' % \
                        picture

def insert_picture(picture):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(get_pictures_insert_stmt(picture))
    connection.commit()
    cursor.close()


def import_from_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if is_image(file):
                picture = {}
                picture['filename'] = file
                picture['path'] = os.path.join(root,file)
                insert_picture(picture)
    
def is_image(file):
    for ext in image_exts:
        if ext in file: 
            return True
        
    return False        