from functools import partial
import subprocess, time, os, re, signal
from concurrent.futures import ThreadPoolExecutor as Pool

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Camera:
    def capture(self, folder_location = ROOT_DIR, callback = None):
        os.chdir(folder_location)

        capture_image_cmd = f"""gphoto2 \
            --capture-image-and-download \
            --force-overwrite \
            --keep-raw \
            --filename %f-photobooth.JPG
            """
        pool = Pool(max_workers=1)
        f = pool.submit(subprocess.call, capture_image_cmd, shell=True)
        if callback is not None:
            f.add_done_callback(callback)

    def liveview(self):
        liveview_cmd = ["gphoto2", "--capture-movie", "--stdout"]
        liveview_process = subprocess.Popen(
            liveview_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

        return liveview_process.stdout

    def stop_liveview(self):
        os.system("ps -ef | grep 'gphoto2 --capture' | grep -v grep | awk '{print $2}' | xargs -r kill -9")
        os.system("gphoto2 --summary -q | grep 'Summary'")

    def is_up(self):
        try:
            camera_setup_process = subprocess.Popen(self.camera_setup_cmd, stdout=subprocess.PIPE)
            if camera_setup_process.wait() != 0:
                return False
            else:
                return True

        except:
            return False

    def get_battery_level(self):
        camera_get_level_cmd = [
            'gphoto2',
            '--get-config=batterylevel',
        ]
        camera_setup_process = subprocess.Popen(camera_get_level_cmd, stdout=subprocess.PIPE)
        out, err = camera_setup_process.communicate()

        if err:
            return None
        else:
            search_battery_level_percent = re.search(r'\d+%', str(out), re.I)
            search_battery_level = re.search(r'\d+', str(search_battery_level_percent.group()), re.I).group()

            return int(search_battery_level)

    def __init__(self, on_error=None):
        self.stream = None

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
            'imageformat=RAW + Small Normal JPEG',
            '--set-config',
            'picturestyle=Portrait',
            '--set-config',
            'drivemode=Single'
        ]
        try:
            camera_setup_process = subprocess.Popen(self.camera_setup_cmd, stdout=subprocess.PIPE)
            if camera_setup_process.wait() != 0:
                raise RuntimeError()
        except:
            if on_error is not None:
                on_error(msg="Pas de caméra détectée")
