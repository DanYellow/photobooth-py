import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, sys, PIL

from screens.Home import Home
from screens.Result import Result

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

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
                'continue': 'Continuer',
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
        self.home_screen.start_btn.configure(command=self.start_photoshooting)
        self.home_screen.pack(fill="both", expand=True)

        collage_path = f"{ROOT_DIR}/../_tmp/collages/IMG_9354.JPG"

        self.result_screen = Result(self, self.parent, collage_path, self.translation['fr'])
        self.result_screen.print_btn.configure(command=self.go_to_home_screen)
        self.result_screen.continue_btn.configure(command=self.go_to_home_screen)

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

    # def create_widgets(self):
    #     self.create_home_screen()

    def setup_files_and_folders(self):
        os.chdir(self.ROOT_DIR)
        full_dir = f"{self.ROOT_DIR}/_tmp/full"
        collages_dir = f"{self.ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def start_photoshooting(self):
        self.result_screen.pack(fill="both", expand=True)
        self.home_screen.pack_forget()

    def go_to_home_screen(self):
        self.result_screen.pack_forget()
        self.home_screen.pack(fill="both", expand=True)

def callback():
    print('hello')

if __name__ == "__main__":
    root = tk.Tk()
    photobooth_app = PhotoboothApplication(root)
    # photobooth_app.home_screen.start_btn.configure(command=callback, text="HELLO")
    photobooth_app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()