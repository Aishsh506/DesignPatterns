# Паттерн Observer в PyQt5 — наглядная демонстрация

## Краткое объяснение Observer

**Observer (Наблюдатель)** — это поведенческий паттерн проектирования, при котором один объект (**Subject / Observable**) уведомляет множество других объектов (**Observers**) об изменениях своего состояния.

Применяется, когда:

* несколько элементов интерфейса должны реагировать на одно изменение данных;
* требуется автоматическая синхронизация между данными и отображением;
* нужно избежать жёсткой связанности между моделью и отображением.

**Ключевая идея:** объект *модели* не знает, кто именно за ним наблюдает — он просто вызывает `notify()`, а наблюдатели сами обновляют себя.

---

# Структура проекта

```
project/
│
└── main.py   # Модель + наблюдатели + окно PyQt5
```

---

# Полный код примера

(данный README объясняет работу следующего примера)

```python
from PyQt5 import QtWidgets

class Model:
    def __init__(self):
        self._value = 0
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._value)

    def set_value(self, value):
        self._value = value
        self.notify()
    
    def get_value(self):
        return self._value
    
class LabelObserver(QtWidgets.QLabel):
    def update(self, value):
        self.setText(str(value))

class ProgressBarObserver(QtWidgets.QProgressBar):
    def update(self, value):
        self.setValue(value)

class LCDObserver(QtWidgets.QLCDNumber):
    def update(self, value):
        self.display(value)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()
        self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setRange(0, 100)
        self.button = QtWidgets.QPushButton('Изменить значение')
        self.button.clicked.connect(self.change_value)
        self.label_observer = LabelObserver()
        self.progress_bar_observer = ProgressBarObserver()
        self.lcd_observer = LCDObserver()
        self.model.attach(self.label_observer)
        self.model.attach(self.progress_bar_observer)
        self.model.attach(self.lcd_observer)
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.addWidget(self.spin_box)
        self.vertical_layout.addWidget(self.button)
        self.vertical_layout.addWidget(self.label_observer)
        self.vertical_layout.addWidget(self.progress_bar_observer)
        self.vertical_layout.addWidget(self.lcd_observer)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.vertical_layout)
        self.setCentralWidget(self.widget)

    def change_value(self):
        value = self.spin_box.value()
        self.model.set_value(value)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
```

---

# Подробное объяснение

## 1. Model — объект, за которым наблюдают

`Model` хранит значение и список наблюдателей.

Методы:

* `attach()` — подписка
* `detach()` — отписка
* `notify()` — уведомление всех наблюдателей
* `set_value()` — изменение состояния и автоматическое оповещение

Модель не знает, какие именно объекты за ней наблюдают. Это снижает связанность.

---

## 2. Observers — элементы интерфейса, реагирующие на изменения

Каждый наблюдатель реализует метод `update(value)`.

Например:

* `LabelObserver` обновляет текст
* `ProgressBarObserver` обновляет полосу прогресса
* `LCDObserver` обновляет цифровой дисплей

Каждый сам решает, *как* обработать изменение.

---

## 3. MainWindow — связывает всё вместе

В конструкторе:

* создается `Model`
* создаются UI-компоненты-наблюдатели
* каждый наблюдатель подписывается на модель

```python
self.model.attach(self.label_observer)
self.model.attach(self.progress_bar_observer)
self.model.attach(self.lcd_observer)
```

При нажатии кнопки значение меняется и вызывается `notify()`.

Все наблюдатели обновляются автоматически:

```
label → текст
progress bar → положение
LCD → цифровое значение
```

---

# Что демонстрирует этот пример

### ✔ Правильное отделение данных от отображения

UI не опрашивает модель — **модель сама сообщает об изменениях**.

### ✔ Несколько независимых наблюдателей

Каждый элемент интерфейса реагирует по-своему.

### ✔ Лёгкое расширение

Можно добавить новый отображающий элемент, просто создав новый класс Observer.

### ✔ Отсутствие жёсткой связанности

Модель не зависит от PyQt — она просто вызывает метод `update()` у наблюдателей.
