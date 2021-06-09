"""
dto stands for Data Transfer Object
"""
from typing import NamedTuple


class User:
    id: int
    email: str
    password: str
    username: str
    token: str
    urls: [str]

    def __init__(self, email, username, password, id):
        self.username = username
        self.password = password
        self.email = email
        self.id = id
        self.urls = []
        self.generate_token()


    def generate_token(self):
        self.token = hash(self.username)

    def print_values(self):
        print(f'Username: {self.username}')
        print(f'Password: {self.password}')
        print(f'Email: {self.email}')
        print(f'ID: {self.id}')
        print(f'Token: {self.token}')
        print(f'URLs: {self.urls}')

