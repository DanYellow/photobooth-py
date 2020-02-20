import os
import tkinter as tk
import cv2 as cv2

import requests, threading

from PIL import Image, ImageTk
import math

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiLiveview(tk.Frame):
    def start(self):
        frame_width = 480 #self.img_container['width']
        frame_height = math.ceil(frame_width * (9/16))
        self.cap = cv2.VideoCapture("/dev/video0")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, 10.00)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.7)

        while(self.cap.isOpened()):
            result, frame = self.cap.read()
            if result:
                pilimage = Image.fromarray(frame).resize((frame_width, frame_height))
                # pilimage.thumbnail((frame_width, frame_height))
                collage = ImageTk.PhotoImage(pilimage)

                self.img_container.configure(image=collage)
                self.img_container.image = collage
            else:
                self.img_container.pack_forget()

        self.cap.release()
        cv2.destroyAllWindow()

    def __init__(self, master=None, width=360):
        tk.Frame.__init__(
            self, 
            master, 
            width=width,
            height=math.ceil(width * (9/16)),
            bg="black"
        )

        self.img_container = tk.Label(
            self, 
            width=width, 
            height=math.ceil(width * (9/16)), 
            bg="red"
        )
        
        self.img_container.pack()
        self.pack_propagate(0)

        thread = threading.Thread(target=self.start)
        thread.start()
        
        

