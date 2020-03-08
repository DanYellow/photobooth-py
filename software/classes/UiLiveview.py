import os
import tkinter as tk
import cv2
import numpy as np

import requests, threading

from PIL import Image, ImageTk
import math

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiLiveview(tk.Frame):
    def countdown(self):
        if self.time_elapsed > 0:
            self.root.after(1000, self.countdown)
            self.time_elapsed = self.time_elapsed - 1
        else:
            self.is_streaming_running = False

    def compute_stream(self):
        bytes = b""

        self.is_streaming_running = True
        chunks_size = 1024
 
        while self.is_streaming_running:
            bytes += self.camera_stream.read(chunks_size)

            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')

            if a != -1 and b != -1:
                if self.countdown_running == False:
                    self.countdown_running = True
                    self.countdown()

                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                
                img = Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB))
                resized_img = img.resize((
                    self.liveview_container['width'], 
                    self.liveview_container['height']
                ))
                
                liveview_frame = ImageTk.PhotoImage(resized_img)
                self.liveview_container.configure(image=liveview_frame)
                self.liveview_container.image = liveview_frame
                self.liveview_container._backbuffer_ = liveview_frame
        
        if self.on_stream_ended is not None:
            self.time_elapsed = 0
            self.reset()
            self.on_stream_ended()

    def start_stream(self):
        if self.camera is not None:
            self.is_streaming_running = True
            self.camera_stream = self.camera.liveview()
            thread = threading.Thread(target=self.compute_stream)
            thread.start()

    def reset(self):
        self.liveview_container.config(image='')
        self.time_elapsed = self.display_time
        self.countdown_running = False

    def __init__(self, master, root, 
        camera, display_time, on_stream_ended = None, width=360):
        
        tk.Frame.__init__(
            self, 
            master, 
            width=width,
            height=math.ceil(width * (10 / 15)),
            bg="black"
        )

        self.liveview_container = tk.Label(
            self, 
            width=width, 
            height=math.ceil(width * (10 / 15)),
        )
        
        self.liveview_container.pack()

        self.camera = camera
        self.time_elapsed = display_time
        self.display_time = display_time
        self.is_streaming_running = True
        self.countdown_running = False
        self.root = root
        self.on_stream_ended = on_stream_ended
