from tkinter import Label, Frame, Canvas
from functools import partial
import threading

class Countdown(Canvas):
    def __init__(self, master=None):
        self.delta_y = 2
        self.width = 50

        Canvas.__init__(self, master=master, width=300, height=width, bg='blue')
        
        self.labels_container = Canvas(self, width=300, height=1000, bg='red')
        self.labels_container_window = self.create_window(0, 0, window=self.labels_container, anchor="nw")

        
        for x in range(3):
            widget = Label(
                self,
                text = x,
                fg = 'white',
                bg = 'black',
                font = ("courier", 35, "bold"),
                borderwidth = 0
            )  

            self.labels_container.create_window(
                0,
                (width * x) + ((delta_y * 2) * x),
                window=widget,
                width=width,
                height=width,
                anchor="nw"
            )       

            # y1 = width + (width * x) + ((delta_y * 2) * x)
            # y0 = y1 - width

            # self.labels_container.create_rectangle(
            #     0,
            #     y0 + 0,
            #     width + 0,
            #     y1 + 0,
            #     fill = "blue"
            # )
        
        # label_text = ['3', '2', '1', "Photo !"]
        # self.label = self.create_text(
        #     0, 0,
        #     text='\n'.join(label_text), 
        #     anchor='nw',
        #     font=("courier", 35, "bold"),
        #     state="disabled",
        #     justify="center")
    
        # self.label_bg = self.create_rectangle(self.bbox(self.label),fill="red")
        # self.tag_lower(self.label_bg, self.label)

        self.remaining = None
        self.callback = None

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

        self.move(self.labels_container_window, 0, -(width * 2 + delta_y * 2 + 2))


        if self.remaining <= 0:
            self.coords(self.label, (0, 0))

            if self.callback is not None:
                threading.Timer(0.01, self.callback).start()
        else:
            # self.itemconfigure(self.label, text="%d" % self.remaining)
            # self.coords(self.label_bg, self.bbox(self.label))
            self.remaining = self.remaining - 1
            
            # self.animate()
            self.after(1000, self.countdown)

