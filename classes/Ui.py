from tkinter import Label, Button, PanedWindow, Frame
import qrcode
from PIL import ImageTk

class PhotoboothUi(Frame):
    def create_widgets(self):
        # COLLAGE SCREEN
        self.collage_label = Label(self, image=None, bg=self['bg'])
        # self.home_screen.add(self.collage_label, pady = (0, 5))


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

        # LOADING SCREEN
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

        # HOME SCREEN
        self.home_screen = PanedWindow(self)
        self.pictures_btn = Button(
            self.home_screen,
            height = 30,
            text = self.translation['fr']['take_pict'],
            command = self.actions['take_pictures']
        )
        self.home_screen.add(self.pictures_btn, pady = (5, 0))

        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 3,
            border = 2,
        )
        qr.add_data('http://photobooth:5000/')
        qr.make(fit=True)

        img_tmp = qr.make_image(fill_color="black", back_color="white")
        img = ImageTk.PhotoImage(img_tmp)

        qrc_label = Label(self, image=img)
        qrc_label.image = img 
        self.home_screen.add(self.collage_label, pady = (5, 0))

    def __init__(self, actions, master=None):
        bgc = 'white'
        Frame.__init__(self, master, image = None, bg = bgc)
        self['bg'] = bgc

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
        