# Паттерн Фабричный Метод (Factory Method) в PyQt5

## Краткое объяснение паттерна

**Фабричный метод (Factory Method)** — это порождающий паттерн, который позволяет создавать объекты, не привязываясь к их конкретному классу. Вместо прямого вызова конструктора объект создаётся с помощью фабрики (класса или метода), которая сама решает, какой конкретный продукт вернуть.

Зачем это нужно:

* упрощает расширение (добавили новый тип — создали новую фабрику);
* отделяет логику выбора объекта от места, где объект используется;
* уменьшает связанность модулей.

В этом примере фабрики создают разные типы кнопок PyQt5: красную, плоскую и кнопку с иконкой.

---

# Полный код примера

(README ниже объясняет работу именно этого примера)

```python
import sys
from abc import ABC, abstractmethod
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

class AbstractButtonFactory(ABC):
    @abstractmethod
    def create_button(self, button_type:str) -> QtWidgets.QPushButton:
        pass

class RedButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        button.setStyleSheet("""
                             background-color:red;
                             color:white;
                             """)
        return button
    
class flatButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        button.setFlat(True)
        return button
    
class IconButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        icon_path = 'dababy.jpg'
        icon = QIcon(icon_path)
        button.setIcon(icon)
        return button
    
class Selector:
    @staticmethod
    def choose_button(button_type:str) -> AbstractButtonFactory:
        if button_type == "red":
            return RedButtonFactory()
        elif button_type == "flat":
            return flatButtonFactory()
        elif button_type == "icon":
            return IconButtonFactory()
        else:
            raise ValueError("Неизвестный тип кнопки :@")
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.vertical_layout= QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.vertical_layout)
        self.line_edit = QtWidgets.QLineEdit()
        self.vertical_layout.addWidget(self.line_edit)
        self.send_button = QtWidgets.QPushButton("push for choose color")
        self.send_button.clicked.connect(self.on_button_clicked)
        self.vertical_layout.addWidget(self.send_button)
        self.setCentralWidget(self.widget)

    def on_button_clicked(self):
        for i in range (int(self.line_edit.text())):
            button = QtWidgets.QPushButton("Кнопка номер: %s"%(i+1))
            self.vertical_layout.addWidget(button)
        # Пример правильного использования фабрики:
        # self.factory = Selector.choose_button(self.line_edit.text())
        # self.button = self.factory.create_button("")
        # self.vertical_layout.addWidget(self.button)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
```

---

# Подробное объяснение паттерна в примере

## 1. Абстрактная фабрика кнопок

`AbstractButtonFactory` задаёт общий интерфейс:

```python
class AbstractButtonFactory(ABC):
    @abstractmethod
    def create_button(self, button_type):
        pass
```

Любая фабрика обязана реализовать метод `create_button()`.

---

## 2. Конкретные фабрики (разные виды кнопок)

### ✔ Красная кнопка

```python
class RedButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        button.setStyleSheet("background-color:red; color:white;")
        return button
```

### ✔ Плоская кнопка

```python
class flatButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        button.setFlat(True)
        return button
```

### ✔ Кнопка с иконкой

```python
class IconButtonFactory(AbstractButtonFactory):
    def create_button(self, button_type):
        button = QtWidgets.QPushButton()
        button.setIcon(QIcon('dababy.jpg'))
        return button
```

Каждая фабрика создаёт кнопку по-своему.

---

## 3. Selector — выбор нужной фабрики

```python
class Selector:
    @staticmethod
    def choose_button(button_type):
        if button_type == "red": return RedButtonFactory()
        if button_type == "flat": return flatButtonFactory()
        if button_type == "icon": return IconButtonFactory()
        raise ValueError("Неизвестный тип кнопки")
```

Этот класс инкапсулирует выбор конкретной фабрики.

---

## 4. MainWindow — использование фабричного метода

Пользователь вводит тип кнопки → выбирается фабрика → создаётся кнопка.

```python
self.factory = Selector.choose_button(self.line_edit.text())
self.button = self.factory.create_button("")
self.vertical_layout.addWidget(self.button)
```

GUI **не знает**, какой именно класс кнопки создаётся.

Именно это и достигается фабричным методом.

---

# Что демонстрирует пример

### ✔ Абстракция создания объектов

UI не зависит от конкретного типа кнопки.

### ✔ Лёгкое добавление новых типов

Чтобы добавить новый тип кнопки, нужно:

1. создать новую фабрику, наследуя `AbstractButtonFactory`;
2. добавить условие в Selector.

### ✔ Уменьшение связанности

Логика выбора объектов вынесена из UI.

### ✔ Простой и понятный пример Factory Method

Каждая фабрика создаёт кнопку по своему "рецепту".
