import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import os, PIL

import utils.colors

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Result(tk.Frame):
    def __init__(self, master, root, texts, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, bg=utils.colors.mainBackgroundColor) # , cursor="none"
        
        self.root = root
        self.texts = texts
        self.is_fullscreen = False

        self.root.update()
        self.create_widgets()

    def create_widgets(self):
        btns_container = self.create_btns_container()
        self.collage_container = self.create_collage_container()
        self.fullscreen_collage = self.create_fullscreen_collage_ui()

        self.collage_container.pack(side="top", pady=(15, 0))
        self.collage_container.pack_propagate(0)

        btns_container.pack(side="top", fill="x", expand=True, pady=(15, 0), padx=40)

    def create_btns_container(self):
        btns_container = tk.Frame(
            self,
            bg = self["bg"],
        )

        btns_container_btns_height = 1
        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=20)

        print_btn_bgc = '#a1d4f0'
        self.print_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background=print_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=print_btn_bgc, 
            borderwidth=0,
            fg=utils.colors.mainButtonTxtColor,
            text = self.texts['print'].upper(),
            font=btns_container_font_style,
        )
        self.print_btn.pack(side="left", pady=(0, 8), ipadx=30, ipady=5)

        continue_btn_bgc = '#e67e22'
        self.continue_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background=continue_btn_bgc,
            highlightthickness=2,
            activeforeground="#f2a560",
            activebackground=continue_btn_bgc,
            highlightbackground="#f2a560",
            borderwidth=0,
            fg=utils.colors.mainButtonTxtColor,
            text = self.texts['continue'].upper(),
            font=btns_container_font_style,
        )

        self.continue_btn.pack(side="right", pady=(0, 8), ipadx=30, ipady=5)

        return btns_container

    def create_collage_container(self):
        collage_label = tk.Button(self, 
            bg=self['bg'],
            activebackground=self['bg'],
            relief="flat",
            overrelief="flat",
            borderwidth=0,
            height=round(self.root.winfo_height() * 0.80),
            command=self.toggle_fullscreen_collage,
            highlightthickness=0,
        )

        return collage_label

    def create_fullscreen_collage_ui(self):
        collage_label = tk.Button(self, 
            activebackground="black",
            relief="flat",
            overrelief="flat",
            borderwidth=0,
            bg = utils.colors.mainBackgroundColor,
            height = self.root.winfo_height(),
            command = self.toggle_fullscreen_collage
        )

        return collage_label

    def toggle_fullscreen_collage(self):
        bools = [True, False]

        if(self.is_fullscreen):
            self.fullscreen_collage.place_forget()
            self.configure(bg=utils.colors.mainBackgroundColor)
        else:
            self.fullscreen_collage.place(
                relx=0.5, rely=0.5,
                anchor="center",
                relheight=1.0, relwidth=1.0
            )
            self.configure(bg=utils.colors.mainBackgroundColor)
        self.is_fullscreen = bools[self.is_fullscreen]

    def set_collage_image(self, collage_path):
        collage_src = PIL.Image.open(collage_path)
        print(self.collage_container['width'] )
        collage_src.thumbnail((self.root.winfo_height()* 0.80, self.root.winfo_height() * 0.80))
        collage = PIL.ImageTk.PhotoImage(collage_src)

        self.collage_container.configure(image=collage)
        self.collage_container.image = collage

    def set_fullscreen_collage_image(self, collage_path):
        collage_src = PIL.Image.open(collage_path)
        collage_src.thumbnail((self.root.winfo_height(), self.root.winfo_height()))
        collage = PIL.ImageTk.PhotoImage(collage_src)

        self.fullscreen_collage.configure(image=collage)
        self.fullscreen_collage.image = collage