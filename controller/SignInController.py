from argon2.exceptions import VerifyMismatchError

from applogging.Logger import Logger
from db.repositories.UserRepository import UserRepository
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongCredentialsException import WrongCredentialsException
from services.UserService import UserService
from tkinter import messagebox

class SignInController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        self._user_service = app_controller.container.get('user_service')

    def open_start_screen(self,main_frame):
        self._app_controller.switch_screen('start', main_frame)

    def open_dashboard_screen(self,main_frame):
        self._app_controller.switch_screen('dashboard', main_frame)

    def sign_in(self,username:str,password:str,main_frame):

        try:

            user = self._user_service.login(username.lower(),password)

            Logger.info(username + " is succesvol ingelogd!")

            self._app_controller.set_user(user)

            self.open_dashboard_screen(main_frame)

        except UserNotFoundException as e:
            Logger.info(e.message)
            messagebox.showerror("Error", "Gebruikersnaam of wachtwoord is verkeerd!")
        except VerifyMismatchError as e:
            Logger.info(username + " voerde een foutief paswoord in!")
            messagebox.showerror("Error", "Gebruikersnaam of wachtwoord is verkeerd!")