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

    def create_rectangle(x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


    def __init__(self, master=None, root=None, bg="white"):
        tk.Frame.__init__(self, master, image = None, bg = bg)
    
        self.master = master
        self.root = root
        self.images = []

        self.root.update()
        self.load()

        self.canvas = tk.Canvas(width=300, height=200)
        self.canvas.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        # self.canvas.lower()

        def create_rectangle(x1, y1, x2, y2, **kwargs):
            if 'alpha' in kwargs:
                alpha = int(kwargs.pop('alpha') * 255)
                fill = kwargs.pop('fill')
                fill = root.winfo_rgb(fill) + (alpha,)
                image = Image.new('RGBA', (x2-x1, y2-y1), fill)
                self.images.append(ImageTk.PhotoImage(image))
                self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
            self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

        create_rectangle(0, 0, self.root.winfo_width(), 60, fill='blue', alpha=.5)
        # create_rectangle(0, 10, self.root.winfo_width(), self.root.winfo_height(), fill='blue')
        
        # self.create_rectangle(50, 50, 250, 150, fill='green')


        
