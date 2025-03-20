from db.repositories.UserRepository import UserRepository
from services.userService import UserService
from tkinter import messagebox

class SetupController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        self._user_repository = UserRepository()
        self._user_service = UserService(self._user_repository)

    def create_user(self, username:str, password:str, password_repeat:str):

        return self._user_service.create_user(username,password,password_repeat)

    def load_start_screen(self,main_frame):

        self._app_controller.switch_screen("start",main_frame)