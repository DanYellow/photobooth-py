import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont

class Countdown(tk.Frame):
    def __init__(self, master, root, texts, callback=None, start_count=3, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, background="wheat") # , cursor="none"

        self.root = root
        self.texts = texts
        self.init_start_count = start_count
        self.count = start_count
        self.callback = callback

        self.create_widgets()
        

    def create_widgets(self):
        self.init_size = 20
        self.countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=self.init_size 
        )
        self.countdown_label = tk.Label(self, 
            background=self["bg"],
            borderwidth=0,
            text=self.count,
            font = self.countdown_label_style
        )

        self.countdown_label.pack(side="top", expand=1, fill="both")

    def start_countdown(self):
        self.countdown()
        self.countdown_font_size_anim()

    def countdown(self):
        if self.count > 0:
            self.countdown_label_style.configure(
                size=self.init_size
            )
            self.countdown_label.configure(
                text = self.count,
                font = self.countdown_label_style
            )
            self.root.after(1000, self.countdown)
            self.count = self.count-1
        else:
            self.countdown_label_style.configure(
                size=70
            )
            self.count = self.count-1
            self.countdown_label.configure(
                text=self.texts["cheese"],
                font = self.countdown_label_style
            )

            if self.callback is not None:
                self.on_countdown_end()
    
    def on_countdown_end(self):
        self.callback()

    def countdown_font_size_anim(self):
        if self.count >= 0:
            self.countdown_label_style.configure(
                size=self.countdown_label_style['size'] + 1
            )
            self.countdown_label.configure(
                font = self.countdown_label_style
            )
            self.root.after(1, self.countdown_font_size_anim)
    
    def reset(self):
        self.count = self.init_start_count
        self.countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=self.init_size 
        )
        self.countdown_label.configure(
            text=self.count,
            font = self.countdown_label_style
        )
