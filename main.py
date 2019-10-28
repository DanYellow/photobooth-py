from tkinter import *
import gphoto2 as gp
import os
import sys
import time

window = Tk()

context = gp.Context()
camera = gp.Camera()
camera.init(context)

print(camera)

bouton = Button(window, text="Take picture")

def capture_image():
    bouton.config(state=DISABLED)
#    
    print('capturing')
    print(dir(camera))
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE, 3)
#
#    target = os.path.join('_tmp', file_path.name)
#    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
#    camera_file.save(target)
#    ts = time.time()
#    os.rename(target, '_tmp/IMG_' + str(ts) + '.cr2');
#    
#    print('2')
#    camera.exit(context)
#    bouton.config(state=NORMAL)

if __name__ == "__main__":
    bouton.config(command=capture_image)
    bouton.pack()

    window.mainloop()
