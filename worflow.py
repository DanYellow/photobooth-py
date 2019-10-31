import glob
import os
import threading
from tkinter import *
from PIL import Image, ImageTk, ImageFile
import subprocess

import http.server
import socketserver

import time

window = Tk()
# window.attributes("-fullscreen", 1)

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
collage_label = Label(window, image=None)
collage_label.place(x=70,y=30)
collage_label.pack()


def get_nlast_images(nb_images):
    imgs_list_full_dir = f"{ROOT_DIR}/_tmp/full/"
    os.chdir(imgs_list_full_dir)

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)

    return images_taken_sorted if nb_images == -1 else images_taken_sorted[-nb_images:]

def setup_files_and_folders():
    os.chdir(ROOT_DIR)
    full_dir = f"{ROOT_DIR}/_tmp/full/"

    os.popen(f"mkdir -p _tmp/ && cp reset.css ./_tmp/reset.css && mkdir -p {full_dir}" )

    return 0


def create_web_gallery():
    all_images = get_nlast_images(-1)[:: -1]
    os.chdir(f"{ROOT_DIR}/_tmp")

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

    return 0


def start_stream():
    stream_cmd = 'gphoto2 gphoto2 --capture-movie --force-overwrite --filename _tmp/movie.mjpg'
    os.system(stream_cmd)

    return 0

def setup_camera():
    camera_setup_cmd = """gphoto2 \
        --set-config capturetarget=1 \
    """
    os.system(camera_setup_cmd)

    return 0

def capture_images():
    os.chdir(ROOT_DIR)
    
    NB_MAX_PHOTOS = 2
    INTERVAL = "3s"
    FULL_PATH = f"{ROOT_DIR}/_tmp/full"

    if not os.path.exists(FULL_PATH):
        os.makedirs(FULL_PATH)

    os.chdir(FULL_PATH)

    print('capturing')

    capture_image_cmd = f"""gphoto2 \
        --capture-image-and-download \
        --force-overwrite \
        --keep-raw \
        -F={NB_MAX_PHOTOS} \
        -I={INTERVAL}"""
    os.system(capture_image_cmd)



    return NB_MAX_PHOTOS


def resize_images_in_ram(list_images):
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
        image.save(image.filename, "JPEG", quality=65)

    create_web_gallery()

def display_collage(list_images):
    os.chdir(f"{ROOT_DIR}/_tmp")

    collage_img_ratio = 10 / 15
    _, height_list_images_item = list_images[0].size
    collage_img_height = height_list_images_item

    collage_img = Image.new('RGB', (
        int(collage_img_height * (1/collage_img_ratio)),
        collage_img_height * len(list_images)
    ))

#    images_positions = [[0, 0], [0, 300], [0, 600]]
    
    for idx, image_obj in enumerate(list_images):
        try:
            _, height = image_obj.size
            collage_img.paste(image_obj, (0, height * idx))
        except Exception as e:
            print(e)
    
    img = ImageTk.PhotoImage(collage_img)

    collage_label.configure(image=img)
    collage_label.image = img



    return collage_img


def photobooth_workflow():
    nb_photos_taken = capture_images()
    n_last_images = get_nlast_images(nb_photos_taken)
    images_in_ram = resize_images_in_ram(n_last_images)
    create_thumbnails(images_in_ram)
    img_collage = display_collage(images_in_ram)
    print("---------------------------------------- img_collage", img_collage)
    
    window.mainloop()
    window.update()
    

if __name__ == "__main__":
    setup_files_and_folders()
    setup_camera()

    create_web_gallery()
    threading.Thread(target=start_server).start()
    
    take_pictures_btn = Button(window, text="Take picture")
    take_pictures_btn.config(command=photobooth_workflow)
    take_pictures_btn.pack()

    screen_width = int(window.winfo_screenwidth() / 2)
    screen_height = int(window.winfo_screenheight() / 2)

    window.geometry(f"{screen_width}x{screen_height}")

    window.mainloop()

    sys.exit(0)
