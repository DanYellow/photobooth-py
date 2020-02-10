import os, PIL, glob
import tkinter as tk
import tkinter.font as tkFont

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiNotification(tk.Canvas):
    def __init__(self, texts, master=None, bg="white"):
        tk.Canvas.__init__(self, master, width=220, height=120, bg=bg)
    
        self.master = master
        self.texts = texts

    def create_print_notification(self):
        self.place(relx=0.5, rely=0, anchor="n", y=-60)
        print_notification_container = tk.Frame(
            self, 
            text = None,
            padx = 5,
            pady = 5,
            bg = "#ddf1d1",
            borderwidth=2,
            relief="flat",
            highlightbackground="#64b747",
            highlightthickness=2,
            width=self['width'],
            height=60
        )
        print_notification_container.pack_propagate(0)

        self.create_window(0, 0, 
            window=print_notification_container, 
            anchor="nw", 
            tag="print_notification",
        )

        countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=12
        )

        icon = PIL.Image.open(f"{ROOT_DIR}/../assets/loading-icon.png")
        photo = PIL.ImageTk.PhotoImage(icon)

        print_btn_icon_src = PIL.Image.open(f"{ROOT_DIR}/../assets/printer-icon.png").convert("RGBA")
        print_btn_icon_src = print_btn_icon_src.resize((30, 30), PIL.Image.ANTIALIAS)
        print_btn_bgc_tmp = PIL.Image.composite(
            print_btn_icon_src,
            PIL.Image.new('RGB', print_btn_icon_src.size, print_notification_container["bg"]),
            print_btn_icon_src
        )
        print_btn_icon = PIL.ImageTk.PhotoImage(print_btn_bgc_tmp)

        label = tk.Label(
            print_notification_container, 
            image=print_btn_icon, 
            bg=print_notification_container["bg"]
        )
        label.image = print_btn_icon # keep a reference!
        label.pack(side="left", padx=(15, 15))
        
        printing_label = tk.Label(
            print_notification_container, 
            text=self.texts["printing"],
            font = countdown_label_style,
            bg=print_notification_container["bg"],
            justify="left"
         )
        printing_label.pack(side="left")

        self.animate_print_notification_in("print_notification")

    def animate_print_notification_in(self, tag_name):
        x_pos, y_pos = self.coords(tag_name)

        if(y_pos < 60):
            self.move(tag_name, 0, 1)
            self.master.after(1, lambda: self.animate_print_notification_in(tag_name))
        else:
            self.is_notification_animating = True
            self.master.after(1500, lambda: self.animate_print_notification_out(tag_name))

    def animate_print_notification_out(self, tag_name):
        x_pos, y_pos = self.coords(tag_name)

        if(y_pos > 0):
            self.move(tag_name, 0, -1)
            self.master.after(1, lambda: self.animate_print_notification_out(tag_name) )
        else:
            self.place_forget()
            # self.place(relx=0.5, rely=0, anchor="n", y=-60)
