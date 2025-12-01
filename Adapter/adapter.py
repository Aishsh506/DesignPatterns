import sys
from abc import ABC, abstractmethod
from PyQt5 import QtWidgets, QtGui, QtCore
import random
#данный класс не является виджетом pyQT, поэтому его нельзя на прямую положить в layout
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