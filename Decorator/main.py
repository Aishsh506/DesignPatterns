from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QApplication

class ButtonDecorator:
    def __init__(self, button):
        self.button = button
        self.next = None # ЗДЕСЬ ХРАНИМ ССЫЛКУ НА СЛЕДУЮЩИЙ ДЕКОРАТОР

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
