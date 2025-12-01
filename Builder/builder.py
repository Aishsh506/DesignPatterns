from abc import ABC,abstractmethod
from PyQt5 import QtWidgets,QtGui
import sys

class DialogBuilder(ABC):
    def __init__(self):
        self.dialog=QtWidgets.QDialog()
        self.layout=QtWidgets.QVBoxLayout()
        self.dialog.setLayout(self.layout)
    @abstractmethod

    def add_title(self,text):
        pass
    @abstractmethod

    def add_fields(self,fields):
        pass
    @abstractmethod

    def add_buttons(self):
        pass

    def get_result(self):
        return self.dialog
    
class SimpleDialog(DialogBuilder):
    def add_title(self, text):
        label=QtWidgets.QLabel(text)
        label.setFont(QtGui.QFont("Colibri",14))
        self.layout.addWidget(label)
    def add_fields(self, fields):
        self.inputs={}
        for field in fields:
            label=QtWidgets.QLabel(field)
            edit=QtWidgets.QLineEdit()
            self.layout.addWidget(label)
            self.layout.addWidget(edit)
            self.inputs[field]=edit

    def add_buttons(self):
        button=QtWidgets.QPushButton("PIFPAFPUSH")
        button.clicked.connect(self.dialog.accept)
        self.layout.addWidget(button)
class StyleDialogBuilder(DialogBuilder):
    def add_title(self, text):
        label=QtWidgets.QLabel(text)
        label.setFont(QtGui.QFont("Colibri",14))
        label.setStyleSheet("color:darkblue;font-weight:bolt;")
        self.layout.addWidget(label)

    def add_fields(self, fields):
        self.inputs={}
        for field in fields:
            label=QtWidgets.QLabel(field)
            label.setStyleSheet("color:green;font-weight:bolt;")
            edit=QtWidgets.QLineEdit()
            edit.setStyleSheet("color:pink;font-weight:bolt;")
            self.layout.addWidget(label)
            self.layout.addWidget(edit)
            self.inputs[field]=edit

    def add_buttons(self):
        button=QtWidgets.QPushButton("PIFPAFPUSH")
        button.clicked.connect(self.dialog.accept)
        self.layout.addWidget(button)
        button.setStyleSheet("background-color:#fcfcfc;color:pink;font-weight:bolt;")
class DialogDirector:
    def __init__(self,builder:DialogBuilder):
        self.builder=builder

    def construct(self,title,fields):
        self.builder.add_title(title)
        self.builder.add_fields(fields)
        self.builder.add_buttons()
        return self.builder.get_result()
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.vertical_layout)
        self.line_edit = QtWidgets.QLineEdit()
        self.vertical_layout.addWidget(self.line_edit)
        self.simple_button = QtWidgets.QPushButton("Simple")
        self.simple_button.clicked.connect(self.showsimpledialog)
        self.vertical_layout.addWidget(self.simple_button)
        self.style_button = QtWidgets.QPushButton("style")
        self.style_button.clicked.connect(self.showstyledialog)
        self.vertical_layout.addWidget(self.style_button)
        self.setCentralWidget(self.widget)

    def showsimpledialog(self):
        builder = SimpleDialog()
        director = DialogDirector(builder)
        dialog = director.construct("Dima", ["Email", "Password"])
        dialog.exec_()

    def showstyledialog(self):
        builder = StyleDialogBilder()
        director = DialogDirector(builder)
        dialog = director.construct("Dima", ["Email", "Password"])
        dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
