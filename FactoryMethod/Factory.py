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
        # self.factory = Selector.choose_button(self.line_edit.text())
        # self.button = self.factory.create_button("")
        # self.vertical_layout.addWidget(self.button)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
