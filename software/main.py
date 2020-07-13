import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import glob, os, sys, PIL, math
import cv2
from subprocess import call


from screens.Home import Home
from screens.Result import Result
from screens.Countdown import Countdown
from screens.Loading import Loading
from screens.Liveview import Liveview

from classes.Camera import Camera
from classes.UiNotification import UiNotification

from classes.UiLiveview import UiLiveview

import utils.colors
import utils.settings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
bytes = ''

class PhotoboothApplication(ttk.Frame):
    def __init__(self, root, nb_shoots_max = 2, start_count = 3, *args, **kwargs):
        self.root = root
        self.nb_shoots_max = nb_shoots_max
        self.nb_shoots_taken = 0
        self.collage_pics_name_buffer = []
        self.liveview_enabled = False

        ttk.Frame.__init__(self, self.root, *args, **kwargs)
        main_style = ttk.Style()
        main_style.configure('App.TFrame', background=utils.colors.mainBackgroundColor)
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
                'printing': "Impression\nlancée",
                'access_gallery': "Accès aux photos\ndès maintenant",
                'link_to_gallery': "raspberrypi.local\nou",
                'cheese': "Cheese !",
                'missing_camera': "Appareil\nnon detecté",
                'close': "Fermer"
             }
        }

        self.configure_gui()
        self.setup_files_and_folders()

        self.countdown_screen = Countdown(
            master = self,
            root = self.root,
            texts = self.translation['fr'],
            callback = self.on_countdown_ended,
            start_count = start_count,
        )
        # self.countdown_screen.pack(fill="both", expand=True)
        # self.countdown_screen.start_countdown(self.nb_shoots_taken + 1, self.nb_shoots_max)

        self.home_screen = Home(self, self.root, self.translation['fr'])
        self.home_screen.start_btn.configure(command=self.start_liveview)
        self.home_screen.pack(fill="both", expand=True)
        
        self.result_screen = Result(self, self.root, self.translation['fr'])
        self.result_screen.print_btn.configure(command=self.print_pic)
        self.result_screen.continue_btn.configure(command=self.go_to_home_screen)

        self.loading_screen = Loading(self, self.translation['fr'])

        self.notification_manager = UiNotification(master = self.root, texts = self.translation['fr'])

        self.camera = Camera(
            on_error=self.on_missing_camera
        )

        self.liveview_screen = Liveview(
            self,
            self.root,
            self.translation['fr'],
            camera=self.camera,
            on_stream_ended=self.on_stream_ended,
            display_time = 25
        )
        self.liveview_screen.start_btn.configure(command=self.interrupt_stream)
        
        root.bind("<KeyPress>", self.quit_)
        root.protocol("WM_DELETE_WINDOW", self.cleanup)

        self.collage_frames = tk.Frame(self, bg=utils.colors.mainBackgroundColor) # utils.colors.mainBackgroundColor

    def update_thumbnails_preview_list(self, img_name):
        TARGET_SIZE = 320, 320
        
        tmp_img = PIL.Image.open(f"{self.ROOT_DIR}/_tmp/full/{img_name}")
        tmp_img.thumbnail(TARGET_SIZE, PIL.Image.ANTIALIAS)

        collage = PIL.ImageTk.PhotoImage(tmp_img)

        img = tk.Label(self.collage_frames, image=collage)
        img.image = collage
        img.pack(side = "left", padx=(4, 4))
            
    def cleanup(self):
        call(["cancel", "-a", f"{utils.settings.printer['name']}"])
        self.camera.stop_liveview()
        sys.exit()
        self.root.destroy()

    def quit_(self, event):
        if event is not None and event.keycode == 9:
            self.cleanup()
        return 0

    def configure_gui(self):
        screen_width = int(root.winfo_screenwidth()) if int(root.winfo_screenwidth()) < 1000 else 1333
        screen_height = int(root.winfo_screenheight()) if int(root.winfo_screenheight()) < 1000 else 1000
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.root.title('Photobooth')
        self.root.resizable(False, False)

    def setup_files_and_folders(self):
        os.chdir(self.ROOT_DIR)
        full_dir = f"{self.ROOT_DIR}/_tmp/full"
        collages_dir = f"{self.ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def start_liveview(self):
        if self.camera.is_up():
            self.home_screen.pack_forget()
            self.liveview_screen.pack(fill="both", expand=True)
            self.liveview_screen.ui_liveview.start_stream()
        else:
            self.notification_manager.create_error_notification('missing_camera')

    def start_photoshoot(self):
        self.liveview_screen.ui_liveview.reset()
        self.camera.stop_liveview()

        self.reset_preview_list()
        self.collage_frames.place(relx=0.5, rely=1, anchor="s", y=-15)

        if self.camera.is_up():
            self.home_screen.pack_forget()
            self.liveview_screen.pack_forget()
            self.countdown_screen.pack(fill="both", expand=True)
            self.countdown_screen.start_countdown(self.nb_shoots_taken + 1, self.nb_shoots_max, skip=True)
        else:
            self.notification_manager.create_error_notification('missing_camera')

    def go_to_home_screen(self):
        self.result_screen.pack_forget()
        self.home_screen.pack(fill="both", expand=True)

    def on_countdown_ended(self):
        self.camera.capture(f"{ROOT_DIR}/../_tmp/full", callback=self.on_taken_pic)

    # Called after each photo
    def on_taken_pic(self, temp):
        self.nb_shoots_taken += 1
        latest_pic = self.get_latest_pic()
        self.collage_pics_name_buffer.append(latest_pic)
        self.create_thumbnail(latest_pic)

        self.update_thumbnails_preview_list(latest_pic)

        self.countdown_screen.reset()
        self.countdown_screen.lower(self.home_screen)
        if self.nb_shoots_taken < self.nb_shoots_max:
            self.countdown_screen.pack(fill="both", expand=True)
            self.countdown_screen.start_countdown(self.nb_shoots_taken + 1, self.nb_shoots_max)
        else:
            self.countdown_screen.pack_forget()
            self.loading_screen.pack(side="top", fill="both", expand=1)
            self.on_photoshoot_ended()
        self.loading_screen.pack_forget()

    def on_photoshoot_ended(self):
        self.collage_path = self.create_collage()

        self.loading_screen.pack_forget()
        self.collage_frames.pack_forget()
        self.collage_frames.place_forget()

        self.result_screen.set_collage_image(self.collage_path)
        self.result_screen.set_fullscreen_collage_image(self.collage_path)
        self.result_screen.pack(fill="both", expand=True)
        self.collage_pics_name_buffer = []
        self.nb_shoots_taken = 0
        self.home_screen.gallery_bg.update()

    def on_missing_camera(self, msg):
        self.notification_manager.create_error_notification('missing_camera')
        print('log : missing_camera')

    def on_stream_ended(self):
        self.start_photoshoot()

    def interrupt_stream(self):
        self.liveview_screen.ui_liveview.time_elapsed = 0

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
        list_collage_pics_paths = list(map(
            lambda img_name: f"{self.ROOT_DIR}/_tmp/full/{img_name}",
            self.collage_pics_name_buffer
        ))

        collage_img_ratio = 15 / 10
        collage_img_width = 1500
        collage_img_bg = (255, 255, 255, 0)
        collage_img_size = (collage_img_width, int(collage_img_width * collage_img_ratio))
        collage_img = PIL.Image.new('RGB', collage_img_size, color=collage_img_bg)

        space_between_thumbs = 10
        bottom_space = 200

        for idx, img_path in enumerate(list_collage_pics_paths):
            try:
                tmp_img = PIL.Image.open(img_path)
                collage_img_width, collage_img_height = collage_img_size
        
                tmp_img_height = math.ceil((collage_img_height - bottom_space) / len(list_collage_pics_paths))
                tmp_img_height = tmp_img_height - space_between_thumbs
                tmp_img.thumbnail([collage_img_width, tmp_img_height], PIL.Image.ANTIALIAS)

                collage_img.paste(
                    tmp_img, 
                        (                            
                            math.ceil(collage_img_width / 2) - math.ceil(tmp_img.size[0] / 2), 
                            tmp_img.size[1] * idx + (space_between_thumbs * idx)
                        )
                )
            except Exception as e:
                print(e)


        filename, file_extension = os.path.splitext(self.collage_pics_name_buffer[0])
        collage_name = f"{filename}-f{file_extension}"
        collage_path = f"{self.ROOT_DIR}/_tmp/collages/{collage_name}"
        collage_img.save(collage_path, "JPEG", quality=65)

        return collage_path

    def print_pic(self):
        print('------------------ printing --------------')

        printer_name = f"{utils.settings.printer['name']}"
        os.system(f"cupsenable {printer_name}")
        print_cmd = f"lp -d {printer_name} -o fit-to-page {self.collage_path}"
        os.system(print_cmd)

        self.go_to_home_screen()
        self.notification_manager.create_print_notification()

    def reset_preview_list(self):
        for child in self.collage_frames.winfo_children():
            child.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root['bg'] = utils.colors.mainBackgroundColor

    nb_shoots_max_settings_arg = utils.settings.photobooth['nb_shoots_max'] if utils.settings.photobooth.get('nb_shoots_max') else None
    nb_shoots_max = nb_shoots_max_settings_arg if type(nb_shoots_max_settings_arg) is int and nb_shoots_max_settings_arg > 0 else 1

    start_count_settings_arg = utils.settings.photobooth['start_count'] if utils.settings.photobooth.get('start_count') else None
    start_count = start_count_settings_arg if type(start_count_settings_arg) is int and start_count_settings_arg > 0 else 1

    photobooth_app = PhotoboothApplication(
        root, 
        nb_shoots_max = nb_shoots_max,
        start_count = start_count
    )
    photobooth_app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()
