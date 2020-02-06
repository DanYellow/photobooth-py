import tkinter as tk
import glob, os, qrcode

class PhotoboothApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, *args, **kwargs)
        self['bg'] = 'black'

        self.ROOT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}/.."

        self.configure_gui()
        self.setup_files_and_folders()

    def configure_gui(self):
        # screen_width = int(root.winfo_screenwidth())
        # screen_height = int(root.winfo_screenheight())
        # root.geometry(f"{screen_width}x{screen_height}")

        self.parent.title('Photobooth')
        self.parent.geometry(f"600x800")
        self.parent.resizable(False, False)

    def setup_files_and_folders():
        os.chdir(ROOT_DIR)
        full_dir = f"{ROOT_DIR}/_tmp/full"
        collages_dir = f"{ROOT_DIR}/_tmp/collages"

        os.popen(f"mkdir -p {full_dir} && mkdir -p {collages_dir}")

    def create_home_screen():
        self.home_screen = tk.PanedWindow(self, orient = "vertical", bg = self['bg'])

        qrc_frame = tk.Frame(self.home_screen, bg=self['bg'])

if __name__ == "__main__":
    root = tk.Tk()
    PhotoboothApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()