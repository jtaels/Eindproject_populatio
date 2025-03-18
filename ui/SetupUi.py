import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *

class SetupUi:

    def __init__(self, controller,main_frame):

        self._controller = controller
        self._root = main_frame

        self._build_form()

    def _submit_form(self,username_error_label,password_error_label):

        has_errors,errors = self._controller.create_user(self._username_var.get(),self._password_var.get(),self._password_rp_var.get())

        if "username" in errors:

            error_str = ""

            for error in errors["username"]:
                error_str += error + "\n"

            username_error_label.configure(text=error_str)

        if "password" in errors:

            error_str = ""

            for error in errors["password"]:
                error_str += error + "\n"

            password_error_label.configure(text=error_str)

    def _build_form(self):

        self._username_var = tk.StringVar()
        self._password_var = tk.StringVar()
        self._password_rp_var = tk.StringVar()

        form_frame = ttk.Labelframe(self._root, text="Superuser aanmaken")

        username_label = ttk.Label(form_frame, text="Gebruikersnaam:")
        username_entry = ttk.Entry(form_frame, textvariable=self._username_var)
        username_error_label = ttk.Label(form_frame)

        password_label = ttk.Label(form_frame, text="Wachtwoord:")
        password_entry = ttk.Entry(form_frame, show="*", textvariable=self._password_var)
        password_error_label = ttk.Label(form_frame)

        password_rp_label = ttk.Label(form_frame, text="Herhaal wachtwoord:")
        password_rp_entry = ttk.Entry(form_frame, show="*", textvariable=self._password_rp_var)

        login_btn = ttk.Button(form_frame, text="Account aanmaken", command=lambda: self._submit_form(username_error_label,password_error_label))

        username_label.pack(pady=5,padx=100)
        username_entry.pack(pady=5,padx=100)
        username_error_label.pack(pady=5,padx=100)
        password_label.pack(pady=5,padx=100)
        password_entry.pack(pady=5,padx=100)
        password_error_label.pack(pady=5,padx=100)
        password_rp_label.pack(pady=5,padx=100)
        password_rp_entry.pack(pady=5,padx=100)
        login_btn.pack(pady=5, padx=100)
        form_frame.pack(pady=10)

    def render(self):
        self._root.mainloop()