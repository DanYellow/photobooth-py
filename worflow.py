import glob
import os
import threading
from tkinter import *
from PIL import Image, ImageTk
import subprocess

import http.server
import socketserver

import time


def start_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def start_stream():
    stream_cmd = 'gphoto2 gphoto2 --capture-movie --force-overwrite --filename _tmp/movie.mjpg'
    os.system(stream_cmd)


def capture_image():
    NB_MAX_PHOTOS = 1
    DIST_FOLDER = "./_tmp"
    os.chdir(DIST_FOLDER)

    for x in range(0, NB_MAX_PHOTOS):
        ts = time.time()
        new_image_name = f"""IMG_{ts}"""
        print('capturing')

        capture_image_cmd = "gphoto2 --capture-image-and-download --force-overwrite --frames=3 --interval=5"
        os.system(capture_image_cmd)

        # list_of_files = glob.glob(f"./*")
        # latest_file = max(list_of_files, key=os.path.getctime)

        # oldext = os.path.splitext(latest_file)[1]
        # os.rename(latest_file, new_image_name + oldext)

        # ufraw_cmd = "ufraw-batch *.cr2 --silent --out-type=jpeg --compression=95 --wb=camera"
        # os.system(ufraw_cmd)

        # if not os.path.exists(directory):
        #     os.makedirs(directory)

        # im = Image.open(image_name)
        # print "Generating jpeg for %s" % name
        # im.thumbnail(im.size)
        # im.save(outfile, "JPEG", quality=100)

        # time.sleep(2)


def display_images():
    image = Image.open("foo.jpg")

    root = Tk()

    img = ImageTk.PhotoImage(image)
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()




if __name__ == "__main__":
    #    threading.Thread(target=start_server).start()
    # display_images()
    capture_image()

#    threading.Thread(target=start_stream).start()
#    start_stream()
