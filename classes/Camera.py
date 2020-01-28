import os
from functools import partial
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor as Pool

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Camera:
    def capture(self, 
        countdown = None,
        nb_takes = None,
        end_shooting_callback = None,
        interval = None,
        photobooth_ui = None
    ):
        os.chdir(self.root_dir)

        FULL_PHOTOS_DIR = f"{self.root_dir}/_tmp/full"

        if nb_takes is not None:
            self.nb_takes = nb_takes

        if countdown is not None:
            self.countdown = countdown

        if photobooth_ui is not None:
            self.photobooth_ui = photobooth_ui

        if interval is not None:
            self.interval = interval

        if end_shooting_callback is not None:
            self.end_shooting_callback = end_shooting_callback
        
        if(self.shutter_counter == self.nb_takes):
            self.shutter_counter = 0
            self.countdown.place_forget()
            self.photobooth_ui.loading_screen.pack()
            return self.end_shooting_callback(self.nb_takes)

        if not os.path.exists(FULL_PHOTOS_DIR):
            os.makedirs(FULL_PHOTOS_DIR)

        self.countdown.place(relx=0.5, rely=0.5, anchor="center")

        os.chdir(FULL_PHOTOS_DIR)

        print('--- capturing ---')

        if self.countdown is not None:
            self.countdown.countdown(self.interval, callback=partial(self.direct_capture))
        else:
            self.direct_capture()

    def direct_capture(self):
        self.shutter_counter = self.shutter_counter + 1

        # print('Chargement')
        self.photobooth_ui.loading_screen.pack(
            expand=1,
            fill="both",
            side="top"
        )
        self.photobooth_ui.lift(self.countdown)

        capture_image_cmd = f"""gphoto2 \
            --capture-image-and-download \
            --force-overwrite \
            --keep-raw
            """
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, capture_image_cmd, shell=True)
        f.add_done_callback(self.post_capture)
        
        self.countdown.place_forget()

    def post_capture(self, arg):
        self.photobooth_ui.lower(self.countdown)
        self.photobooth_ui.loading_screen.pack_forget()
        self.capture()
    
    def __init__(self, root_dir = ROOT_DIR, on_error=None):
        self.root_dir = root_dir
        self.nb_takes = 0
        self.shutter_counter = 0
        self.interval = 0

        try:
            camera_setup_cmd = [
                'gphoto2',
                '--set-config', 
                'capturetarget=1', 
                '--set-config', 
                'shutterspeed=1/80',
                '--set-config',
                'whitebalance=0'
                '--set-config',
                'iso=Auto'
            ]
            camera_setup_process = subprocess.Popen(camera_setup_cmd, stdout=subprocess.PIPE)
            if camera_setup_process.wait() != 0:
                raise RuntimeError()
        except:
            if on_error is not None:
                on_error(msg="Pas de caméra détectée")
