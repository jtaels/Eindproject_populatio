from setup.generator import Generator

class SetupController:

    def __init__(self, app_controller):

        self._app_controller = app_controller

        self._user_service = app_controller.container.get('user_service')

        self._app_controller = app_controller

    def create_user(self, username:str, password:str, password_repeat:str):

        return self._user_service.create_user(username,password,password_repeat)

    def generate_start_data(self):

        generator = Generator('datasets/gemeente.json',self._app_controller.container)

        generator.run()

    def load_start_screen(self,main_frame):

        self._app_controller.switch_screen("start",main_frame)