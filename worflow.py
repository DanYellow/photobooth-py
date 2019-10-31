import glob
import os
import threading
from tkinter import *
from PIL import Image, ImageTk
import subprocess

import http.server
import socketserver

import time

window = Tk()
# window.attributes("-fullscreen", 1)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_nlast_images(nb_images):
    os.chdir(f"{ROOT_DIR}/_tmp/full")

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)

    return images_taken_sorted if nb_images == -1 else images_taken_sorted[-nb_images:]

def setup_web_gallery():
    os.chdir(ROOT_DIR)

    os.popen('mkdir -p _tmp/ & cp reset.css ./_tmp/reset.css')


def create_web_gallery():
    os.chdir(f"{ROOT_DIR}/_tmp")

    all_images = glob.glob('*.JPG')
    all_images.sort(key=os.path.getmtime)

    f = open('index.html','w')

    images_tpl = []
    for image in all_images:
        images_tpl.append(f"""
            <li>
                <a href="full/{image}">
                    <figure>
                        <img src="./{image}" />
                    </figure>
                </a>
            </li>
        """)

    message = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Photomaton</title>
                <link rel="stylesheet" type="text/css" href="reset.css">
                <style>
                    body {{
                        padding: 0 2%;
                    }}
                    ul {{
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                        grid-gap: 0.25em;
                        margin: 0 auto;
                    }}

                    @media only screen and (max-width: 600px) {{
                        ul {{
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(33%, 1fr));
                            grid-gap: 0.25em;
                            margin: 0 auto;
                        }}
                    }}

                    img {{
                        display: block;
                        max-width: 100%;
                    }}

                    figure {{
                        height: 150px;
                        overflow: hidden;
                    }}
                </style>
            </head>
            <body>
                <ul>{''.join(images_tpl)}</ul>
            </body>
        </html>
    """

    f.write(message)
    f.close()
    
    return 0


def start_server():
    os.chdir(f"{ROOT_DIR}/_tmp")

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
    os.chdir(ROOT_DIR)
    
    NB_MAX_PHOTOS = 2
    INTERVAL = 1
    FULL_PATH = "./_tmp/full"

    if not os.path.exists(FULL_PATH):
        os.makedirs(FULL_PATH)

    os.chdir(FULL_PATH)

    print('capturing')

    capture_image_cmd = f"""gphoto2 \
        --capture-image-and-download \
        --force-overwrite \
        --frames={NB_MAX_PHOTOS} \
        --keep-raw \
        --interval={INTERVAL}"""
    os.system(capture_image_cmd)

    return NB_MAX_PHOTOS

def display_images(images):
    tmp_img = Image.open(images[0])

    window = Tk()

    basewidth = 300
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

def resize_images_in_ram(list_images):
    TARGET_SIZE = 300, 300
    resized_images = []

    os.chdir(f"{ROOT_DIR}/_tmp/full")

    for image in list_images:
        tmp_img = Image.open(image)
        
        resized_images.append(tmp_img)
    

    return resized_images

def create_thumbnails(list_images_obj):
    TARGET_SIZE = 300, 300
    os.chdir(f"{ROOT_DIR}/_tmp")

    for image in list_images_obj:
        image.thumbnail(TARGET_SIZE, Image.ANTIALIAS)
        print(image.filename)
        image.save(image.filename, "JPEG", quality=65)

    create_web_gallery()

    return 0


def display_collage(list_images):
    collage_img_ratio = 10 / 15
    collage_img_height = 1500
    collage_img = Image.new('RGB', (
        int(collage_img_height * collage_img_ratio),
        collage_img_height
    ))
    images_positions = [[0, 0], [0, 0]]                                                                                                                                                                                                   

    for idx, image_obj in enumerate(list_images):
        collage_img.paste(image_obj, images_positions[idx])

    img = ImageTk.PhotoImage(collage_img)

    panel = Label(window, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    btn = Button(window, text = 'Fermer', command = window.destroy)
    btn.pack()

    window.geometry("1200x600")

    return collage_img


def photobooth_workflow():
    nb_photos_taken = capture_images()
    n_last_images = get_nlast_images(nb_photos_taken)
    resized_images = resize_images_in_ram(n_last_images)
    create_thumbnails(resized_images)

    # threading.Thread(target=create_thumbnails,
    #             kwargs={'list_images_obj':resized_images}, name='create_thumbnails').start()


if __name__ == "__main__":
    setup_web_gallery()
    setup_camera()

    create_web_gallery()
    threading.Thread(target=start_server).start()
    
    bouton = Button(window, text="Take picture")
    bouton.config(command=photobooth_workflow)
    bouton.pack()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{screen_width}x{screen_height}")

    window.mainloop()
    

    # display_collage(resized_images) 
    # display_images(n_last_images)

    sys.exit(0)
#    threading.Thread(target=start_stream).start()
#    start_stream()
