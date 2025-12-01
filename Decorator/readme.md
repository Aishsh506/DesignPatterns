# Паттерн Decorator в PyQt5 — подробное объяснение

## Краткое объяснение Decorator

**Decorator (Декоратор)** — это структурный паттерн проектирования, который позволяет динамически добавлять объекту новое поведение, не изменяя его класс.

Используется, когда нужно:

* расширять функциональность объектов без наследования,
* комбинировать поведение «цепочкой»,
* гибко подключать и отключать дополнительные функции.

Вместо того чтобы создавать подкласс кнопки с новым поведением, мы создаём **декоратор**, который оборачивает кнопку и добавляет логику, не меняя исходный объект.

---

# Код примера

```python
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QApplication

class ButtonDecorator:
    def __init__(self, button):
        self.button = button
        self.next = None  # ЗДЕСЬ ХРАНИМ ССЫЛКУ НА СЛЕДУЮЩИЙ ДЕКОРАТОР

    def set_next(self, decorator):
        self.next = decorator
        return decorator

    def click(self):
        if self.next:
            self.next.click()

class LoggingDecorator(ButtonDecorator):
    def __init__(self, button):
        super().__init__(button)

    def click(self):
        print("[LOG] Button pressed")
        super().click()

class CounterDecorator(ButtonDecorator):
    def __init__(self, button):
        super().__init__(button)
        self.count = 0

    def click(self):
        self.count += 1
        print(f"[COUNT] {self.count}")
        super().click()

class StyleDecorator(ButtonDecorator):
    def __init__(self, button):
        super().__init__(button)
        button.setStyleSheet("background: red; color: white;")

    def click(self):
        # этот декоратор не добавляет поведения
        super().click()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        btn = QPushButton("Click me")

        self.widget = QWidget()

        # создаём декораторы
        self.log = LoggingDecorator(btn)
        counter = self.log.set_next(CounterDecorator(btn))
        counter.set_next(StyleDecorator(btn))

        # Когда нажата кнопка → вызвать первый декоратор
        btn.clicked.connect(self.log.click)

        layout.addWidget(btn)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
```

---

# Как работает этот пример

## 1. Базовый класс `ButtonDecorator`

Это обёртка над кнопкой.

Он содержит:

* ссылку на кнопку,
* ссылку на следующий декоратор в цепочке.

Метод `click()` передаёт управление дальше.

## 2. Конкретные декораторы

Каждый декоратор добавляет новое поведение к событию нажатия.

### ✔ LoggingDecorator

Печатает лог:

```
[LOG] Button pressed
```

### ✔ CounterDecorator

Считает количество нажатий:

```
[COUNT] 1
[COUNT] 2
...
```

### ✔ StyleDecorator

Применяет стиль к кнопке, но не изменяет поведение.

```python
button.setStyleSheet("background: red; color: white;")
```

## 3. Цепочка декораторов

Построение цепочки:

```python
self.log = LoggingDecorator(btn)
counter = self.log.set_next(CounterDecorator(btn))
counter.set_next(StyleDecorator(btn))
```

Цепочка выглядит так:

```
Logging → Counter → Style
```

Когда кнопка нажата:

1. вызывается первый декоратор → LoggingDecorator
2. он вызывает следующий → CounterDecorator
3. тот вызывает следующий → StyleDecorator
4. цепочка завершается

---

# Что демонстрирует этот пример

### ✔ Динамическое добавление поведения кнопке

Поведение можно менять во время выполнения, не изменяя кнопку.

### ✔ Гибкая композиция функциональности

Поведение комбинируется через цепочку декораторов.

### ✔ Отсутствие необходимости в наследовании от QPushButton

Мы не создаём `LoggingButton`, `CountingButton`, `StyledCountingLoggingButton` — всё решается комбинацией.

### ✔ Минимальная связанность

Кнопка не знает про декораторы.
