from tkinter import *
from functools import partial

class Countdown(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.label = Label(self, text="2000", width=10)
        self.remaining = 0
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
                self.callback()
        else:
            print(self.remaining)
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)


    def reset(self):
        self.remaining = 0

    
