import glob
import os
import sys

from tkinter import messagebox, Tk, Tcl, Canvas, PanedWindow, Label, Button
from PIL import Image, ImageTk, ImageFile
from classes.Ui import PhotoboothUi
from classes.Camera import Camera
from classes.Countdown import Countdown
from functools import partial

root = Tk()
root['bg'] = 'white'
# root.option_add('*Dialog.msg.width', 20)
# root.attributes("-fullscreen", 1)

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

photobooth_ui = None
web_gallery = None
camera = None
countdown = None
SCREEN_WIDTH = 600

is_shooting_running = False

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
    full_dir = f"{ROOT_DIR}/_tmp/full"
    cards_dir = f"{ROOT_DIR}/_tmp/cards"

    os.popen(f"mkdir -p {full_dir} && mkdir -p {cards_dir}")

    return 0

def set_nlast_photos_in_ram(list_photos):
    list_last_photos = []

    os.chdir(f"{ROOT_DIR}/_tmp/full")

    for image in list_photos:
        tmp_img = Image.open(image)
        list_last_photos.append(tmp_img)
    
    return list_last_photos

def create_thumbnails(list_images_obj):
    TARGET_SIZE = 450, 450
    os.chdir(f"{ROOT_DIR}/_tmp")

    for image in list_images_obj:
        image_copy = Image.copy(image)
        image_copy.thumbnail(TARGET_SIZE, Image.ANTIALIAS)
        image_copy.save(image_copy.filename, "JPEG", quality=65)

def generate_collage(list_images):
    os.chdir(f"{ROOT_DIR}/_tmp/cards")

    collage_img_ratio = 10 / 15
    collage_img_width = 1000

    collage_img = Image.new('RGB', (
        collage_img_width,
        int(collage_img_width * (1 / collage_img_ratio))
        # int(collage_img_height * (1/collage_img_ratio)),
        # collage_img_height * len(list_images)
    ))

#    images_positions = [[0, 0], [0, 300], [0, 600]]
    
    for idx, image_obj in enumerate(list_images):
        try:
            image_copy = Image.copy(image_obj)
            image_copy.thumbnail((1000, 1000), Image.ANTIALIAS)
            _, height = image_copy.size
            # image_obj.resize((image_obj.size.width * 2, image_obj.size.height * 2), Image.ANTIALIAS)
            collage_img.paste(image_copy, (0, height * idx))
        except Exception as e:
            print(e)

    collage_img.save(list_images[0].filename, "JPEG", quality=65)

    collage_img.thumbnail((600, 600))
    img = ImageTk.PhotoImage(collage_img)
    photobooth_ui.collage_label.configure(image=img)

    return collage_img

def photobooth_workflow(event = None):
    global is_shooting_running
    if event is not None and event.keycode != 36:
        return 0
    if is_shooting_running is True:
        return 0
    is_shooting_running = True

    def pb_anonymous(nb_photos_taken):
        photobooth_ui.pack(
            expand = "y",
            fill = "both",
            pady = 10,
            padx = 10
        )

        n_last_images = get_nlast_images(nb_photos_taken)
        images_in_ram = set_nlast_photos_in_ram(n_last_images)
        
        create_thumbnails(images_in_ram)
        generate_collage(images_in_ram)

        photobooth_ui.collage_label.pack()


        photobooth_ui.btns_panel.pack(
            side="bottom",
            expand=True,
            fill='x',
            anchor="s",
        )

    photobooth_ui.pictures_btn.pack_forget()

    interval = 1
    countdown.generate_ui(interval)
    
    camera.capture(
        countdown = countdown,
        nb_takes = 2,
        end_shooting_callback = pb_anonymous,
        interval = interval,
        photobooth_ui = photobooth_ui
    )

def print_photo():
    print('------------------ printing --------------')

def show_error(msg):
    root.withdraw()
    messagebox.showerror("Error", msg)
    sys.exit()

def quit_(event):
    if event is not None and event.keycode == 9:
        sys.exit()
    return 0

def reset_ui():
    global is_shooting_running
    is_shooting_running = False

    photobooth_ui.pack()
    photobooth_ui.pictures_btn.pack()

    photobooth_ui.btns_panel.pack_forget()
    photobooth_ui.collage_label.pack_forget()

    countdown.pack_forget()

if __name__ == "__main__":
    setup_files_and_folders()

    actions = { 
        "take_pictures": photobooth_workflow,
        "cancel": reset_ui,
        "print": print_photo
    }

    camera = Camera(
        root_dir=ROOT_DIR,
        on_error=show_error
    )
    photobooth_ui = PhotoboothUi(master=root, actions=actions)
    photobooth_ui.pictures_btn.pack(side="bottom")

    countdown = Countdown(master=root)

    root.bind("<KeyPress>", photobooth_workflow)
    root.bind("<KeyPress>", quit_)
    
    photobooth_ui.pack(
            expand=True,
            fill="both",
            pady=10,
            padx=10
        )

    # os.system('env FLASK_APP=router.py flask run --host=0.0.0.0 &')

    screen_width = int(root.winfo_screenwidth() / 2)
    screen_height = int(root.winfo_screenheight() / 2)

    root.geometry(f"600x1024")
    # root.geometry(f"{screen_width}x{screen_height}")

    root.mainloop()

    sys.exit(0)
