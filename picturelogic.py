import gtk
import gobject
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
          self.addTagsDialog = self.builder.get_object("addtags_dialog")
          dic = {
                 "on_quit_menuitem_activate" : self.close,
                 "on_about_menuitem_activate" : self.about,
                 "on_import_folder_activate": self.importFolder,
                 "on_importfolder_ok_button_clicked": self.doImportFolder,
                 "on_open_image_activate": self.openImage,
                 "on_search_button_clicked" : self.search,
                 "on_pictures_iconview_item_activated" : self.iconview_item_activated,
                 "on_pictures_iconview_selection_changed" : self.iconview_selection_changed,
                 "on_pictures_iconview_button_press_event": self.iconview_button_press_events,
                 "on_addtags_cancel_button_clicked": self.addTagsDialog_destroy,
                 "on_addtags_ok_button_clicked": self.doAddTags
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
        self.pictures_store = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_INT)
        self.iconView.set_model(self.pictures_store)
        self.iconView.set_pixbuf_column(0)
        self.iconView.set_text_column(1)
        self.pictures = get_pictures_from_db()
        if self.pictures == []:
            return
        for picture in self.pictures:
            pixbuf = gtk.gdk.pixbuf_new_from_file(picture[0])
            self.pictures_store.append([pixbuf,picture[2], picture[0], picture[3]])
        
    def search(self,widget):
        pass
    
    def iconview_item_activated(self,widget, item):
        logger.debug("item activated: "+self.pictures_store[item][1])
        pass
    
    def iconview_selection_changed(self, widget):
        for item in self.iconView.get_selected_items():
            logger.debug("item selected: "+self.pictures_store[item][1])
        
        pass
        
    def iconview_button_press_events(self,widget, event):      
        item = self.iconView.get_path_at_pos(event.x, event.y)
        if (event.button == 3 and item != None ):  
          logger.debug("item where right click ocurred: "+self.pictures_store[item][1])
          self.iconView.select_path(item)
          self.iconMenu = gtk.Menu()
          addTagsItem = gtk.MenuItem("Add tags")
          addTagsItem.connect("activate", self.addTags)
          removeTagsItem = gtk.MenuItem("Remove tags")
          self.iconMenu.append(addTagsItem)
          self.iconMenu.append(removeTagsItem)
          self.iconMenu.popup(None, None, None, event.button, event.time, None)
          self.iconMenu.show_all()
    def addTags(self, widget):
        self.addTagsDialog.show()
        
    def doAddTags(self, widget):
        logger.debug("Adding tags to pictures selected")
        selectedItems = self.iconView.get_selected_items()
        pictureids = []
        for item in selectedItems:
            pictureids.append(self.pictures_store[item][3])
        addtagsEntry = self.builder.get_object("addtags_entry")
        selectedTags = addtagsEntry.get_text()
        if selectedTags != '':
            insert_tags(pictureids, selectedTags)
        self.addTagsDialog_destroy(self,widget)
    def addTagsDialog_destroy(widget):
        logger.debug("Destroying add tags dialog")
        self.addTagsDialog.destroy()
class About:
    
    def __init__(self, builder):
        
        self.window = builder.get_object("aboutdialog")
        self.window.show()
            
    
PictureLogic()
gtk.main()   
    