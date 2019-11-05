import glob
import os

from tkinter import Tcl
from flask import Flask, render_template, escape, request, Blueprint

app = Flask(__name__)

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

gallery_cards_bp = Blueprint(
    'cards', 
    __name__, 
    static_url_path='/_tmp/cards', 
    static_folder='_tmp/cards'
)
app.register_blueprint(gallery_cards_bp)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    os.chdir(f"{ROOT_DIR}/_tmp")

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)
    return render_template('index.html',  images_list=images_taken_sorted)

@app.route('/cards')
def cards():
    os.chdir(f"{ROOT_DIR}/_tmp/cards")

    images_taken = glob.glob('*.JPG')
    images_taken.extend(glob.glob('*.jpeg'))
    images_taken.extend(glob.glob('*.jpg'))

    images_taken_sorted = Tcl().call('lsort', '-dict', images_taken)
    return render_template('cards.html',  images_list=images_taken_sorted)