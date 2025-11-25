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