import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, sys, PIL

from screens.Home import Home
from screens.Result import Result
from screens.Countdown import Countdown
from screens.Loading import Loading

from classes.Camera import Camera

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class PhotoboothApplication(ttk.Frame):
    def __init__(self, root, nb_shoots_max = 2, start_count = 2, *args, **kwargs):
        self.root = root
        self.nb_shoots_max = nb_shoots_max
        self.nb_shoots_taken = 0
        self.collage_pics_name_buffer = []

        ttk.Frame.__init__(self, self.root, *args, **kwargs)
        main_style = ttk.Style()
        main_style.configure('App.TFrame', background="white")
        self['style'] = 'App.TFrame'

        self.ROOT_DIR = f"{ROOT_DIR}/.."

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
                'cheese': "Souriez !",
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
            callback = self.on_countdown_ended,
            start_count = start_count
        )


        self.home_screen = Home(self, self.root, self.translation['fr'])
        self.home_screen.start_btn.configure(command=self.start_photoshoot)
        self.home_screen.pack(fill="both", expand=True)

        self.result_screen = Result(self, self.root, self.translation['fr'])
        self.result_screen.print_btn.configure(command=self.print_pic)
        self.result_screen.continue_btn.configure(command=self.go_to_home_screen)

        self.loading_screen = Loading(self, self.translation['fr'])

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

    def go_to_home_screen(self):
        self.result_screen.pack_forget()
        self.home_screen.pack(fill="both", expand=True)

    def on_countdown_ended(self):
        self.camera.capture(f"{ROOT_DIR}/../_tmp/full", callback=self.on_taken_pic)

        # self.loading_screen.pack(side="top", fill="both", expand=1)

    def on_taken_pic(self, temp):
        self.nb_shoots_taken += 1
        latest_pic = self.get_latest_pic()
        self.collage_pics_name_buffer.append(latest_pic)
        self.create_thumbnail(latest_pic)

        self.countdown_screen.reset()
        self.countdown_screen.pack_forget()
        if self.nb_shoots_taken < self.nb_shoots_max:
            self.countdown_screen.start_countdown()
            self.countdown_screen.pack(side="top", fill="both", expand=1)
        else:
            self.loading_screen.pack(side="top", fill="both", expand=1)
            self.on_photoshoot_ended()
        self.loading_screen.pack_forget()

    def on_photoshoot_ended(self):
        collage_path = self.create_collage()

        self.loading_screen.pack_forget()

        self.result_screen.set_collage_image(collage_path)
        self.result_screen.set_fullscreen_collage_image(collage_path)
        self.result_screen.pack(fill="both", expand=True)
        self.collage_pics_name_buffer = []
        self.nb_shoots_taken = 0
        self.home_screen.gallery_bg.update()

    def on_missing_camera(self, msg):
        print('missing_camera')

    def get_latest_pic(self, folder = None):
        os.chdir(f"{self.ROOT_DIR}/_tmp/full")
        images_taken = glob.glob('*.JPG')
        images_taken.extend(glob.glob('*.jpeg'))
        images_taken.extend(glob.glob('*.jpg'))
        latest_pic = max(images_taken, key=os.path.getctime)

        return latest_pic

    def create_thumbnail(self, img_name):
        img_path = f"{self.ROOT_DIR}/_tmp/full/{img_name}"
        TARGET_SIZE = 450, 450
        os.chdir(f"{self.ROOT_DIR}/_tmp")

        tmp_img = PIL.Image.open(img_path)
        tmp_img.thumbnail(TARGET_SIZE, PIL.Image.ANTIALIAS)
        tmp_img.save(img_name, "JPEG", quality=65)

    def create_collage(self):
        os.chdir(f"{self.ROOT_DIR}/_tmp/collages")
        list_collage_pics_paths = map(
            lambda img_name: f"{self.ROOT_DIR}/_tmp/full/{img_name}",
            self.collage_pics_name_buffer
        )

        collage_img_ratio = 15 / 10
        collage_img_width = 1500

        color_white = (255,255,255,0)

        collage_img_size = (collage_img_width, int(collage_img_width * collage_img_ratio))
        collage_img = PIL.Image.new('RGB', collage_img_size, color=color_white)

        for idx, img_path in enumerate(list(list_collage_pics_paths)):
            try:
                tmp_img = PIL.Image.open(img_path)
                tmp_img.thumbnail(collage_img_size, PIL.Image.ANTIALIAS)
                _, height = tmp_img.size

                collage_img.paste(tmp_img, (0, height * idx))
            except Exception as e:
                print(e)

        filename, file_extension = os.path.splitext(self.collage_pics_name_buffer[0])
        collage_name = f"{filename}-f{file_extension}"
        collage_path = f"{self.ROOT_DIR}/_tmp/collages/{collage_name}"
        collage_img.save(collage_path, "JPEG", quality=65)

        return collage_path

    def print_pic():
        print('------------------ printing --------------')

        os.system("cupsenable Canon_SELPHY_CP1300")

        print_cmd = f"""lp -d Canon_SELPHY_CP1300 -o fit-to-page {ROOT_DIR}/_tmp/collages/{collage_name}"""
        os.system(print_cmd)

if __name__ == "__main__":
    root = tk.Tk()
    photobooth_app = PhotoboothApplication(root, nb_shoots_max = 2, start_count = 1)
    photobooth_app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()