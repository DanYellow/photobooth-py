import glob
import os

from tkinter import Frame, Label
from PIL import Image, ImageTk, ImageFile, ImageFilter

class Gallery(Frame):
    def load(self):
        COLUMNS = 4
        image_count = 0

        for infile in glob.glob(os.path.join("_tmp/", '*.JPG')):
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)

            img = Image.open(infile)
            resized = img.resize((150, 100), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2))
            tkimage = ImageTk.PhotoImage(resized)
            img_container = Label(self, image=tkimage)
            img_container.image = tkimage

            img_container.grid(row=r, column=c)

            self.grid_rowconfigure(r, pad=0)
            self.grid_columnconfigure(c, pad=0)

    def __init__(self, master=None):
        bgc = 'white'
        Frame.__init__(self, master, image = None, bg = bgc)
        self['bg'] = bgc

        self.load()
        
