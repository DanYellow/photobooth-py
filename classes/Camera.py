import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NB_MAX_PHOTOS = 2

print('ROOT_DIR', ROOT_DIR)

class Camera:
    def capture(self, nb_photos_to_take = NB_MAX_PHOTOS):
        os.chdir(self.root_dir)
        
        INTERVAL = "3s"
        FULL_PATH = f"{self.root_dir}/_tmp/full"

        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)

        os.chdir(FULL_PATH)

        print('capturing')

        capture_image_cmd = f"""gphoto2 \
            --capture-image-and-download \
            --force-overwrite \
            --keep-raw \
            -F={nb_photos_to_take} \
            -I={INTERVAL}"""
        os.system(capture_image_cmd)

        return nb_photos_to_take

    def __init__(self, root_dir = ROOT_DIR):
        self.root_dir = root_dir

        camera_setup_cmd = """gphoto2 \
            --set-config capturetarget=1
        """
        os.system(camera_setup_cmd)