#import cv2
#import numpy as np
from urllib.request import urlopen
import http.server

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    
stream = urlopen('http://localhost:8000/movie.mjpg')