from tkinter import Label, Button, PanedWindow, Frame

class PhotoboothUi(PanedWindow):
    def create_widgets(self):
        self.collage_label = Label(self, image=None)

        self.pictures_btn = Button(self, text=self.translation['fr']['take_pict'])
        self.pictures_btn.config(command=self.actions['take_pictures'])

        self.btns_panel = PanedWindow(
            self,
            orient="horizontal",
            showhandle=False,
            sashwidth=50,
            height=50,
        ) # height="200", width="200" 
        
        self.print_btn = Button(
            self.btns_panel,
            text=self.translation['fr']['print'],
            # height=50,
            # width=50,
            fg="red"
        )
        self.print_btn.config(command=self.actions['print'])
        self.print_btn.pack(side="left")

        self.cancel_btn = Button(
            self.btns_panel,
            text=self.translation['fr']['cancel'],
            # height=50,
            # width=50,
        )
        self.cancel_btn.config(command=self.actions['cancel'])
        self.cancel_btn.pack(side="right")

        self.loading_label = Label(self, text=self.translation['fr']['loading'])

    def __init__(self, actions, master=None):
        PanedWindow.__init__(self, master, orient="vertical")
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

        