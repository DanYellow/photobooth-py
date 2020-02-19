import cv2 as cv2
import subprocess, os, signal

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Liveview:
    def start(self, folder_location = ROOT_DIR):
        os.chdir(folder_location)

        capture_movie_cmd = f"""gphoto2 \
            --capture-movie
        """

        capture_movie_process = subprocess.Popen(
            capture_movie_cmd,
            stdout=subprocess.PIPE, 
            shell=True,
            preexec_fn=os.setsid
        )

        self.process = capture_movie_process.pid

    def stop(self):
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM) 

    def __init__(self):
        self.process = None