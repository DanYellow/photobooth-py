import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, qrcode

from classes.Gallery import Gallery


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
                'access_gallery': "Accéder à la galerie",
                'link_to_gallery': "ou \nraspberrypi.local",
            }
        }

        self.configure_gui()
        self.create_widgets()
        self.setup_files_and_folders()

    def configure_gui(self):
        # screen_width = int(root.winfo_screenwidth())
        # screen_height = int(root.winfo_screenheight())
        # root.geometry(f"{screen_width}x{screen_height}")

        self.parent.title('Photobooth')
        self.parent.geometry(f"600x800")
        self.parent.resizable(False, False)

    def create_widgets(self):
        self.create_home_screen()

    def setup_files_and_folders(self):
        os.chdir(self.ROOT_DIR)
        full_dir = f"{self.ROOT_DIR}/_tmp/full"
        collages_dir = f"{self.ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def create_home_screen(self):
        main_container = tk.Frame(self, bg = "white")
        main_container.pack(fill="both", expand=True)

        navigation_style = ttk.Style()
        navigation_style.configure('HomeScreenBtnsContainer.TFrame', background="#262727")
        navigation = ttk.Frame(
            main_container,
            width="360",
            height="520",
            style='HomeScreenBtnsContainer.TFrame'
        )
        

        qrc_frame = tk.Frame(navigation)
        qrc_frame.pack(pady=10)

        qrc_title_label = tk.Label(
            qrc_frame, 
            text=self.translation['fr']['access_gallery'],
            fg="black",
            bg=self['bg'],
            font = ('Sans','15', 'bold')
        )
        qrc_title_label.pack()


        navigation.pack(pady=30)
        navigation.pack_propagate(0)
        
        btns_container = tk.Frame(
            navigation,
        )
        btns_container.pack(side="top", fill="x", expand=True)

        btns_container_font_style = tkFont.Font(family='DejaVu Sans Mono', size=15)
        start_btn = tk.Button(
            btns_container,
            height = 2,
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
        start_btn.pack(fill="x", expand=True, padx=10, pady=5)

        help_btn = tk.Button(
            btns_container,
            height = 2,
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
        help_btn.pack(fill="x", expand=True, padx=10, pady=5)

        gallery_bg = Gallery(main_container, self.parent)
        gallery_bg.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        gallery_bg.lower()
        # qrc_frame = ttk.Frame(self.home_screen, bg=self['bg'])

        

if __name__ == "__main__":
    root = tk.Tk()
    PhotoboothApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()