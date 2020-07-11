import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import os, PIL

import utils.colors

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Loading(tk.Frame):
    def __init__(self, master, texts, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, bg=utils.colors.mainBackgroundColor) # , cursor="none"
        
        self.texts = texts

        self.create_widgets()

    def create_widgets(self):
        group = tk.LabelFrame(
            self, 
            text=None, 
            padx=5, 
            pady=5, 
            bg=self["bg"], 
            borderwidth=0
        ) 
        group.place(relx=0.5, rely=0.5, anchor="center")

        self.countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=50
        )

        image = PIL.Image.open(f"{ROOT_DIR}/../assets/loading-icon.png")
        photo = PIL.ImageTk.PhotoImage(image)

        label = tk.Label(group, image=photo, bg=self["bg"])
        label.image = photo
        label.pack(side="left", padx=(0, 15))
        
        loading_label = tk.Label(
            group, 
            text=self.texts["loading"],
            font = self.countdown_label_style,
            bg=self["bg"],
        )
        loading_label.pack(side="left")

        
        
