import unittest
from core import pictures


class TestPictures(unittest.TestCase):
    
    
    def test_get_pictures_insert_stmt(self):
        picture = { 'filename':'picture1file','path':'/tmp/pictureone'}
        insert_stmt = pictures.get_pictures_insert_stmt(picture)
        print insert_stmt
        for key in picture.keys():
            print "testing key: "+key
            self.assertTrue(picture[key] in insert_stmt)
             
        
    
        
      

