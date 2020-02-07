import glob
import os
import tkinter as tk

from math import ceil
from PIL import Image, ImageTk, ImageFile, ImageFilter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Gallery(tk.Frame):
    def load(self):

        COLUMNS = ceil(self.root.winfo_width() / 150)
        image_count = 0
        for infile in glob.glob(os.path.join(f"{ROOT_DIR}/../../_tmp/", '*.JPG')):
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)

            img = Image.open(infile)
            resized = img.resize((150, 100), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2))
            tkimage = ImageTk.PhotoImage(resized)
            img_container = tk.Label(self, image=tkimage)
            img_container.image = tkimage

            img_container.grid(row=r, column=c)
            
            self.grid_rowconfigure(r, pad=0)
            self.grid_columnconfigure(c, pad=0)

    def __init__(self, master=None, root=None, bg="white"):
        tk.Frame.__init__(self, master, image = None, bg = bg)
    
        self.master = master
        self.root = root

        root.update()

        self.load()
        
