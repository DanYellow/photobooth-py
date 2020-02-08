import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont

class Countdown(tk.Frame):
    def __init__(self, master, root, texts, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, background="wheat") # , cursor="none"

        self.root = root
        self.count = 3
        self.root.update()

        self.canvas = tk.Canvas(
            self,
            width=self.root.winfo_width(),
            height = self.root.winfo_height()
        )
        w = tk.Label(master, text="Hello, world!")
        self.labels_container_window = self.canvas.create_window(
            30, 
            30, 
            window=w, 
            anchor="nw",
            
        )
        self.canvas.create_rectangle(0, 0, 60, 90, fill="blue", tags = "circle")
        self.canvas.pack()
        self.create_widgets()
        self.countdown()

    def create_widgets(self):
        self.countdown_label = tk.Label(self, 
            background=self["bg"],
            borderwidth=0,
            text=self.count,
            font = ('DejaVu Sans Mono', 70)
        )

        self.countdown_label.pack(side="top", expand=1, fill="both")

    def countdown(self):
        self.canvas.scale("circle", 1, 1, 1.5, 1.5)
        if self.count > 0:
            # call countdown again after 1000ms (1s)
            self.countdown_label.configure(text=self.count)
            self.root.after(1000, self.countdown)
            self.count = self.count-1
        else:
            self.countdown_label.configure(text="Souriez !")