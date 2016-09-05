
import sys
from PyQt5 import QtWidgets, QtCore, uic

class HelloWorldMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super(HelloWorldMainWindow, self).__init__(*args)

        uic.loadUi('HelloWorld.ui', self)


    @QtCore.pyqtSlot()
    def on_helloWorldButton_clicked(self):
        print("Hello World!")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = HelloWorldMainWindow()
    widget.show()
    sys.exit(app.exec_())