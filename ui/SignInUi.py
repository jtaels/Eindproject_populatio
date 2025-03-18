import tkinter
import ttkbootstrap as ttkb
from ttkbootstrap import ttk

class SingInUi:

    def __init__(self, controller, main_frame):

        self._controller = controller
        self._root = main_frame

        self._build_form()

    def _submit_open_start_screen(self):
        self._controller.open_start_screen(self._root)

    '''
        
        Submit login form
    
    '''
    def _submit_login(self):
        self._controller.sign_in(self._username_var.get(), self._password_var.get())

    def _build_form(self):

        self._username_var = tkinter.StringVar()
        self._password_var = tkinter.StringVar()

        form_frame = ttk.Labelframe(self._root, text="Aanmelden")

        username_label = ttk.Label(form_frame, text="Gebruikersnaam:")
        username_entry = ttk.Entry(form_frame, textvariable=self._username_var)

        password_label = ttk.Label(form_frame, text="Wachtwoord:")
        password_entry = ttk.Entry(form_frame, show="*", textvariable=self._password_var)

        login_btn = ttk.Button(form_frame, text="Aanmelden", command=self._submit_login)
        start_screen_btn = ttk.Button(form_frame, text="Terug naar startscherm", bootstyle="warning", command=self._submit_open_start_screen)

        username_label.pack(pady=5,padx=100)
        username_entry.pack(pady=5,padx=100)
        password_label.pack(pady=5,padx=100)
        password_entry.pack(pady=5,padx=100)
        login_btn.pack(pady=5, padx=100)
        start_screen_btn.pack(pady=5,padx=100)
        form_frame.pack(pady=10)

    def render(self):
        self._root.mainloop()


if __name__ == "__main__":
    controller = None  # Hier zou je controller logica in kunnen voegen
    ui = SingInUi(controller)
    ui.render()