from __future__ import print_function

import threading
import logging
import os
import subprocess
import sys
from PIL import Image

import io

import time
import gphoto2 as gp

def capture_images(camera):
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    NB_MAX_PHOTOS = 1

    for x in range(0, NB_MAX_PHOTOS):
        ts = time.time()
        callback_obj = gp.check_result(gp.use_python_logging())

        print('Capturing image')

        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join('./_tmp/', file_path.name)
        print('Copying image to', target)
        camera_file = camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)

        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

        foo = io.BytesIO(file_data)

        basewidth = 3000
        im = Image.open(foo)
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((basewidth, hsize), Image.ANTIALIAS)

        im.save(f"./_tmp/{ts}.jpg")
        
    camera.exit()

def main():
    while True:
        try:
            context = gp.Context()
            camera = gp.Camera()
            camera.init(context)
        except gp.GPhoto2Error as ex:
            print('Please connect and switch on your camera')
            if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                # no camera, try again in 2 seconds
                time.sleep(2)
                continue
            # some other error we can't handle here
            raise
        # operation completed successfully so exit loop
        break

    capture_images(camera)

    return 0

if __name__ == "__main__":
    sys.exit(main())