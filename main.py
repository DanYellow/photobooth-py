import glob
import os

import sys

from tkinter import messagebox, Tk, Tcl, Canvas, PanedWindow
from PIL import Image, ImageTk, ImageFile
from classes.Ui import PhotoboothUi
from classes.WebGallery import WebGallery
from classes.Camera import Camera
from classes.Countdown import Countdown
from functools import partial

root = Tk()
root['bg'] = 'white'
root.option_add('*Dialog.msg.width', 20)
# root.attributes("-fullscreen", 1)

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

photobooth_ui = None
web_gallery = None
camera = None
countdown = None

p = PanedWindow(root, orient="horizontal")
p.pack(side="top", expand="y", fill="both", pady=2, padx=2)



is_shooting_running = False

class CustomButton(Canvas):
    def __init__(self, parent, width, height, color, command=None):
        Canvas.__init__(self, parent, borderwidth=1, 
            relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        self.create_oval((padding,padding,
            width+padding, height+padding), outline=color, fill=color)
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0) + padding
        height = (y1-y0) + padding
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(color="purple")

    def _on_release(self, event):
        # self.configure(relief="raised")
        if self.command is not None:
            self.command()

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

def set_nlast_photos_in_ram(list_photos):
    list_last_photos = []

    os.chdir(f"{ROOT_DIR}/_tmp/full")

    for image in list_photos:
        tmp_img = Image.open(image)
        list_last_photos.append(tmp_img)
    
    return list_last_photos

def create_thumbnails(list_images_obj):
    TARGET_SIZE = 300, 300
    os.chdir(f"{ROOT_DIR}/_tmp")

    for image in list_images_obj:
        image.thumbnail(TARGET_SIZE, Image.ANTIALIAS)
        image.save(image.filename, "JPEG", quality=65)

    # web_gallery.generate_gallery(get_nlast_images(-1)[:: -1])

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

    photobooth_ui.collage_label.configure(image=img)
    photobooth_ui.collage_label.image = img

    return collage_img

def photobooth_workflow(event = None):
    global is_shooting_running
    if event is not None and event.keycode != 36:
        return 0
    if is_shooting_running is True:
        return 0
    is_shooting_running = True

    def pb_anonymous(nb_photos_taken):
        
        n_last_images = get_nlast_images(nb_photos_taken)
        images_in_ram = set_nlast_photos_in_ram(n_last_images)
        create_thumbnails(images_in_ram)

        photobooth_ui.collage_label.pack()
        collage = display_collage(images_in_ram)
        # collage.save("image.jpg", "JPEG", quality=65)

        photobooth_ui.pictures_btn.pack_forget()
        countdown.pack_forget()
        photobooth_ui.print_btn.pack(side="left")
        photobooth_ui.cancel_btn.pack(side="right")

    photobooth_ui.pictures_btn.pack_forget()

    interval = 3
    countdown.generate_ui(interval)
    countdown.pack()
    camera.capture(
        countdown = countdown,
        nb_takes = 2,
        end_shooting_callback = pb_anonymous,
        interval = interval
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
    photobooth_ui.pictures_btn.pack()

    countdown.pack_forget()
    photobooth_ui.collage_label.pack_forget()
    photobooth_ui.print_btn.pack_forget()
    photobooth_ui.cancel_btn.pack_forget()
    
if __name__ == "__main__":
    setup_files_and_folders()

    actions = { 
        "take_pictures": photobooth_workflow,
        "cancel": reset_ui,
        "print": print_photo
    }

    camera = Camera(root_dir=ROOT_DIR, on_error=show_error)
    photobooth_ui = PhotoboothUi(master=root, actions=actions)
    countdown = Countdown(master=root)

    root.bind("<KeyPress>", photobooth_workflow)
    root.bind("<KeyPress>", quit_)

    btn = CustomButton(root, 40, 50, 'red')

    p.add(btn)

    p.pack()
    
    # web_gallery = WebGallery(root_dir=ROOT_DIR)
    # web_gallery.generate_gallery(get_nlast_images(-1)[:: -1])

    screen_width = int(root.winfo_screenwidth() / 2)
    screen_height = int(root.winfo_screenheight() / 2)

    root.geometry(f"{screen_width}x{screen_height}")

    root.mainloop()

    sys.exit(0)
