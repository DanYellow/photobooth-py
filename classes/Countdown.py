from tkinter import Label, Frame, Canvas
from PIL import Image, ImageTk, ImageFile
from functools import partial
import threading
import os
import sys
import shutil

shutil.which("gs")
ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

class Countdown(Canvas):
    def __init__(self, master=None):
        self.delta_y = 2
        self.width_children = 80

        Canvas.__init__(self, master=master, width=300, height=self.width_children)
        self.master = master
        self.labels_container = Canvas(self, width=300, height=1000)
        self.labels_container_window = self.create_window(0, self.width_children / 2, window=self.labels_container, anchor="nw")

        self.remaining = None
        self.callback = None
        self.animation_speed = 100

    def generate_ui(self, nb_takes):
        img = ImageTk.PhotoImage(Image.open(f"""{ROOT_DIR}/chat.tmp.jpg"""), size=30)
        # img = ImageTk.PhotoImage(Image.open(f"""{ROOT_DIR}/photo-icon.png"""), size=30)

        # label = Label(image=img)

        label = Label(self.labels_container, image=img)
        self.labels_container.create_window(125,10, window=label)

        for x in range(nb_takes, -1, -1):
            lbl_countdown = x if x != 0 else 'Posez !'

            widget = Label(
                self,
                text = lbl_countdown,
                fg = 'black',
                font = ("courier", 50, "bold"),                                                
                borderwidth = 0,
                anchor="nw",
                # image=img,
            )

            if x == 0:
                # widget.config(image=img)
                print(img)
                widget.config(text="0", fg="red")

            y_position = (self.width_children * (nb_takes - x)) + ((self.delta_y * 2) * (nb_takes - x))
            self.labels_container.create_window(
                (300 / 2),
                y_position + 1, 
                window=widget,
                height=self.width_children,
                anchor="center"
            )

        # self.countdown(remaining=5)

    def countdown(self, remaining = None, callback = None):
        if remaining is not None:
            self.pack()
            self.remaining = remaining

        if callback is not None:
            self.callback = callback

        y_move = -(self.width_children + (self.delta_y * 2))
        self.move(self.labels_container_window, 0, y_move / self.animation_speed)
         
        if self.remaining <= 0:
            self.coords(self.labels_container_window, 0, self.width_children / 2)
            if self.callback is not None:
                # threading.Timer(0.01, self.callback).start()
                # self.pack_forget()
                self.callback()
        else:
            self.remaining = self.remaining - (1 / self.animation_speed)
            self.after(int(1000 / self.animation_speed), self.countdown)

