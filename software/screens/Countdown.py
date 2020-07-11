import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont

import datetime
import time
import utils.colors

class Countdown(tk.Frame):
    def __init__(self, master, root, texts, callback=None, start_count=3,  *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, background=utils.colors.mainBackgroundColor) # , cursor="none"

        self.root = root
        self.texts = texts
        self.init_start_count = start_count
        self.count = start_count
        self.callback = callback
        self.has_liveview = False

        self.debug_counter = 0
        
        self.animation_speed = 100 # 250
        self.animation = None
        self.max_angle = 359.9999
        self.angle_offset = float((359.9999 * self.animation_speed) / (start_count * 1000))
        
        self.countpics_label_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        circle_canvas_container_width = 400
        circle_canvas_container_height = circle_canvas_container_width

        self.circle_canvas_container = tk.Canvas(
            self,
            background=utils.colors.mainBackgroundColor,
            borderwidth=0,
            width=circle_canvas_container_width,
            height=circle_canvas_container_height,
            highlightthickness=0,
        )
        
        self.circle_canvas = self.circle_canvas_container.create_arc(
            0, 0, 
            circle_canvas_container_width - 10, circle_canvas_container_height - 10,
            style="arc",
            outline="white",
            width=3,
            start=0,
            extent=0, 
        )

        self.circle_canvas_container.place(
            relx=0.5, rely=0.5,
            anchor="center",
        )

        self.init_size = 70
        self.countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=self.init_size 
        )
        
        countdown_label_bg = self['background']
        self.countdown_label = tk.Label(self, 
            background=countdown_label_bg,
            borderwidth=0,
            text=self.count,
            font = self.countdown_label_style,
            fg="white",
        )

        self.countdown_label.place(
            relx=0.5, rely=0.5,
            anchor="center",
        )

        countpics_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=15
        )
        countpics_label = tk.Label(self, background=self["bg"],
            borderwidth=0,
            textvariable=self.countpics_label_var,
            fg="white",
            font = countpics_label_style)

        countpics_label.pack(side="bottom", expand=0, fill="x", pady=((0, 15)))

    def start_countdown(self, photocount = None, maxcount = None, skip = False):
        self.skip = skip
        if photocount is not None:
            self.countpics_label_var.set('Photo {}/{}'.format(photocount, maxcount))
        
        if(self.skip == False):
            self.countdown_circle_anim()

        self.countdown()

    def countdown(self):
        if self.skip == False and self.count > 0:
            self.countdown_label_style.configure(
                size=self.init_size
            )
            self.countdown_label.configure(
                text = self.count,
                font = self.countdown_label_style
            )
            # print("start", datetime.datetime.now())
            self.debug_counter = 0

            self.count = self.count - 1
            self.root.after(1000, self.countdown)            
        else:
            self.countdown_label_style.configure(
                size=70
            )
            self.countdown_label.configure(
                text=self.texts["cheese"],
                font = self.countdown_label_style
            )

            if self.callback is not None:
                self.on_countdown_end()
    
    def on_countdown_end(self):
        self.callback()

    def countdown_circle_anim(self):
        circle_angle = float(self.circle_canvas_container.itemcget(self.circle_canvas, "extent"))
        self.debug_counter = self.debug_counter + 1
        if self.count >= 0 and circle_angle < self.max_angle:
            self.circle_canvas_container.itemconfigure(
                self.circle_canvas, 
                extent=circle_angle + self.angle_offset
            )
            self.animation = self.root.after(self.animation_speed, self.countdown_circle_anim)
        else:
            print("----- self.debug_counter", self.debug_counter)
            print(float(self.circle_canvas_container.itemcget(self.circle_canvas, "extent")))
            
            self.root.after_cancel(self.animation)

    def reset(self):
        self.debug_counter = 0
        self.count = self.init_start_count
        self.circle_canvas_container.itemconfigure(self.circle_canvas, extent=0, start=0)
        
        if self.animation is not None:
            self.root.after_cancel(self.animation)
