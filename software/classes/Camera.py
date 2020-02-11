import os
from functools import partial
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor as Pool

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Camera:
    def capture(self, folder_location = ROOT_DIR, callback = None):
        os.chdir(folder_location)

        capture_image_cmd = f"""gphoto2 \
            --capture-image-and-download \
            --force-overwrite \
            --keep-raw
            """
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, capture_image_cmd, shell=True)
        if callback is not None:
            f.add_done_callback(callback)

    def is_camera_up(self):
        try:
            camera_setup_process = subprocess.Popen(self.camera_setup_cmd, stdout=subprocess.PIPE)
            if camera_setup_process.wait() != 0:
                return False
                raise RuntimeError()
            else:
                return True

        except:
            return False

    def __init__(self, on_error=None):
        self.camera_setup_cmd = [
            'gphoto2',
            '--set-config', 
            'capturetarget=1', 
            '--set-config', 
            'shutterspeed=1/80',
            '--set-config',
            'whitebalance=0',
            '--set-config',
            'iso=Auto',
            '--set-config',
            'imageformat=RAW + Small Normal JPEG'
        ]
        try:
            camera_setup_process = subprocess.Popen(self.camera_setup_cmd, stdout=subprocess.PIPE)
            if camera_setup_process.wait() != 0:
                raise RuntimeError()
        except:
            if on_error is not None:
                on_error(msg="Pas de caméra détectée")
