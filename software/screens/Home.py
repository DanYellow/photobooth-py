import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import qrcode, os
import PIL

from classes.UiGallery import UiGallery

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Home(tk.Frame):
    def __init__(self, master, root, texts, *args, **kwargs):
        self.root = root
        self.texts = texts

        tk.Frame.__init__(self, master, *args, **kwargs) # , cursor="none"

        self.create_widgets()

        self.is_notification_animating = False

    def create_widgets(self):
        navigation = self.create_navigation()
        navigation.pack(pady=30)
        navigation.pack_propagate(0)

        btns_container = self.create_btns_container(navigation)
        qr_code_area = self.create_qr_code_area(navigation)

        w = tk.Canvas(
            navigation,
            width=200,
            height=10,
            bg=ttk.Style().lookup(navigation['style'], "background"),
            highlightthickness=0,
            relief='ridge'
        )
        w.create_line(2, 2, 600, 2, fill="white")
        w.pack(fill="x", pady=30, padx=40)

        qr_code_area.pack(pady=0)
        btns_container.pack(side="bottom", fill="x", expand=False, padx=40, pady=(0, 20))

        self.gallery_bg = self.create_gallery_bg()
        self.gallery_bg.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        self.gallery_bg.lower()

        self.print_notification_canvas = self.create_print_notification()
        # self.print_notification_canvas.place(relx=0.5, rely=0, anchor="n", y=-60)

    def create_navigation(self):
        navigation_style_bg = "#333333"
        navigation_style = ttk.Style()
        navigation_style.configure(
            'HomeScreenBtnsContainer.TFrame',
            background=navigation_style_bg,
            highlightthickness=10,
        )
        navigation = ttk.Frame(
            self,
            width="360",
            height="520",
            style='HomeScreenBtnsContainer.TFrame',
            relief="solid",
            borderwidth=3
            # highlightthickness=10,
            # highlightbackground="black",
        )

        return navigation

    def create_gallery_bg(self):
        gallery_bg = UiGallery(self, self.root, bg = "#f6e2c3")
        return gallery_bg

    def create_btns_container(self, wrapper):
        btns_container = tk.Frame(
            wrapper,
            bg = ttk.Style().lookup(wrapper['style'], "background"),
        )
        btns_container_btns_height = 70
        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=20)

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
            btns_container,
            height = btns_container_btns_height,
            background=start_btn_bgc,
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground=start_btn_bgc, 
            borderwidth=0,
            fg="white",
            image=start_btn_icon,
            text = self.texts['take_pict'].upper(),
            font=btns_container_font_style,
            compound="left"
        )
        self.start_btn.image = start_btn_icon
        self.start_btn.pack(fill="x", expand=True, pady=(0, 8))


        help_btn_bgc = '#e67e22'
        help_btn_icon_src = PIL.Image.open(f"{ROOT_DIR}/../assets/help-icon.png").convert("RGBA")
        help_btn_icon_src = help_btn_icon_src.resize((30, 30), PIL.Image.ANTIALIAS)
        help_btn_bgc_tmp = PIL.Image.composite(
            help_btn_icon_src,
            PIL.Image.new('RGB', help_btn_icon_src.size, help_btn_bgc),
            help_btn_icon_src
        )
        help_btn_icon = PIL.ImageTk.PhotoImage(help_btn_bgc_tmp)

        self.help_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background=help_btn_bgc,
            highlightthickness=2, 
            highlightcolor="red", 
            highlightbackground="#f2a560",
            activeforeground="#f2a560", 
            activebackground=help_btn_bgc, 
            borderwidth=0,
            fg="white",
            text = self.texts['help'].upper(),
            font=btns_container_font_style,
            image=help_btn_icon,
            compound="left"
        )
        self.help_btn.image = help_btn_icon
        self.help_btn.pack(fill="x", expand=True, pady=(8, 0))

        return btns_container

    def create_qr_code_area(self, wrapper):
        qrc_frame = tk.Frame(
            wrapper,
            bg= ttk.Style().lookup(wrapper['style'], "background")
        )
        qrc_frame.pack(pady=0)

        qrc_title_label = tk.Label(
            qrc_frame, 
            text=self.texts['access_gallery'],
            bg= ttk.Style().lookup(wrapper['style'], "background"),
            font = ('DejaVu Sans Mono','20'),
            fg="white"
        )
        qrc_title_label.pack(side="top", pady=(30, 0))

        qrc_txt_label = tk.Label(
            qrc_frame, 
            text=self.texts['link_to_gallery'],
            fg="white",
            bg= ttk.Style().lookup(wrapper['style'], "background"),
            font = ('DejaVu Sans Mono','15'),
        )
        qrc_txt_label.pack(pady=(0, 10))

        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 5,
            border = 0,
        )
        qr.add_data('http://raspberrypi.local/')
        qr.make(fit=True)
        img_tmp = qr.make_image(fill_color="black", back_color="white")
        img = PIL.ImageTk.PhotoImage(img_tmp)

        qrc_label = tk.Label(
            qrc_frame,
            image=img, 
            bg=ttk.Style().lookup(wrapper['style'], "background"),
        )
        qrc_label.image = img
        qrc_label.pack(side="bottom")

        return qrc_frame

    def create_print_notification(self):  
        print_notification_canvas = tk.Canvas(self, width=220, height=120)

        self.print_notification_container = tk.Frame(
            self, 
            text = None,
            padx = 5,
            pady = 5,
            bg = "#ddf1d1",
            borderwidth=2,
            relief="flat",
            highlightbackground="#64b747",
            highlightthickness=2,
            width=220,
            height=60
        )
        self.print_notification_container.pack_propagate(0)
        print_notification_canvas.create_window(0, 0, 
            window=self.print_notification_container, 
            anchor="nw", 
            tag="print_notification",
        )

        self.countdown_label_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=12
        )

        image = PIL.Image.open(f"{ROOT_DIR}/../assets/loading-icon.png")
        photo = PIL.ImageTk.PhotoImage(image)

        print_btn_icon_src = PIL.Image.open(f"{ROOT_DIR}/../assets/printer-icon.png").convert("RGBA")
        print_btn_icon_src = print_btn_icon_src.resize((30, 30), PIL.Image.ANTIALIAS)
        print_btn_bgc_tmp = PIL.Image.composite(
            print_btn_icon_src,
            PIL.Image.new('RGB', print_btn_icon_src.size, self.print_notification_container["bg"]),
            print_btn_icon_src
        )
        print_btn_icon = PIL.ImageTk.PhotoImage(print_btn_bgc_tmp)

        label = tk.Label(
            self.print_notification_container, 
            image=print_btn_icon, 
            bg=self.print_notification_container["bg"]
        )
        label.image = print_btn_icon # keep a reference!
        label.pack(side="left", padx=(15, 15))
        
        printing_label = tk.Label(
            self.print_notification_container, 
            text=self.texts["printing"],
            font = self.countdown_label_style,
            bg=self.print_notification_container["bg"],
            justify="left"
         )
        printing_label.pack(side="left")

        return print_notification_canvas


    def animate_print_notification_in(self):
        # if self.is_notification_animating == False:
        x_pos, y_pos = self.print_notification_canvas.coords('print_notification')
        print("animate_print_notification_in", y_pos)

        if(y_pos < 60):
            self.print_notification_canvas.move('print_notification', 0, 1)
            self.root.after(1, self.animate_print_notification_in)
        else:
            self.is_notification_animating = True
            self.root.after(1500, self.animate_print_notification_out)


    def animate_print_notification_out(self):
        x_pos, y_pos = self.print_notification_canvas.coords('print_notification')

        if(y_pos > 0):
            self.print_notification_canvas.move('print_notification', 0, -1)
            self.root.after(1, self.animate_print_notification_out)
        else:
            self.is_notification_animating = False
            self.print_notification_canvas.place(relx=0.5, rely=0, anchor="n", y=-60)
