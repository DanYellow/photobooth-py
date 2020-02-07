import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import qrcode, os
from PIL import ImageTk

from classes.Gallery import Gallery

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Home(tk.Frame):
    def __init__(self, master, root, texts, *args, **kwargs):
        self.root = root
        self.texts = texts

        tk.Frame.__init__(self, master, *args, **kwargs) # , cursor="none"

        self.create_widgets()

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

        gallery_bg = self.create_gallery_bg()
        gallery_bg.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        gallery_bg.lower()

    def create_navigation(self):
        navigation_style_bg = "#333333"
        navigation_style = ttk.Style()
        navigation_style.configure(
            'HomeScreenBtnsContainer.TFrame',
            background=navigation_style_bg,
            borderwidth=4,
            highlightbackground="black",
            highlightthickness=1
        )
        navigation = ttk.Frame(
            self,
            width="360",
            height="520",
            style='HomeScreenBtnsContainer.TFrame',
        )

        return navigation

    def create_gallery_bg(self):
        gallery_bg = Gallery(self, self.root, bg = "#f6e2c3")
        return gallery_bg

    def create_btns_container(self, wrapper):
        btns_container = tk.Frame(
            wrapper,
            bg = ttk.Style().lookup(wrapper['style'], "background"),
        )
        btns_container_btns_height = 70
        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=20)
        

        self.image = tk.PhotoImage(file=f"{ROOT_DIR}/../assets/photo-icon.png")
        self.start_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background="#a1d4f0",
            highlightbackground="#8e9ae9", 
            highlightthickness=2,
            activeforeground="#033754", 
            activebackground="#bceefe", 
            borderwidth=0,
            fg="white",
            image=self.image,
            text = self.texts['take_pict'].upper(),
            font=btns_container_font_style,
            compound="left"
        )
        self.start_btn.pack(fill="x", expand=True, pady=(0, 8))

        self.help_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            background="#e67e22",
            highlightthickness=2, 
            highlightcolor="red", 
            highlightbackground="#f2a560", 
            borderwidth=0,
            fg="white",
            text = self.texts['help'].upper(),
            font=btns_container_font_style,
            image=self.image,
            compound="left"
        )
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
        img = ImageTk.PhotoImage(img_tmp)

        qrc_label = tk.Label(
            qrc_frame,
            image=img, 
            bg=ttk.Style().lookup(wrapper['style'], "background"),
        )
        qrc_label.image = img
        qrc_label.pack(side="bottom")

        return qrc_frame

