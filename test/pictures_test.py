import unittest
from pictures import *


class TestPictures(unittest.TestCase):
    
    
    def test_get_pictures_insert_stmt(self):
        picture = { 'filename':'picture1file','path':'/tmp/pictureone'}
        insert_stmt = get_pictures_insert_stmt(picture)
        print insert_stmt
        for key in picture.keys():
            print "testing key: "+key
            self.assertTrue(picture[key] in insert_stmt)
             
    def test_import_from_folder(self):
        import_from_folder('/home/juan/Pictures/Photos')
        
    
        
      

