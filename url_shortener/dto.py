"""
dto stands for Data Transfer Object
"""
import logging
log = logging.getLogger(__name__)

class User:
    id: int
    email: str
    password: str
    username: str
    urls: [str]

    def __init__(self, email, username, password, id):
        self.username = username
        self.password = password
        self.email = email
        self.id = id
        self.urls = []

    def print_values(self):
        log.info(f'Username: {self.username}' +
                 f'\nPassword: {self.password}' +
                 f'\nEmail: {self.email}' +
                 f'\nID: {self.id}' +
                 f'\nToken: {self.token}' +
                 f'\nURLs: {self.urls}')
