from tkinter import *

class PhotoboothUi(Frame):
    def createWidgets(self):
        self.collage_label = Label(self, image=None)

        self.print_btn = Button(self, text=self.translation['fr']['print'])
        self.print_btn.config(command=self.actions['print'])

        self.pictures_btn = Button(self, text=self.translation['fr']['take_pict'])
        self.pictures_btn.config(command=self.actions['take_pictures'])
        self.pictures_btn.pack()

        self.cancel_btn = Button(self, text=self.translation['fr']['cancel'])
        self.cancel_btn.config(command=self.actions['cancel'])

    def __init__(self, actions, master=None):
        Frame.__init__(self, master)
        self.actions = actions
        self.translation = {
            'fr': {
                'take_pict': "Prendre des photos !",
                'print': 'Imprimer',
                'cancel': "Annuler",
                'last_collage': "Dernier collage"
            }
        }

        self.pack()
        self.createWidgets()

        