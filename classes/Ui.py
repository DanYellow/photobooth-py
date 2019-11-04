from tkinter import Label, Button, Frame

class PhotoboothUi(Frame):
    def create_widgets(self):
        self.collage_label = Label(self, image=None)
        # self.collage_label.place(x=70,y=30)
        self.collage_label.pack()

        self.print_btn = Button(self, text=self.translation['fr']['print'], fg="red")
        self.print_btn.config(command=self.actions['print'])

        self.pictures_btn = Button(self, text=self.translation['fr']['take_pict'])
        self.pictures_btn.config(command=self.actions['take_pictures'])
        self.pictures_btn.pack()

        self.cancel_btn = Button(self, text=self.translation['fr']['cancel'])
        self.cancel_btn.config(command=self.actions['cancel'])

        self.loading_label = Label(self, text=self.translation['fr']['loading'])

    def __init__(self, actions, master=None):
        Frame.__init__(self, master)
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

        