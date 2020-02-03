import os, glob, random

from tkinter import Tcl
from flask import Flask, render_template, request, Blueprint

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.filters['zip'] = zip

gallery_thumb_bp = Blueprint(
    'thumb', 
    __name__, 
    static_url_path='/_tmp', 
    static_folder='_tmp'
)
app.register_blueprint(gallery_thumb_bp)

gallery_full_bp = Blueprint(
    'full', 
    __name__, 
    static_url_path='/_tmp/full', 
    static_folder='_tmp/full'
)
app.register_blueprint(gallery_full_bp)

gallery_collages_bp = Blueprint(
    'collages', 
    __name__, 
    static_url_path='/_tmp/collages', 
    static_folder='_tmp/collages'
)
app.register_blueprint(gallery_collages_bp)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

full_dir = f"{ROOT_DIR}/_tmp/full"
collages_dir = f"{ROOT_DIR}/_tmp/collages"

os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

def generate_grid_classes(nb_items):
    def get_class(value):
        if(value <= 0.5):
            return ""
        elif(value > 0.5 and value <= 0.87):
            return "item--medium"
        else:
            return "item--large"

    list_values = []
    for _ in range(nb_items):
        weight = random.uniform(0, 1)
        list_values.append(get_class(weight))

    return list_values

@app.route('/')
def index():
    path = f"{ROOT_DIR}/_tmp"
    os.chdir(path)

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)
    images_taken_sorted = list(reversed(images_taken_sorted))

    return render_template(
        'index.html',
        images_list=images_taken_sorted,
        classes=generate_grid_classes(len(images_taken_sorted))
    )

@app.route('/collages')
def collages():
    path = f"{ROOT_DIR}/_tmp/collages"
    os.chdir(path)

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)
    images_taken_sorted = list(reversed(images_taken_sorted))

    return render_template(
        'collages.html',
        images_list=images_taken_sorted,
        classes=generate_grid_classes(len(images_taken_sorted))
    )

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
