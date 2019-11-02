from tkinter import Label, Frame, Canvas
from functools import partial
import threading

class Countdown(Canvas):
    def __init__(self, master=None):
        Canvas.__init__(self, master=master, bg='yellow', width=300, height=350)
        self.grid(ipady=1000)

        label_text = ['3', '2', '1', "Photo !"]
        self.label = self.create_text(
            0, 0,
            text='\n'.join(label_text), 
            anchor='nw',
            font=("courier", 35, "bold"),
            state="disabled",
            justify="center")
    
        # self.label_bg = self.create_rectangle(self.bbox(self.label),fill="red")
        # self.tag_lower(self.label_bg, self.label)

        self.remaining = None
        self.callback = None
        self.countdown(3)

        self.pack()

    def animate(self):
        if self.remaining > 0:
            self.move(self.label, 0, -60)
            self.after(1000, self.animate)

    def countdown(self, remaining = None, callback = None):
        if remaining is not None:
            self.remaining = remaining

        if callback is not None:
            self.callback = callback

        self.move(self.label, 0, -53)

        if self.remaining <= 0:
            # self.itemconfigure(self.label, text="time's up!")
            # self.coords(self.label_bg, self.bbox(self.label))
            self.coords(self.label, (0, 0))

            threading.Timer(3, partial(self.countdown, remaining = 3)).start()
            if self.callback is not None:
                threading.Timer(0.01, self.callback).start()
        else:
            # self.itemconfigure(self.label, text="%d" % self.remaining)
            # self.coords(self.label_bg, self.bbox(self.label))
            self.remaining = self.remaining - 1
            
            # self.animate()
            self.after(1000, self.countdown)

