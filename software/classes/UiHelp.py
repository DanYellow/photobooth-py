import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
import qrcode, os, PIL, pyqrcode


class UiHelp(tk.Frame):
    def __init__(self, master, texts, *args, **kwargs): 
        self.texts = texts

        tk.Frame.__init__(self, master, *args, **kwargs, bg="#333333")


        self.instructions = {
            'fr': {
                'step1': "Appuyez sur le bouton \"Commencer\"",
                'step2': "Prenez la pose",
                'step3': "Connectez-vous au réseau Wi-Fi \"photomaton\" (mdp: \"photos!!\") ou via",
                'step4': "Accéder à vos photos via raspberrypi.local ou via",
            }
        }
        # self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        navigation = self.create_main_container()
        navigation.place(
            relx=0.5, rely=0.5,
            anchor="center",
            width="465",
            height="700",
        )

        self.create_list_instructions(navigation)

    def create_main_container(self):
        navigation_style_bg = "#333333"

        navigation = tk.Frame(
            self,
            relief="flat",
            borderwidth=3,
            bg=navigation_style_bg,
            highlightthickness=0,
            # highlightbackground="black",
        )

        return navigation

    def create_list_instructions(self, container):
        space_between_instruction = 8
        instruction_container = tk.Frame(
            container,
            bg=self['bg']
        )
        instruction_container.pack(fill="both", expand=1)

        instruction_text_style = tkFont.Font(
            family='DejaVu Sans Mono', 
            size=15
        )

        instruction_number_style = tkFont.Font(
            family='DejaVu Sans Mono Bold', 
            size=35
        )

        instruction_step_1_container = tk.Frame(
            instruction_container,
            bg=self['bg'],
        )
        instruction_step_1_container.pack(fill="x", pady=space_between_instruction)

        instruction_step_1_number = tk.Label(
            instruction_step_1_container,
            text=1,
            justify="left",
            font=instruction_number_style,
            bg=self['bg'],
            foreground="white"
        )

        instruction_step_1_text = tk.Message(
            instruction_step_1_container,
            text=self.instructions['fr']['step1'],
            justify="left",
            font=instruction_text_style,
            bg=self['bg'],
            foreground="white",
            aspect=500
        )

        instruction_step_1_number.pack(side="left")
        instruction_step_1_text.pack(side="left", fill="x")

        instruction_step_2_container = tk.Frame(
            instruction_container,
            bg=self['bg'],
        )
        instruction_step_2_container.pack(fill="x", pady=space_between_instruction)

        instruction_step_2_number = tk.Label(
            instruction_step_2_container,
            text=2,
            justify="left",
            font=instruction_number_style,
            bg=self['bg'],
            foreground="white"
        )

        instruction_step_2_text = tk.Message(
            instruction_step_2_container,
            text=self.instructions['fr']['step2'],
            justify="left",
            font=instruction_text_style,
            bg=self['bg'],
            foreground="white",
            aspect=700
        )

        instruction_step_2_number.pack(side="left")
        instruction_step_2_text.pack(side="left", fill="x")

        instruction_step_3_container = tk.Frame(
            instruction_container,
            bg=self['bg'],
        )
        instruction_step_3_container.pack(fill="x", pady=space_between_instruction)

        instruction_step_3_texts_container = tk.Frame(
            instruction_step_3_container,
            bg=self['bg'],
        )
        instruction_step_3_texts_container.pack(side="top", fill="x")

        instruction_step_3_number = tk.Label(
            instruction_step_3_texts_container,
            text=3,
            justify="left",
            font=instruction_number_style,
            bg=self['bg'],
            foreground="white"
        )

        instruction_step_3_text = tk.Message(
            instruction_step_3_texts_container,
            text=self.instructions['fr']['step3'],
            justify="left",
            font=instruction_text_style,
            bg=self['bg'],
            foreground="white",
            aspect=500
        )

        instruction_step_3_number.pack(side="left")
        instruction_step_3_text.pack(side="left", fill="x")

        site_qr_code = self.get_site_qr_code()
        site_qr_code_label = tk.Label(instruction_step_3_container, image=site_qr_code)
        site_qr_code_label.image = site_qr_code
        site_qr_code_label.pack(side="bottom")


        instruction_step_4_container = tk.Frame(
            instruction_container,
            bg=self['bg'],
        )
        instruction_step_4_container.pack(fill="x", pady=space_between_instruction)

        instruction_step_4_texts_container = tk.Frame(
            instruction_step_4_container,
            bg=self['bg'],
        )
        instruction_step_4_texts_container.pack(side="top", fill="x")

        instruction_step_4_number = tk.Label(
            instruction_step_4_texts_container,
            text=4,
            justify="left",
            font=instruction_number_style,
            bg=self['bg'],
            foreground="white"
        )

        instruction_step_4_text = tk.Message(
            instruction_step_4_texts_container,
            text=self.instructions['fr']['step4'],
            justify="left",
            font=instruction_text_style,
            bg=self['bg'],
            foreground="white",
            aspect=500
        )

        instruction_step_4_number.pack(side="left")
        instruction_step_4_text.pack(side="left", fill="x")

        wifi_qr_code = self.get_wifi_access_qr_code()
        wifi_qr_code_label = tk.Label(instruction_step_4_container, image=wifi_qr_code)
        wifi_qr_code_label.image = wifi_qr_code
        wifi_qr_code_label.pack(side="bottom")

    def get_wifi_access_qr_code(self):
        ssid = 'photomaton'
        security = 'WPA'
        password = 'photos!!'
        qr = pyqrcode.create(f'WIFI:S:{ssid};T:{security};P:{password};;')
        qr_xbm = qr.xbm(scale=3)
        code_bmp = tk.BitmapImage(data=qr_xbm)
        code_bmp.config(background="white")

        return code_bmp

    def get_site_qr_code(self):
        qr = pyqrcode.create(f'http://raspberrypi.local/')
        qr_xbm = qr.xbm(scale=3)
        code_bmp = tk.BitmapImage(data=qr_xbm)
        code_bmp.config(background="white")

        return code_bmp