# user_dao_odbc.py
import pyodbc
from dao import IUserDAO

class UserDAO_ODBC(IUserDAO):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_all_users(self):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Applicants")
        rows = cursor.fetchall()

        conn.close()

        return rows