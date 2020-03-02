import tkinter as tk
import tkinter.font as tkFont

from classes.UiLiveview import UiLiveview

class Liveview(tk.Frame):
    def __init__(self, master, texts, stream = None, *args, **kwargs):
        self.texts = texts
        self.camera_stream = stream

        tk.Frame.__init__(self, master, *args, **kwargs, bg="wheat") # , cursor="none"

        self.create_widgets()

    def create_widgets(self):
        ui_liveview = UiLiveview(
                master = self, 
                width = 600,
                camera_stream = self.camera_stream
        )

        ui_liveview.pack(fill="x", expand=True)

        start_btn_bgc = '#a1d4f0'
        self.start_btn = tk.Button(
            self,
            height = 2,
            background=start_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=start_btn_bgc, 
            borderwidth=0,
            fg="white",
            # image=start_btn_icon,
            text = self.texts['take_pict'].upper(),
            font=tkFont.Font(family='DejaVu Sans Mono', size=20),
            compound="left"
        )
        self.start_btn.pack(expand=True, pady=2)