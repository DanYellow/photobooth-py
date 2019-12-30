from tkinter import Label, Button, PanedWindow, Frame
from PIL import ImageTk

import qrcode

from classes.Gallery import Gallery
    

class PhotoboothUi(Frame):
    def create_widgets(self):
        # COLLAGE SCREEN
        self.collage_screen = Frame(self, bg=self['bg'])
        
        self.collage_label = Label(self.collage_screen, image=None, bg=self['bg'])
        self.collage_label.pack(side="top", expand=True, fill="both")

        self.btns_panel = Frame(self.collage_screen, bg = self['bg'])
        self.btns_panel.pack(
            side="bottom",
            expand=True,
            fill='x',
            anchor="s",
        )
        
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
            text=self.translation['fr']['not_print'],
            height=3,
            fg="red",
            font = ('Sans','10','bold')
        )
        self.cancel_btn.config(command=self.actions['not_print'])
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
        self.home_screen = PanedWindow(self, orient = "vertical", bg = self['bg'])

        self.pictures_btn = Button(
            self.home_screen,
            height = 31,
            text = self.translation['fr']['take_pict'],
            command = self.actions['take_pictures']
        )
        self.home_screen.add(self.pictures_btn, pady=10, padx=10)

        qrc_frame = Frame(self, bg=self['bg'])
        self.home_screen.add(qrc_frame, sticky="s", pady=10)

        qrc_title_label = Label(
            qrc_frame, 
            text=self.translation['fr']['access_gallery'],
            fg="black",
            bg=self['bg'],
            font = ('Sans','15', 'bold')
        )
        qrc_title_label.pack()

        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 3,
            border = 2,
        )
        qr.add_data('http://raspberrypi.local/')
        qr.make(fit=True)

        img_tmp = qr.make_image(fill_color="black", back_color="white")
        img = ImageTk.PhotoImage(img_tmp)

        qrc_label = Label(
            qrc_frame,
            image=img, 
            bg = self['bg']
        )
        qrc_label.image = img
        qrc_label.pack()

        qrc_txt_label = Label(
            qrc_frame, 
            text=self.translation['fr']['link_to_gallery'],
            fg="black",
            bg=self['bg'],
            font = ('Sans','10')
        )
        qrc_txt_label.pack()

        self.gallery_bg = Gallery(self.home_screen)
        self.gallery_bg.place(
            relx=0.5, rely=0.5,
            anchor="center",
            relheight=1.0, relwidth=1.0
        )
        self.gallery_bg.lower()

        #PRINTING SCREEN
        self.print_screen = Frame(self, bg="#F0F8FF")
        self.printing_label = Label(
            self.print_screen, 
            text=self.translation['fr']['printing'],
            fg="black",
            bg="blue",
            font = ('Sans','30','bold')
        )
        self.printing_label.place(relx=0.5, rely=0.5, anchor="center")
        self.print_screen.lift()

    def __init__(self, actions, master=None):
        bgc = 'white'
        Frame.__init__(self, master, image = None, bg = bgc, cursor="none")
        self['bg'] = bgc

        self.actions = actions
        self.translation = {
            'fr': {
                'take_pict': "Prendre des photos !",
                'print': 'Imprimer',
                'cancel': "Annuler",
                'not_print': "Ne pas imprimer",
                'last_collage': "Dernier collage",
                'ready': 'Prêt ?',
                'take_another_one': "Prendre une autre photo",
                'loading': "Chargement",
                'printing': "Impression lancée",
                'access_gallery': "Accéder à la galerie",
                'link_to_gallery': "ou \nraspberrypi.local",
            }
        }

        self.pack(
            expand=True,
            fill="both"
        )
        self.create_widgets()
        