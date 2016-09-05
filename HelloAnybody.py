
import sys
from PyQt5 import QtWidgets, QtCore, uic

class HelloAnybodyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super(HelloAnybodyMainWindow, self).__init__(*args)

        uic.loadUi('HelloAnybody.ui', self)

        # just for type hinting (for IDE autocompletion)
        if False:
            self.nameLineEdit = self.nameLineEdit  # type: QtWidgets.QLineEdit

    @QtCore.pyqtSlot()
    def on_helloWorldButton_clicked(self):
        print("Hello %s!" %(self.nameLineEdit.text()))
        msgBox = QtWidgets.QMessageBox()
        msgBox.setInformativeText("Hello %s!" %(self.nameLineEdit.text()))
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Hinweis")
        msgBox.exec()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = HelloAnybodyMainWindow()
    widget.show()
    sys.exit(app.exec_())