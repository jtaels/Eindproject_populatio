import tkinter
from tkinter import messagebox

import ui.StartUi as startUi
import ui.SignInUi as signInUi
from Container import Container
from controller.SetupController import SetupController
from ui.SetupUi import SetupUi
import controller.SignInController as signInController
from controller.DashboardController import DashboardController
from ui.DashboardUi import DashboardUi

class AppController:

    def __init__(self, container:Container):

        self.container = container

        self._user_service = container.get('user_service')
        self._user = None

    def clear_main_frame(self,main_frame):
        for widget in main_frame.winfo_children():
            widget.destroy()

    def switch_screen(self, screen_name,main_frame):

        #Als er geen gebruikers in de database zitten moet er een superuser aangemaakt worden
        if(self._user_service.get_user_count() == 0):
            self.open_setup_screen(main_frame)
            return

        match screen_name:

            case "start":
                self.open_start_screen(main_frame)
            case "signIn":
                self.open_signin_screen(main_frame)
            case "dashboard":
                self.open_dashboard_screen(main_frame)
            case _:
                messagebox.showwarning("Error", "Dit is geen geldig scherm!")

    def open_setup_screen(self,main_frame):
        self.clear_main_frame(main_frame)

        controller = self.container.get('setup_controller')
        ui = SetupUi(controller,main_frame)

    def open_start_screen(self,main_frame):

        self.clear_main_frame(main_frame)

        controller = self.container.get('start_controller')
        ui = startUi.StartUi(controller,main_frame)

    def open_signin_screen(self,main_frame):
        self.clear_main_frame(main_frame)

        controller = signInController.SignInController(self)
        ui = signInUi.SingInUi(controller, main_frame)

    def open_dashboard_screen(self,main_frame):
        self.clear_main_frame(main_frame)

        controller = DashboardController(self)
        ui = DashboardUi(controller, main_frame)

    def set_user(self, user):

        self._user = user

    def get_user(self):

        return self._user