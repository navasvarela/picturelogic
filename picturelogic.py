import gtk
    
class PictureLogic:
    def close(self, widget):
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
                 "on_open_image_activate": self.openImage
                 }
          self.builder.connect_signals(dic)
          
    def about(self,widget):
        self.about = About(self.builder)
        
    def importFolder(self,widget):
        self.importFolderDialog = self.builder.get_object("importfolderdialog")
        self.importFolderDialog.show()
    def openImage(self,widget):
        self.openImageDialog = self.builder.get_object("openimagedialog")
        self.openImageDialog.show()
class About:
    
    def __init__(self, builder):
        self.builder = builder
        self.window = builder.get_object("aboutdialog")
        self.window.show()
            

PictureLogic()
gtk.main()   
    