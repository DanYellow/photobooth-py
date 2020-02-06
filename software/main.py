import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, *args, **kwargs)
        self['bg'] = 'black'

        self.configure_gui()

    def configure_gui(self):
        self.parent.title('Hello')
        self.parent.geometry(f"600x800")
        self.parent.resizable(False, False)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()