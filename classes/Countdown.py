from tkinter import Label, Frame, Canvas
from functools import partial
import threading

class Countdown(Canvas):
    def __init__(self, master=None):
        self.delta_y = 2
        self.width = 50

        Canvas.__init__(self, master=master, width=300, height=self.width, bg='blue')
        
        self.labels_container = Canvas(self, width=300, height=1000, bg='red')
        self.labels_container_window = self.create_window(0, 0, window=self.labels_container, anchor="nw")

        nb_items = 3
        for x in range(nb_items, -1, -1):
            lbl_countdown = x if x != 0 else 'Posez !'
            widget = Label(
                self,
                text = lbl_countdown,
                fg = 'white',
                bg = 'black',
                font = ("courier", 35, "bold"),
                borderwidth = 0
            )  

            y_position = (self.width * (nb_items - x)) + ((self.delta_y * 2) * (nb_items - x))
            self.labels_container.create_window(
                0,
                y_position + 1,
                window=widget,
                height=self.width,
                anchor="nw"
            )

        self.remaining = None
        self.callback = None
        self.animation_speed = 10

    def countdown(self, remaining = None, callback = None):
        if remaining is not None:
            self.pack()
            self.remaining = remaining

        if callback is not None:
            self.callback = callback

        y_move = -(self.width + (self.delta_y * 2)) / self.animation_speed
        self.move(self.labels_container_window, 0, y_move)
        if self.remaining <= 0:
            if self.callback is not None:
                self.coords(self.labels_container_window, 0, 0)
                # threading.Timer(0.01, self.callback).start()
                # self.pack_forget()
                self.callback()
        else:
            self.remaining = self.remaining - (1 / self.animation_speed)
            self.after(int(1000 / self.animation_speed), self.countdown)

