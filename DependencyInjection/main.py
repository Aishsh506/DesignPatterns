# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget
from user_dao_odbc import UserDAO_ODBC

class MainWindow(QWidget):
    def __init__(self, user_dao):
        super().__init__()

        # DAO пришел извне → Dependency Injection
        self.user_dao = user_dao

        self.setWindowTitle("DI + PyQT + pyODBC Example")

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        btn = QPushButton("Load users")
        btn.clicked.connect(self.load_users)
        self.layout.addWidget(btn)

        self.setLayout(self.layout)

    def load_users(self):
        self.list_widget.clear()
        users = self.user_dao.get_all_users()
        for u in users:
            self.list_widget.addItem(f"{u}")

def main():
    app = QApplication(sys.argv)

    # --- Внедрение зависимости ---
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-GGG7RJD\SQLEXPRESS01;"
        "DATABASE=RequestsManagementDB;"
        "Trusted_Connection=yes;"
    )
    user_dao = UserDAO_ODBC(connection_string)

    # DAO передаём в окно — это и есть DI!
    window = MainWindow(user_dao)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
