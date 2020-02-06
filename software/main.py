import tkinter.ttk as ttk
import tkinter as tk
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
        home_screen_style = ttk.Style()
        home_screen_style.configure('HomeScreen.TFrame', background="red")
        self.home_screen = ttk.Frame(self)
        self.home_screen['style'] = 'HomeScreen.TFrame'
        self.home_screen.pack(fill="both", expand=True)


        gallery_bg = Gallery(self.home_screen, self.parent)
        gallery_bg.pack(fill="both", expand=True)
        gallery_bg.lower()
        # qrc_frame = ttk.Frame(self.home_screen, bg=self['bg'])

if __name__ == "__main__":
    root = tk.Tk()
    PhotoboothApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()