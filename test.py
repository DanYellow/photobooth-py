from __future__ import print_function

import logging
import os
import subprocess
import sys
from PIL import Image

import time
import gphoto2 as gp

def capture_image():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    NB_MAX_PHOTOS = 1
    
    for x in range(0, NB_MAX_PHOTOS):
        ts = time.time()

def main():
    

    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join('./_tmp/', file_path.name)
    print('Copying image to', target)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)

    basewidth = 3000
    im = Image.open(target)
    wpercent = (basewidth / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((basewidth, hsize), Image.ANTIALIAS)

    im.save('./_tmp/test.jpg')

    camera.exit()
    return 0

if __name__ == "__main__":
    sys.exit(main())