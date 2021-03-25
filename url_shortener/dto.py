"""
dto stands for Data Transfer Object
"""
from typing import NamedTuple


class User(NamedTuple):
    """Sample User DTO, which is used to represent authenticated user in out system"""
    email: str
