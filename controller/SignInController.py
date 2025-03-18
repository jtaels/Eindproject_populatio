from db.repositories.UserRepository import UserRepository
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongCredentialsException import WrongCredentialsException
from services.userService import UserService
from tkinter import messagebox

class SignInController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        self._user_repository = UserRepository()
        self._user_service = UserService(self._user_repository)

    def open_start_screen(self,main_frame):
        self._app_controller.switchScreen('start', main_frame)

    def sign_in(self,username:str,password:str):

        try:

            user = self._user_service.login(username,password)

        except UserNotFoundException as e:
            messagebox.showerror("Error", "Gebruikersnaam of wachtwoord is verkeerd!")
        except WrongCredentialsException as e:
            messagebox.showerror("Error", "Gebruikersnaam of wachtwoord is verkeerd!")