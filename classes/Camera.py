import os
import time
from functools import partial
import threading


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NB_MAX_PHOTOS = 2

countdown_ended_thread = threading.Event()


class Camera:
    def capture(self, countdown, nb_photos_to_take = NB_MAX_PHOTOS):
        os.chdir(self.root_dir)
        
        INTERVAL = "3s"
        FULL_PATH = f"{self.root_dir}/_tmp/full"

        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)

        os.chdir(FULL_PATH)

        print('--- capturing ---')

        for _ in range(nb_photos_to_take):
            if countdown is not None:
                print('rgggege')
                countdown.countdown(3, callback=partial(self.direct_capture, nb_photos_to_take))
            else:
                self.direct_capture(nb_photos_to_take = nb_photos_to_take)

    def direct_capture(self, nb_photos_to_take):
        print('picture')

        # for _ in range(nb_photos_to_take):
        #     if countdown is not None:
        #         print('==========================')
        #         countdown.label.pack()
        #         countdown.countdown(3, callback=self.foo)
        #     print('picture')
        #     # capture_image_cmd = f"""gphoto2 \
        #     #     --capture-image-and-download \
        #     #     --force-overwrite \
        #     #     --keep-raw
        #     #     """
        #     # os.system(capture_image_cmd)
        #     time.sleep(3)

        # capture_image_cmd = f"""gphoto2 \
        #     --capture-image-and-download \
        #     --force-overwrite \
        #     --keep-raw \
        #     -F={nb_photos_to_take} \
        #     -I={INTERVAL}"""
        # os.system(capture_image_cmd)

        return nb_photos_to_take

    def __init__(self, root_dir = ROOT_DIR):
        self.root_dir = root_dir

        camera_setup_cmd = """gphoto2 \
            --set-config capturetarget=1 \
            --set-config shutterspeed=1/100
        """
        os.system(camera_setup_cmd)