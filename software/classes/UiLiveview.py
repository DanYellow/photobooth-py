import os
import tkinter as tk
import cv2 as cv2

import requests, threading

from PIL import Image, ImageTk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiLiveview(tk.Frame):
    def start(self):
        cap = cv2.VideoCapture(0)
        print(cap.get(cv2.CAP_PROP_FPS))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 202)
        cap.set(cv2.CAP_PROP_FPS, 1.00)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)

        while(cap.isOpened()):
            result, frame = cap.read()
            if result:
                pilimage = Image.fromarray(frame).resize((360, 202))
      
                collage = ImageTk.PhotoImage(pilimage)

                self.img_container.configure(image=collage)
                self.img_container.image = collage

        cap.release()

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.img_container = tk.Label(self, width=360, height=202, bg="black")
        self.img_container.pack()

        thread = threading.Thread(target=self.start)
        thread.start()
        
        

