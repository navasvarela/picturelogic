'''
Created on 20 Jan 2011

@author: juan
'''

from multiprocessing import Process
import logging

# create logger
logger = logging.getLogger(__name__)

def process_thumbnails(path, widget):
    logger.debug("process thumbnails for path " + path)
    pass

def import_from_folder(path, widget):
    process = Process(target=process_thumbnails, args=(path, widget))
    process.start()
