import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, qrcode, sys
from PIL import ImageTk

from classes.Gallery import Gallery
from screens.Home import Home


class PhotoboothApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        ttk.Frame.__init__(self, self.parent, *args, **kwargs)
        main_style = ttk.Style()
        main_style.configure('App.TFrame', background="white")
        self['style'] = 'App.TFrame'

        self.ROOT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/.."

        self.translation = {
            'fr': {
                'take_pict': "COMMENCER",
                'help': "aide",
                'print': 'Imprimer',
                'cancel': "Annuler",
                'not_print': "Ne pas imprimer",
                'last_collage': "Dernier collage",
                'ready': 'Prêt ?',
                'take_another_one': "Prendre une autre photo",
                'loading': "Chargement",
                'printing': "Impression lancée",
                'access_gallery': "Accès aux photos",
                'link_to_gallery': "raspberrypi.local\nou",
            }
        }

        self.configure_gui()
        # self.create_widgets()
        self.setup_files_and_folders()

        parent.bind("<KeyPress>", self.quit_)

        self.home_screen = Home(self, self.parent, self.translation['fr'])
        self.home_screen.pack(fill="both", expand=True)
        

    def quit_(self, event):
        if event is not None and event.keycode == 9:
            sys.exit()
        return 0

    def configure_gui(self):
        screen_width = int(root.winfo_screenwidth()) if int(root.winfo_screenwidth()) < 1000 else 600
        screen_height = int(root.winfo_screenheight()) if int(root.winfo_screenheight()) < 1000 else 800
        self.parent.geometry(f"{screen_width}x{screen_height}")

        self.parent.title('Photobooth')
        self.parent.resizable(False, False)

    def create_widgets(self):
        self.create_home_screen()

    def setup_files_and_folders(self):
        os.chdir(self.ROOT_DIR)
        full_dir = f"{self.ROOT_DIR}/_tmp/full"
        collages_dir = f"{self.ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def create_home_screen(self):
        main_container = tk.Frame(self, bg = "#f6e2c3")
        main_container.pack(fill="both", expand=True)

        navigation_style_bg = "#262727"
        navigation_style = ttk.Style()
        navigation_style.configure(
            'HomeScreenBtnsContainer.TFrame',
            background=navigation_style_bg,
            highlightthickness=4,
            highlightcolor="red"
        )
        navigation = ttk.Frame(
            main_container,
            width="360",
            height="520",
            style='HomeScreenBtnsContainer.TFrame',
        )
        navigation.pack(pady=30)
        navigation.pack_propagate(0)

        qrc_frame = tk.Frame(navigation, bg=navigation_style_bg)
        qrc_title_label = tk.Label(
            qrc_frame, 
            text=self.translation['fr']['access_gallery'],
            bg=navigation_style_bg,
            font = ('DejaVu Sans Mono','20'),
            fg="white"
        )
        qrc_title_label.pack(side="top", pady=(30, 0))
#        print('f', ttk.Style().lookup('HomeScreenBtnsContainer.TFrame', "background"))
        qrc_txt_label = tk.Label(
            qrc_frame, 
            text=self.translation['fr']['link_to_gallery'],
            fg="white",
            bg="red",
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
            bg=navigation_style_bg,
        )
        qrc_label.image = img
        qrc_label.pack(side="bottom")

        btns_container = tk.Frame(
            navigation,
            bg=navigation_style_bg,
        )
        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=20)
        btns_container_btns_height = 2
        self.start_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            text = self.translation['fr']['take_pict'],
            # command = self.actions['take_pictures'],
            background="#a1d4f0",
            highlightthickness=2, 
            highlightcolor="red", 
            highlightbackground="#8e9ae9", 
            borderwidth=0,
            fg="white",
            font=btns_container_font_style
        )
        self.start_btn.pack(fill="x", expand=True, pady=(0, 8))

        help_btn = tk.Button(
            btns_container,
            height = btns_container_btns_height,
            text = self.translation['fr']['help'].upper(),
            # command = self.actions['take_pictures'],
            background="#e67e22",
            highlightthickness=2, 
            highlightcolor="red", 
            highlightbackground="#f2a560", 
            borderwidth=0,
            fg="white",
            font=btns_container_font_style
        )
        help_btn.pack(fill="x", expand=True, pady=(8, 0))


        qrc_frame.pack(pady=0)
        btns_container.pack(side="bottom", fill="x", expand=False, padx=40, pady=(0, 20))


        gallery_bg = Gallery(main_container, self.parent, bg = "#f6e2c3")
        gallery_bg.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        gallery_bg.lower()

def callback():
    print('hello')

if __name__ == "__main__":
    root = tk.Tk()
    photobooth_app = PhotoboothApplication(root)
    # photobooth_app.home_screen.start_btn.configure(command=callback, text="HELLO")
    photobooth_app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()