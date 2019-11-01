from tkinter import *

class Countdown(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.label = Label(self, text="2000", width=10)
        self.remaining = 0

        self.pack()

    def countdown(self, remaining = None, thread = None):
        if remaining is not None:
            self.remaining = remaining

        
        if self.remaining <= 0:
            self.label.configure(text="time's up!")
            if thread is not None:
                thread.set()
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            print(self.remaining)
            self.after(1000, self.countdown)


    def reset(self):
        self.remaining = 0

    
