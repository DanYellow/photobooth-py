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
        
        params = {
            'notif_bg': "#ddf1d1",
            'notif_border_bg': "#64b747",
            'tag': 'print_notification',
            'icon_type': "printer",
            'texts_key': "printing"
        }

        self.notification_creator(params)

        self.animate_notification_in("print_notification")

    def create_error_notification(self, texts_key = ""):
        self.place(relx=0.5, rely=0, anchor="n", y=-60)
        
        params = {
            'notif_bg': "#f1d1d9",
            'notif_border_bg': "#b74747",
            'tag': 'error_notification',
            'icon_type': "error",
            'texts_key': texts_key
        }

        self.notification_creator(params)

        self.animate_notification_in("error_notification")

    def notification_creator(self, params):
        notification_container = tk.Frame(
            self, 
            text = None,
            padx = 5,
            pady = 5,
            bg = params['notif_bg'],
            borderwidth=2,
            relief="flat",
            highlightbackground=params['notif_border_bg'],
            highlightthickness=2,
            width=self['width'],
            height=60
        )
        notification_container.pack_propagate(0)

        self.create_window(0, 0, 
            window=notification_container, 
            anchor="nw", 
            tag=params['tag'],
        )

        countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=12
        )

        btn_icon_src = PIL.Image.open(
            f"{ROOT_DIR}/../assets/{params['icon_type']}-icon.png"
        ).convert("RGBA")
        btn_icon_src = btn_icon_src.resize((30, 30), PIL.Image.ANTIALIAS)
        btn_bgc_tmp = PIL.Image.composite(
            btn_icon_src,
            PIL.Image.new(
                'RGB', 
                btn_icon_src.size,
                notification_container["bg"]
            ),
            btn_icon_src
        )
        btn_icon = PIL.ImageTk.PhotoImage(btn_bgc_tmp)

        label = tk.Label(
            notification_container, 
            image=btn_icon, 
            bg=notification_container["bg"]
        )
        label.image = btn_icon # keep a reference!
        label.pack(side="left", padx=(15, 15))
        
        label = tk.Label(
            notification_container, 
            text=self.texts[params["texts_key"]],
            font = countdown_label_style,
            bg=notification_container["bg"],
            justify="left"
         )
        label.pack(side="left")

    def animate_notification_in(self, tag_name):
        x_pos, y_pos = self.coords(tag_name)

        if(y_pos < 60):
            self.move(tag_name, 0, 1)
            self.master.after(1, lambda: self.animate_notification_in(tag_name))
        else:
            self.is_notification_animating = True
            self.master.after(1500, lambda: self.animate_notification_out(tag_name))

    def animate_notification_out(self, tag_name):
        x_pos, y_pos = self.coords(tag_name)

        if(y_pos > 0):
            self.move(tag_name, 0, -1)
            self.master.after(1, lambda: self.animate_notification_out(tag_name) )
        else:
            self.place_forget()
