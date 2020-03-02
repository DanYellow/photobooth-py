import os
import tkinter as tk
import cv2
import numpy as np

import requests, threading

from PIL import Image, ImageTk
import math

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UiLiveview(tk.Frame):
    def start(self):
        bytes = b""

        is_streaming_running = True
        size_chunks = 1024
        nb_chunks = math.ceil(sys.getsizeof(p.stdout) / size_chunks)

        while is_streaming_running:
            bytes += self.camera_stream.read(1024)

            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')

            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                liveview_frame = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)))
                self.liveview_container.configure(image=liveview_frame)
                self.liveview_container.image = liveview_frame
                self.liveview_container._backbuffer_ = liveview_frame
            
                nb_chunks = nb_chunks - 1

            if nb_chunks == 1:
                is_streaming_running = False
 

    def __init__(self, camera_stream, master=None, width=360):
        tk.Frame.__init__(
            self, 
            master, 
            width=width,
            height=math.ceil(width * (9/16)),
            bg="black"
        )

        self.liveview_container = tk.Label(
            self, 
            width=width, 
            height=math.ceil(width * (9/16)),
        )
        
        self.liveview_container.pack()

        self.camera_stream = camera_stream

        if self.camera_stream is not None:
            thread = threading.Thread(target=self.start)
            thread.start()
