import ui.SignInUi as signInUi
import controller.SignInController as signInController
import tkinter
class StartController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

    '''

        Gebruiker doet aanvraag om gezinssamenstelling en adreshistoriek op te vragen

    '''
    def handle_request_gezinssamenstelling(self, bevolkingsregisternummer:str):
        print(bevolkingsregisternummer)

    def open_sign_in_screen(self,main_frame):

        self._app_controller.switch_screen('signIn', main_frame)