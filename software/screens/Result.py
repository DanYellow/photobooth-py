import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import qrcode, os
import PIL

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Result(tk.Frame):
    def __init__(self, master, root, collage_path, texts, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs) # , cursor="none"
        
        self.root = root
        self.collage_path = collage_path
        self.texts = texts

        self.root.update()
        self.create_widgets()

    def create_widgets(self):
        btns_container = self.create_btns_container()
        collage_container = self.create_collage_container()

        collage_container.pack(side="top", pady=(15, 0))
        collage_container.pack_propagate(0)

        btns_container.pack(side="top", fill="x", expand=True, pady=(15, 0), padx=40)

    def create_btns_container(self):
        btns_container = tk.Frame(
            self,
            bg = self["bg"],
        )

        btns_container_btns_height = 1
        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=20)

        print_btn_bgc = '#a1d4f0'
        print_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background=print_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=print_btn_bgc, 
            borderwidth=0,
            fg="white",
            text = self.texts['print'].upper(),
            font=btns_container_font_style,
        )
        print_btn.pack(side="left", pady=(0, 8), ipadx=30, ipady=5)

        continue_btn_bgc = '#e67e22'
        continue_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background=continue_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=continue_btn_bgc, 
            borderwidth=0,
            fg="white",
            text = self.texts['continue'].upper(),
            font=btns_container_font_style,
        )

        continue_btn.pack(side="right", pady=(0, 8), ipadx=30, ipady=5)

        return btns_container

    def create_collage_container(self):
        collage_src = PIL.Image.open(self.collage_path)
        collage_src.thumbnail((self.root.winfo_width(), self.root.winfo_width()))
        collage = PIL.ImageTk.PhotoImage(collage_src)

        self.collage_label = tk.Button(self, 
            image=collage,
            bg=self['bg'],
            activebackground=self['bg'],
            relief="ridge",
            overrelief="flat",
            borderwidth=0,
            width=round(self.root.winfo_width() * 0.7),
        )
        self.collage_label.image = collage

        return self.collage_label
        