from tkinter import Label, Frame, Canvas
from functools import partial
import threading
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

class Countdown(Canvas):
    def __init__(self, master=None):
        self.delta_y = 2
        self.width_children = 100
        self.canvas_width = 600

        Canvas.__init__(self, master=master, width=self.canvas_width, height=self.width_children, bg="red")
        self.master = master
        self.labels_container = Canvas(self, width=self.canvas_width, height=1000)
        self.labels_container_window = self.create_window(0, 0, window=self.labels_container, anchor="nw")

        self.remaining = None
        self.callback = None
        self.animation_speed = 100

    def generate_ui(self, nb_takes):
        for x in range(nb_takes, -1, -1):
            lbl_countdown = x if x != 0 else 'Posez !'

            widget = Label(
                self.labels_container,
                text = lbl_countdown,
                fg = 'black',
                font = ("courier", int(self.width_children * 0.625), "bold"),                                                
                borderwidth = 0,
                anchor="nw"
            )

            if x == 0:
                widget.config(fg="red")

            y_position = (self.width_children * (nb_takes - x)) + ((self.delta_y * 2) * (nb_takes - x)) 

            self.labels_container.create_window(
                (self.canvas_width / 2),
                y_position + (self.width_children / 2) + self.delta_y, 
                window=widget,
                height=self.width_children,
                anchor="center"
            )

    def countdown(self, remaining = None, callback = None):
        if remaining is not None:
            # self.pack()
            self.remaining = remaining

        if callback is not None:
            self.callback = callback

        y_move = -(self.width_children + (self.delta_y * 2))
        self.move(self.labels_container_window, 0, y_move / self.animation_speed)
         
        if self.remaining <= 0:
            self.coords(self.labels_container_window, 0, 0)
            if self.callback is not None:
                # threading.Timer(0.01, self.callback).start()
                self.callback()
        else:
            self.remaining = self.remaining - (1 / self.animation_speed)
            self.after(int(1000 / self.animation_speed), self.countdown)

