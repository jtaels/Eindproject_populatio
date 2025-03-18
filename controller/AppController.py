from tkinter import messagebox

import ui.StartUi as startUi
import ui.SignInUi as signInUi
from controller.SetupController import SetupController
from ui.SetupUi import SetupUi
import controller.SignInController as signInController
from controller.StartController import StartController
from db.repositories.UserRepository import UserRepository
from services.userService import UserService

class AppController:

    def __init__(self):

        self._user_repository = UserRepository()
        self._user_service = UserService(self._user_repository)

    def clear_main_frame(self,main_frame):
        for widget in main_frame.winfo_children():
            widget.destroy()

    def switch_screen(self, screen_name,main_frame):

        #Als er geen gebruikers in de database zitten moet er een superuser aangemaakt worden
        if(self._user_service.get_user_count() == 0):
            self.open_setup_screen(main_frame)

        match screen_name:

            case "start":
                self.open_start_screen(main_frame)
            case "signIn":
                self.open_signin_screen(main_frame)
            case _:
                messagebox.showwarning("Error", "Dit is geen geldig scherm!")

    def open_setup_screen(self,main_frame):
        self.clear_main_frame(main_frame)

        controller = SetupController(self)
        ui = SetupUi(controller,main_frame)

        ui.render()

    def open_start_screen(self,main_frame):

        self.clear_main_frame(main_frame)

        controller = StartController(self)
        ui = startUi.StartUi(controller,main_frame)

        ui.render()

    def open_signin_screen(self,main_frame):
        self.clear_main_frame(main_frame)

        controller = signInController.SignInController(self)
        ui = signInUi.SingInUi(controller, main_frame)

        ui.render()