import gtk
from pictures import *
import logging
import logging.config 
from config import *

# create logger
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger("picturelogic")

    
class PictureLogic:
    def close(self, widget):
        logger.info("Exiting picturelogic")
        gtk.main_quit()
        
          
    def __init__(self):
          self.builder = gtk.Builder()
          self.builder.add_from_file("gui/gui.glade")
          self.window = self.builder.get_object("window1")
          self.window.show()
          dic = {
                 "on_quit_menuitem_activate" : self.close,
                 "on_about_menuitem_activate" : self.about,
                 "on_import_folder_activate": self.importFolder,
                 "on_importfolder_ok_button_clicked": self.doImportFolder,
                 "on_open_image_activate": self.openImage,
                 "on_search_button_clicked" : self.search
                 }
          self.builder.connect_signals(dic)
          self.iconView = self.builder.get_object("pictures_iconview")
          self.refresh_images()
          
          
    def about(self,widget):
        self.about = About(self.builder)
        
    def importFolder(self,widget):
        self.importFolderDialog = self.builder.get_object("importfolderdialog")
        self.importFolderDialog.show()
    def doImportFolder(self,widget):
        
        self.folder = self.importFolderDialog.get_filename()
        logger.debug("Import all pictures from folder: "+self.folder)
        # Close import dialog
        self.importFolderDialog.hide()
        #1 Import images from folder recursively
        
        import_from_folder(self.folder)
        
        #2 Display images using gtk icon view
        self.refresh_images()
    def openImage(self,widget):
        self.openImageDialog = self.builder.get_object("openimagedialog")
        self.openImageDialog.show()
    def refresh_images(self):
        self.pictures_store = gtk.ListStore(gtk.gdk.Pixbuf)
        self.iconView.set_model(self.pictures_store)
        self.iconView.set_pixbuf_column(0)
        self.pictures = get_pictures_from_db()
        if self.pictures == []:
            return
        for picture in self.pictures:
            print picture
            pixbuf = gtk.gdk.pixbuf_new_from_file(picture[0])
            self.pictures_store.append((pixbuf,))
        
    def search(self,widget):
        pass
        
class About:
    
    def __init__(self, builder):
        self.builder = builder
        self.window = builder.get_object("aboutdialog")
        self.window.show()
            

PictureLogic()
gtk.main()   
    