# dao.py
from abc import ABC, abstractmethod

class IUserDAO(ABC):
    @abstractmethod
    def get_all_users(self):
        pass