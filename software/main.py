import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, sys, PIL

from screens.Home import Home
from screens.Result import Result
from screens.Countdown import Countdown

from classes.Camera import Camera

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class PhotoboothApplication(ttk.Frame):
    def __init__(self, root, nb_shoots_max = 2, *args, **kwargs):
        self.root = root
        self.nb_shoots_max = nb_shoots_max
        self.nb_shoots_taken = 0

        ttk.Frame.__init__(self, self.root, *args, **kwargs)
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
                'cheese': "Souriez !"
             }
        }

        self.configure_gui()
        # self.create_widgets()
        self.setup_files_and_folders()

        self.camera = Camera(
            on_error=self.on_missing_camera
        )

        self.countdown_screen = Countdown(
            master = self,
            root = self.root,
            texts = self.translation['fr'],
            callback = self.on_countdown_ended
        )

        self.home_screen = Home(self, self.root, self.translation['fr'])
        self.home_screen.start_btn.configure(command=self.start_photoshoot)
        self.home_screen.pack(fill="both", expand=True)

        # collage_path = f"{ROOT_DIR}/../_tmp/collages/IMG_9354.JPG"
        self.result_screen = Result(self, self.root, self.translation['fr'])
        self.result_screen.print_btn.configure(command=self.go_to_home_screen)
        self.result_screen.continue_btn.configure(command=self.go_to_home_screen)

        root.bind("<KeyPress>", self.quit_)

    def quit_(self, event):
        if event is not None and event.keycode == 9:
            sys.exit()
        return 0

    def configure_gui(self):
        screen_width = int(root.winfo_screenwidth()) if int(root.winfo_screenwidth()) < 1000 else 600
        screen_height = int(root.winfo_screenheight()) if int(root.winfo_screenheight()) < 1000 else 800
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.root.title('Photobooth')
        self.root.resizable(False, False)

    # def create_widgets(self):
    #     self.create_home_screen()

    def setup_files_and_folders(self):
        os.chdir(self.ROOT_DIR)
        full_dir = f"{self.ROOT_DIR}/_tmp/full"
        collages_dir = f"{self.ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def start_photoshoot(self):
        self.home_screen.pack_forget()

        self.countdown_screen.start_countdown()
        self.countdown_screen.pack(side="top", fill="both", expand=1)
        # self.result_screen.pack(fill="both", expand=True)

    def go_to_home_screen(self):
        self.result_screen.pack_forget()
        self.home_screen.pack(fill="both", expand=True)

    def on_countdown_ended(self):
        self.camera.capture(f"{ROOT_DIR}/../_tmp/full", callback=self.on_taken_pic)
        self.countdown_screen.reset()
        self.countdown_screen.pack_forget()

    def on_taken_pic(self, temp):
        self.nb_shoots_taken += 1
        if self.nb_shoots_taken < self.nb_shoots_max:
            self.countdown_screen.start_countdown()
            self.countdown_screen.pack(side="top", fill="both", expand=1)
        else:
            self.on_photoshoot_ended()

    def on_photoshoot_ended(self):
        collage_path = f"{ROOT_DIR}/../_tmp/collages/IMG_9354.JPG"
        self.result_screen.set_collage_image(collage_path)
        self.result_screen.set_fullscreen_collage_image(collage_path)
        self.result_screen.pack(fill="both", expand=True)

    def on_missing_camera(self, msg):
        print('missing_camera')

if __name__ == "__main__":
    root = tk.Tk()
    photobooth_app = PhotoboothApplication(root, nb_shoots_max = 1)
    photobooth_app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()