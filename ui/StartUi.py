import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap import ttk
import controller.StartController as StartController
from ttkbootstrap.constants import *

class StartUi:

    def __init__(self, controller,main_frame):

        self._controller = controller
        self._root = main_frame

        self._build_form()

    def _submit_form(self):

        self._controller.handle_request_adreshistoriek(self._bevolkingsregisternr.get())

    def _submit_open_sign_in_screen(self):
        self._controller.open_sign_in_screen(self._root)

    def _build_form(self):

        self._bevolkingsregisternr = tk.StringVar()

        form_frame = ttk.Labelframe(self._root, bootstyle="solid", text="Adreshistoriek opvragen")

        bevolkingsreg_nr_label = ttkb.Label(form_frame, text="Bevolkingsregisternummer:")
        bevolkingsreg_nr_entry = ttkb.Entry(form_frame,textvariable=self._bevolkingsregisternr)
        request_btn = ttkb.Button(form_frame, text="Adreshistoriek opvragen", command=self._submit_form)
        signin_btn = ttkb.Button(form_frame, text="Aanmelden medewerker", bootstyle="warning", command=self._submit_open_sign_in_screen)

        bevolkingsreg_nr_label.pack(pady=5,padx=100)
        bevolkingsreg_nr_entry.pack(pady=5,padx=100)
        request_btn.pack(pady=5,padx=100)
        signin_btn.pack(pady=5,padx=100)
        form_frame.pack(pady=5)