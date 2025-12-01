# Паттерн Adapter в PyQt5 — демонстрация на примере кастомного графика

## Краткое объяснение Adapter

**Adapter (Адаптер)** — структурный паттерн, который позволяет объектам с несовместимыми интерфейсами работать вместе.

Применяется, когда:

* существует класс, который *уже написан* и менять его нельзя;
* нужно использовать этот класс там, где ожидается совсем другой тип или интерфейс;
* необходимо встроить нестандартный компонент в существующую архитектуру.

**Идея:** создать промежуточный объект (Adapter), который преобразует интерфейс исходного класса к ожидаемому.

В нашем случае: есть кастомный класс `CustomPlot`, который **не является виджетом PyQt**, значит, его нельзя положить в layout. Адаптер превращает его в `QLabel`, который *можно* отображать.

---

# Полный код примера

Код, который иллюстрируется этим README:

```python
import sys
from abc import ABC, abstractmethod
from PyQt5 import QtWidgets, QtGui, QtCore
import random

# данный класс не является виджетом pyQT, поэтому его нельзя на прямую положить в layout
class CustomPlotIncorrect():
    def __init__(self):
        pass
    
    def draw(self, data):
        pixmap = QtGui.QPixmap(300, 200)
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.black)
        for i in range(len(data) -1):
            painter.drawLine(i*10, 200 - data[i], (i + 1) * 10, 200 - data[i+1])
        painter.end
        return pixmap
    
class CustomPlot:
    def draw(self, data):
        pixmap = QtGui.QPixmap(300, 200)
        pixmap.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.black)
        for i in range(len(data) - 1):
            painter.drawLine(i*10, 200 - data[i], (i+1) * 10, 200 - data[i+1])
        painter.end
        return pixmap
    
class CustomPlotAdapter(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.plot = CustomPlot()

    def updatePlot(self, data):
        pixmap = self.plot.draw(data)
        self.setPixmap(pixmap)
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.plotWidget = CustomPlotAdapter()
        self.vertical_layout= QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.vertical_layout)
        self.line_edit = QtWidgets.QLineEdit()
        self.vertical_layout.addWidget(self.line_edit)
        self.send_button = QtWidgets.QPushButton("press")
        self.vertical_layout.addWidget(self.send_button)
        self.vertical_layout.addWidget(self.plotWidget)
        self.send_button.clicked.connect(self.drawGraph)
        self.setCentralWidget(self.widget)   

    def drawGraph(self):
        data = [random.randint(0, 100) for _ in range(0, 200)]
        self.plotWidget.updatePlot(data)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
```

---

# Подробное объяснение

## 1. Проблема

`CustomPlot` умеет рисовать график, но **не является PyQt-виджетом**.

То есть:

* его нельзя добавить в layout,
* он не наследует `QWidget`,
* он только возвращает `QPixmap`.

Прямо использовать его невозможно.

---

## 2. Решение — Adapter

Мы создаём класс `CustomPlotAdapter`, который:

* наследует `QLabel` (значит, это PyQt-виджет),
* содержит внутри `CustomPlot`,
* преобразует вызов `updatePlot()` → в вызов `draw()` → в отображение `QPixmap`.

```python
class CustomPlotAdapter(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.plot = CustomPlot()

    def updatePlot(self, data):
        pixmap = self.plot.draw(data)
        self.setPixmap(pixmap)
```

Теперь `CustomPlotAdapter` можно положить в layout.

---

## 3. MainWindow — использует адаптированный класс

Окно ничего не знает о `CustomPlot`, оно работает только с адаптером.

```python
self.plotWidget = CustomPlotAdapter()
self.vertical_layout.addWidget(self.plotWidget)
```

При нажатии кнопки генерируются случайные данные, и адаптер обновляет картинку.

---

# Что демонстрирует этот пример

### ✔ Преобразование несовместимого класса в PyQt-виджет

`CustomPlot` становится совместимым с layout через Adapter.

### ✔ Отделение интерфейсов и логики

`CustomPlot` не изменяется — адаптер берёт на себя всю работу по интеграции.

### ✔ Гибкость

Можно легко заменить:

* внутренний механизм рисования,
* логику отображения,
* внешний вид адаптера.

Ни код окна, ни сама модель не изменятся.

### ✔ Иллюстрация «обёртки» над сторонним компонентом

Типичный сценарий Adapter: есть библиотека, которую нельзя модифицировать.
