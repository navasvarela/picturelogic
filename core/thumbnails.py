'''
Created on 20 Jan 2011

@author: juan
'''

import os
from threading import Thread
import logging
import pictures
import Image
import gobject

# create logger
logger = logging.getLogger(__name__)

class ThumbsWorker(Thread):
    
    def __init__(self, path, label, callback):
        Thread.__init__(self)
        self.label = label
        self.path = path
        logger.debug("Setting callback to:")
        logger.debug(callback)
        self.callback = callback
    
    def run(self):
        logger.debug("processing thumbnails for path " + self.path)
        for root, dirs, files in os.walk(self.path):
            for image_file in files:
                image_path = os.path.join(root.replace(':', ''), image_file)
                if pictures.is_picture_in_db(image_path):
                    continue
                logger.debug("Processing %s" % image_file)
                if pictures.is_image(image_file):
                    picture = {}
                    picture['filename'] = image_file
                    
                    gobject.idle_add(self.label.set_text,'Processing: ' + image_file) 
                                                                  
                    picture['path'] = image_path
                    image = Image.open(picture['path'])
                    picture['width'] = image.size[0]
                    picture['height'] = image.size[1]
                    picture['thumbnail'] = pictures.generate_and_save_thumbnail(image, picture['path'], ".jpg", picture)
                    exif = pictures.get_exif(picture['path'])
                    exif_str = ''
                    if exif != None:
                        for tag in pictures.EXIF_PARAMS:
                            if exif[tag] != '':
                                if isinstance(exif[tag], (list, tuple)):
                                    exif[tag] = "%d / %d" % (exif[tag][0] , exif[tag][1])
                                if isinstance(exif[tag], (int, long)):
                                    exif[tag] = "%d" % exif[tag]
                                exif_str += '%%' + tag + '##' + exif[tag] 
                    picture['raw_exif'] = exif_str
                    pictures.insert_picture(picture)
       
        gobject.idle_add(self.label.set_text,"Finished Importing pictures")
        self.callback()
        

def import_from_folder(path, widget, callback):
    worker = ThumbsWorker(path, widget, callback)
    worker.start()

    
    
    
    
    
    
