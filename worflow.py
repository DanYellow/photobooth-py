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

def setup_camera():
    camera_setup_cmd = "gphoto2 --set-config capturetarget=1"
    os.system(camera_setup_cmd)

def capture_images():
    NB_MAX_PHOTOS = 1
    INTERVAL = 3

    cwd = "./_tmp"
    os.chdir(cwd)

    print('capturing')

    capture_image_cmd = f"""gphoto2 \
        --capture-image-and-download \
        --force-overwrite \
        --frames={NB_MAX_PHOTOS} \
        --keep-raw \
        --interval={INTERVAL}"""
    os.system(capture_image_cmd)

    return NB_MAX_PHOTOS

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

def get_nlast_images(nb_images):
    # try:
    #     cwd = "./_tmp"
    #     os.chdir(cwd)

    images_taken = glob.glob(f"./*")
    images_taken.sort(key=os.path.getmtime)
     
    return images_taken[-nb_images:]

def display_images(images):
    # window = Tk()
    tmp_img = Image.open(images[0])


    # photo = PhotoImage(file=images[0])
    # panel = Label(window, image = photo)

    # panel.pack(side = "bottom", fill = "both", expand = "yes")

    # canvas = Canvas(window, width=350, height=200)
    # canvas.create_image(0, 0, anchor=NW, image=photo)
    # canvas.pack()

    window = Tk()

    basewidth = 600
    wpercent = (basewidth / float(tmp_img.size[0]))
    hsize = int((float(tmp_img.size[1]) * float(wpercent)))
    tmp_img_resized = tmp_img.resize((basewidth, hsize), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(tmp_img_resized)

    panel = Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    window.geometry("900x600")

    bouton=Button(window, text="Fermer", command=window.quit)
    bouton.pack()

    window.mainloop()

if __name__ == "__main__":
    #    threading.Thread(target=start_server).start()
    # display_images()
    setup_camera()
    nb_photos_taken = capture_images()
    n_last_images = get_nlast_images(nb_photos_taken)
    display_images(n_last_images)


#    threading.Thread(target=start_stream).start()
#    start_stream()
