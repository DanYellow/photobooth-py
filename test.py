import gphoto2 as gp
import os
import sys
import time

context = gp.Context()
camera = gp.Camera()
camera.init(context)

def capture_image():
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))

    target = os.path.join('_tmp', file_path.name)
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    
    camera_file.save(target)
    
    ts = time.time()
    os.rename(target, '_tmp/IMG_' + str(ts) + '.cr2');
    
    camera.exit(context)

capture_image()