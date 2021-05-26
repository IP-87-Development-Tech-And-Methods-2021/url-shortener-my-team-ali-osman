"""
dto stands for Data Transfer Object
"""
from typing import NamedTuple


class User(NamedTuple):
    """Sample User DTO, which is used to represent authenticated user in out system"""
    id: int
    email: str
    password: str
    username: str
    token: str

    def generate_token(self):
        self.token = hash(self.username)

    # def __init__(self, email, username, password, id):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.id = id
    #     self.generateToken()


