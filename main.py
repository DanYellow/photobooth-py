import time
import glob, os, sys, random, subprocess, threading, eventlet, socketio
import _thread

from tkinter import messagebox, Tk, Tcl, Button
from PIL import Image, ImageTk, ImageFile
from functools import partial
from concurrent.futures import ThreadPoolExecutor as Pool

from classes.Ui import PhotoboothUi
from classes.Camera import Camera
from classes.Countdown import Countdown

root = Tk()
# root['bg'] = 'white'
root.title('Photomaton')
# root.attributes("-fullscreen", 1)
# root.option_add('*Dialog.msg.width', 20)

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

photobooth_ui = None
web_gallery = None
camera = None
countdown = None
SCREEN_WIDTH = 600
collage_name = None

is_shooting_running = False

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins="*")
    
# wrap with a WSGI application
app = socketio.WSGIApp(sio)

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
        image_copy = image.copy()
        image_copy.thumbnail(TARGET_SIZE, Image.ANTIALIAS)
        image_copy.save(image.filename, "JPEG", quality=65)

def generate_collage(list_images):
    os.chdir(f"{ROOT_DIR}")
    imtest = Image.open("white.png")

    global collage_name
    os.chdir(f"{ROOT_DIR}/_tmp/cards")

    collage_img_ratio = 15 / 10
    collage_img_width = 1500

    color_white = (255,255,255,0)
    color_black = (0,0,0,1)

    collage_img_size = (collage_img_width, int(collage_img_width * collage_img_ratio))

    collage_img = Image.new('RGB', collage_img_size
        # int(collage_img_height * (1/collage_img_ratio)),
        # collage_img_height * len(list_images)
    , color=color_black)

#    images_positions = [[0, 0], [0, 300], [0, 600]]
    
    for idx, image_obj in enumerate(list_images):
        try:
            image_copy = image_obj.copy()
            image_copy.thumbnail(collage_img_size, Image.ANTIALIAS)
            _, height = image_copy.size

            # image_obj.resize((image_obj.size.width * 2, image_obj.size.height * 2), Image.ANTIALIAS)
            collage_img.paste(image_copy, (0, height * idx))
        except Exception as e:
            print(e)

    collage_name = list_images[0].filename
    collage_img.save(list_images[0].filename, "JPEG", quality=65)

    # test for design
    # collage_img.paste(imtest)

    collage_img.thumbnail((600, 600))
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

    def shooting_callback(nb_photos_taken = 2):
        photobooth_ui.pack(
            expand = "y",
            fill = "both"
        )

        n_last_images = get_nlast_images(nb_photos_taken)
        images_in_ram = set_nlast_photos_in_ram(n_last_images)
        
        create_thumbnails(images_in_ram)
        photobooth_ui.gallery_bg.load()
        generate_collage(images_in_ram)

        photobooth_ui.collage_screen.pack(expand=True, fill='both', pady = 10,
            padx = 10)

    photobooth_ui.home_screen.pack_forget()

    interval = 3
    countdown.generate_ui(interval)
    
    camera.capture(
        countdown = countdown,
        nb_takes = 2, 
        end_shooting_callback = shooting_callback,
        interval = interval,
        photobooth_ui = photobooth_ui
    )

def check_printing():
    while True:
        result = subprocess.run(['lpstat', '-o'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        if "Canon_SELPHY" not in result:
            break
    reset_ui()

def print_photo():
    print('------------------ printing --------------')

    photobooth_ui.collage_screen.pack_forget()
    photobooth_ui.print_screen.pack(
            expand=1,
            fill="both",
            side="top"
    )

    os.system("cupsenable Canon_SELPHY_CP1300")

    print_cmd = f"""lp -d Canon_SELPHY_CP1300 -o fit-to-page {ROOT_DIR}/_tmp/cards/{collage_name}"""
    os.system(print_cmd)
    
    ui_thread = threading.Thread(target=check_printing)
    ui_thread.start()


def show_error(msg):
    messagebox.showerror("Error", msg)
    root.withdraw()
    sys.exit()

def quit_(event):
    if event is not None and event.keycode == 9:
        sys.exit()
    return 0

def reset_ui():
    global is_shooting_running
    is_shooting_running = False

    photobooth_ui.pack()
    photobooth_ui.home_screen.pack(expand=True, fill='both')

    photobooth_ui.collage_screen.pack_forget()
    countdown.pack_forget()
    photobooth_ui.print_screen.pack_forget()

if __name__ == "__main__":
    setup_files_and_folders()

    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())

    root.geometry(f"600x800")
    # root.geometry(f"{screen_width}x{screen_height}")

    actions = { 
        "take_pictures": photobooth_workflow,
        "not_print": reset_ui,
        "print": print_photo
    }

    camera = Camera(
        root_dir=ROOT_DIR,
        on_error=show_error
    )
    photobooth_ui = PhotoboothUi(master=root, actions=actions)
    photobooth_ui.home_screen.pack(expand=True, fill='both')

    countdown = Countdown(master=root)

    root.bind("<KeyPress>", photobooth_workflow)
    root.bind("<KeyPress>", quit_)

    root.mainloop()

    sys.exit(0)
