from wsgiref.validate import validator
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from applogging.Logger import Logger
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongCredentialsException import WrongCredentialsException
from validator.RegisterFormValidator import  RegisterFormValidator

class UserService:

    def __init__(self, user_repository):

        self._repository = user_repository
        self._hasher = PasswordHasher()

    def get_by_id(self, user_id:int):

        return self._repository.get_by_id(user_id)

    def get_by_username(self, username:str):

        return self._repository.get_by_username(username)

    def login(self, username: str, password:str):

        try:

            user = self.get_by_username(username.lower())

            self._hasher.verify(user.password, password)

            return user

        except UserNotFoundException as e:
            raise e
        except VerifyMismatchError as e:
            raise e

    def get_user_count(self):
        return self._repository.get_user_count()[0]

    def create_user(self, username:str, password:str, password_repeat:str):

        validator = RegisterFormValidator(username,password,password_repeat,self._repository)

        validator.validate()

        errors,_has_errors = validator.get_errors()

        password = self._hasher.hash(password)

        if not _has_errors:

            self._repository.create_user(username,password,100)

            return _has_errors,[]

        return _has_errors,errors