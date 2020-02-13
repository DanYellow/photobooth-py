import glob
import os
import tkinter as tk

from math import ceil
from PIL import Image, ImageTk, ImageFile, ImageFilter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiGallery(tk.Frame):
    def create_widgets(self):
        thumb_width = 150
        thumb_height = 100
        NB_COLUMNS = ceil(self.root.winfo_width() / thumb_width)
        NB_ROWS = ceil(self.root.winfo_height() / thumb_height)

        image_count = 0
        list_images = glob.glob(os.path.join(f"{ROOT_DIR}/../../_tmp/", '*.JPG'))[:NB_ROWS*NB_COLUMNS]

        for infile in reversed(list_images):
            image_count += 1
            r, c = divmod(image_count - 1, NB_COLUMNS)

            img = Image.open(infile)
            resized = img.resize((thumb_width, thumb_height), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2))
            tkimage = ImageTk.PhotoImage(resized)
            img_container = tk.Label(self, image=tkimage)
            img_container.image = tkimage

            img_container.grid(row=r, column=c)
            
            self.grid_rowconfigure(r, pad=0)
            self.grid_columnconfigure(c, pad=0)
    
    def update(self):
        for child in list(self.winfo_children()):
            child.grid_forget()
        self.create_widgets()

    def __init__(self, master=None, root=None, bg="white"):
        tk.Frame.__init__(self, master, image = None, bg = bg)
    
        self.master = master
        self.root = root

        self.root.update()
        self.create_widgets()
