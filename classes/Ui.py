from tkinter import Label, Button, PanedWindow, Frame

class PhotoboothUi(Frame):
    def create_widgets(self):
        self.collage_label = Label(self, image=None)

        self.pictures_btn = Button(
            self,
            height=50,
            width=50,
            text=self.translation['fr']['take_pict']
        )
        self.pictures_btn.config(command=self.actions['take_pictures'])

        self.btns_panel = Frame(self, bg=self['bg'])
        
        self.print_btn = Button(
            self.btns_panel,
            text = self.translation['fr']['print'],
            height = 3,
            fg = "blue"
        )
        self.print_btn.config(command=self.actions['print'])
        self.print_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.cancel_btn = Button(
            self.btns_panel,
            text=self.translation['fr']['cancel'],
            height=3,
            fg="red",
            font = ('Sans','10','bold')
        )
        self.cancel_btn.config(command=self.actions['cancel'])
        self.cancel_btn.pack(side="left", fill="x", expand=True, padx=(10, 0))

        self.loading_screen = Frame(self, bg="black")
        self.loading_label = Label(
            self.loading_screen, 
            text=self.translation['fr']['loading'],
            fg="white",
            bg="black",
            font = ('Sans','30','bold')
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.loading_screen.lift()

    def __init__(self, actions, master=None):
        Frame.__init__(self, master, bg='white')
        self['bg'] = 'white'

        self.actions = actions
        self.translation = {
            'fr': {
                'take_pict': "Prendre des photos !",
                'print': 'Imprimer',
                'cancel': "Annuler",
                'last_collage': "Dernier collage",
                'ready': 'Prêt ?',
                'take_another_one': "Prendre une autre photo",
                'loading': "Chargement"
            }
        }

        self.pack()
        self.create_widgets()
        