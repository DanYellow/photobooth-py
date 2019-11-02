import os
from functools import partial

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Camera:
    def capture(self, 
        countdown = None,
        nb_takes = None,
        end_shooting_callback = None,
        interval = None):
        os.chdir(self.root_dir)

        FULL_PATH = f"{self.root_dir}/_tmp/full"

        if nb_takes is not None:
            self.nb_takes = nb_takes

        if countdown is not None:
            self.countdown = countdown

        if interval is not None:
            self.interval = interval

        if end_shooting_callback is not None:
            self.end_shooting_callback = end_shooting_callback
        
        if(self.shutter_counter == self.nb_takes):
            self.shutter_counter = 0
            return self.end_shooting_callback(self.nb_takes)

        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)

        os.chdir(FULL_PATH)

        print('--- capturing ---', self.nb_takes)

        if self.countdown is not None:
            self.countdown.countdown(self.interval, callback=partial(self.direct_capture))
        else:
            self.direct_capture()

        return 0

    def direct_capture(self):
        self.shutter_counter = self.shutter_counter + 1

        capture_image_cmd = f"""gphoto2 \
            --capture-image-and-download \
            --force-overwrite \
            --keep-raw
            """
        os.system(capture_image_cmd)

        self.capture()

    def __init__(self, root_dir = ROOT_DIR):
        self.root_dir = root_dir
        self.nb_takes = 9999999999
        self.shutter_counter = 0
        self.interval = 3

        camera_setup_cmd = """gphoto2 \
            --set-config capturetarget=1 \
            --set-config shutterspeed=1/100
        """
        os.system(camera_setup_cmd)