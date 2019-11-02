from tkinter import Label, Frame
from functools import partial
import threading

class Countdown(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.label = Label(self, text="HHE", fg="black", font=(None, 25))
        self.remaining = None
        self.callback = None

        self.pack()

    def countdown(self, remaining = None, callback = None):
        if remaining is not None:
            self.remaining = remaining

        if callback is not None:
            self.callback = callback

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
            if self.callback is not None:
                threading.Timer(0.01,  self.callback).start()
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

