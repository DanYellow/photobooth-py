import tkinter as tk
import tkinter.font as tkFont
import os, PIL

import utils.colors

from classes.UiLiveview import UiLiveview

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Liveview(tk.Frame):
    def __init__(self, master, root,
        texts, camera = None, on_stream_ended = None, 
        display_time = 15,
        *args, **kwargs):
        
        self.texts = texts
        self.camera = camera
        self.root = root
        self.display_time = display_time
        self.on_stream_ended = on_stream_ended

        tk.Frame.__init__(self, master, *args, **kwargs, bg=utils.colors.mainBackgroundColor)

        self.create_widgets()

    def create_widgets(self):
        self.ui_liveview = UiLiveview(
                master = self, 
                width = int(self.root.winfo_width() * 0.72),
                root = self.root,
                camera = self.camera,
                on_stream_ended = self.on_stream_ended,
                display_time = self.display_time,
                bg = utils.colors.mainBackgroundColor
        )

        self.ui_liveview.pack(fill="x", expand=True, pady=2)

        start_btn_bgc = '#a1d4f0'
        start_btn_icon_src = PIL.Image.open(f"{ROOT_DIR}/../assets/camera-icon.png").convert("RGBA")
        start_btn_icon_src = start_btn_icon_src.resize((30, 30), PIL.Image.ANTIALIAS)
        start_btn_bgc_tmp = PIL.Image.composite(
            start_btn_icon_src,
            PIL.Image.new('RGB', start_btn_icon_src.size, start_btn_bgc),
            start_btn_icon_src
        )
        start_btn_icon = PIL.ImageTk.PhotoImage(start_btn_bgc_tmp)

        self.start_btn = tk.Button(
            self,
            height = 60,
            background=start_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=start_btn_bgc, 
            borderwidth=0,
            fg="white",
            image=start_btn_icon,
            text = self.texts['take_pict'].upper(),
            font=tkFont.Font(family='DejaVu Sans Mono', size=20),
            compound="left"
        )
        self.start_btn.image = start_btn_icon
        self.start_btn.pack(expand=True, pady=2)