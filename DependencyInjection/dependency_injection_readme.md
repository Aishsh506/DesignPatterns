# Dependency Injection (DI) в PyQt5 + pyODBC

## Краткое объяснение Dependency Injection
**Dependency Injection (DI)** — это принцип, при котором объекты не создают свои зависимости сами, а получают их извне. Это позволяет:
- разделять бизнес-логику и инфраструктуру (например, доступ к базе данных);
- упрощать тестирование (можно подменить зависимости на mock);
- делать код гибким и расширяемым (можно сменить реализацию без изменения логики интерфейса).

Вместо того чтобы окно само создавало объект доступа к базе, мы передаём ему DAO извне. Это и есть внедрение зависимостей.

---

# Пример DI в приложении PyQt5 с использованием pyODBC
Проект состоит из следующих частей:

```
project/
│
├── dao.py              # интерфейс DAO
├── user_dao_odbc.py    # реализация DAO через pyODBC
└── main.py             # GUI + внедрение зависимости
```

---

## dao.py — интерфейс DAO
Задаётся абстракция, с которой будет работать UI.

```python
from abc import ABC, abstractmethod

class IUserDAO(ABC):
    @abstractmethod
    def get_all_users(self):
        pass
```

UI знает только про интерфейс, а не про конкретную реализацию.

---

## user_dao_odbc.py — реализация DAO через pyODBC
Здесь описывается, как получать данные из базы.

```python
import pyodbc
from dao import IUserDAO

class UserDAO_ODBC(IUserDAO):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_all_users(self):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM Users")
        rows = cursor.fetchall()

        conn.close()

        return rows
```

Важный момент: UI ничего не знает ни о строке подключения, ни о pyODBC — это сохраняет слабую связанность.

---

## main.py — окно PyQt5, которое получает DAO через DI
GUI получает реализацию DAO в конструктор.

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget
from user_dao_odbc import UserDAO_ODBC

class MainWindow(QWidget):
    def __init__(self, user_dao):
        super().__init__()
        self.user_dao = user_dao  # Dependency Injection

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
            self.list_widget.addItem(f"{u.id} — {u.name}")


def main():
    app = QApplication(sys.argv)

    # Создаём реализацию DAO
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=TestDB;"
        "Trusted_Connection=yes;"
    )
    user_dao = UserDAO_ODBC(connection_string)

    # Внедряем зависимость в окно
    window = MainWindow(user_dao)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```

---

# Что здесь демонстрируется
### ✔ Интерфейс + реализация
UI работает только с `IUserDAO`, реализация может быть любой.

### ✔ Dependency Injection через конструктор
```python
window = MainWindow(user_dao)
```

### ✔ Ослабление связности
Окно не знает:
- какая используется база,
- какой драйвер,
- какая строка подключения.

### ✔ Гибкость
Можно подменить `UserDAO_ODBC` на:
- фейковый DAO для тестов,
- DAO для SQLite,
- DAO для REST API.

И при этом *не менять ни одной строки в UI*.
