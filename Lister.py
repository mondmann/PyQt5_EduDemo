# coding=utf-8
import sip
import sys
import traceback
import ctypes
from enum import Enum
from sys import platform as _platform

from PyQt5 import QtWidgets, QtCore, QtGui, uic

DEBUG = True

BUTTON_EDIT_TEXT = "Ändern"
BUTTON_ADD_TEXT = "Hinzufügen"


def debug(text=None):
    """display debugging message
    :param text: optional text to display
    """
    if not DEBUG:  # only run if debugging is enabled
        return

    # discover calling point
    res = traceback.extract_stack(limit=2)
    filename, lineno, functionname, message = res[0]  # get lasst calling data

    if text is None:
        print("%s(...):%d" % (functionname, lineno))
    else:
        print("%s(...):%d: %s" % (functionname, lineno, text))


class Modes(Enum):
    insert = 0  # insert is default
    edit = 1


class ListerMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super(ListerMainWindow, self).__init__(*args)

        uic.loadUi('list.ui', self)

        self.mode = Modes.insert  # type: Modes

        # just for type hinting (for IDE autocompletion)
        if False:
            self.MainWindow = self.MainWindow  # type: QtWidgets.QMainWindow
            self.centralwidget = self.centralwidget  # type: QtWidgets.QWidget
            self.delAllButton = self.delAllButton  # type: QtWidgets.QPushButton
            self.countLabel = self.countLabel  # type: QtWidgets.QLabel
            self.countLcdNumber = self.countLcdNumber  # type: QtWidgets.QLCDNumber
            self.delButton = self.delButton  # type: QtWidgets.QPushButton
            self.addButton = self.addButton  # type: QtWidgets.QPushButton
            self.editButton = self.editButton  # type: QtWidgets.QPushButton
            self.itemList = self.itemList  # type: QtWidgets.QListWidget
            self.lineEdit = self.lineEdit  # type: QtWidgets.QLineEdit
            self.menubar = self.menubar  # type: QtWidgets.QMenuBar
            self.menuFile = self.menuFile  # type: QtWidgets.QMenu
            self.menuHelp = self.menuHelp  # type: QtWidgets.QMenu
            self.statusbar = self.statusbar  # type: QtWidgets.QStatusBar
            self.actionLoad = self.actionLoad  # type: QtWidgets.QAction
            self.actionSave = self.actionSave  # type: QtWidgets.QAction
            self.actionQuit = self.actionQuit  # type: QtWidgets.QAction
            self.actionAbout = self.actionAbout  # type: QtWidgets.QAction

    @QtCore.pyqtSlot(bool)
    def on_actionLoad_triggered(self, checked):
        debug(str(checked))
        infileName = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Öffnen", directory=None, filter="Textdateien (*.txt)")[0]
        try:
            with open(infileName) as infile:
                self.itemList.clear()
                for line in infile:
                    self.itemList.addItem(line.strip())  # no newlines
                self.updateDelAllButton()
        except OSError as e:
            self.showErrorMessageBox(str(e))

    def showErrorMessageBox(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setInformativeText(message)
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setWindowTitle("Fehler")
        msgBox.exec()

    @QtCore.pyqtSlot(bool)
    def on_actionSave_triggered(self, checked):
        debug(str(checked))
        outfileName = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption="Speichern",
                                                            directory=None, filter="Textdatei (*.txt)")[0]
        try:
            with open(outfileName, "w") as outfile:
                for row in range(self.itemList.count()):
                    outfile.write(self.itemList.item(row).text() + "\n")
        except OSError as e:
            self.showErrorMessageBox(str(e))

    @QtCore.pyqtSlot(bool)
    def on_actionQuit_triggered(self, checked):
        debug(str(checked))
        QtCore.QCoreApplication.exit()

    @QtCore.pyqtSlot(bool)
    def on_actionAbout_triggered(self, checked):
        debug(str(checked))
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("PyQt 5 Demonstration. Version 0.1")
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Über Lister")
        msgBox.exec()

    def updateDelAllButton(self):
        self.delAllButton.setEnabled(0 != self.itemList.count())

    def updateItemCount(self):
        self.countLcdNumber.display(self.itemList.count())

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        text = self.lineEdit.text()
        debug(text)

        if self.mode == Modes.insert:
            self.itemList.addItem(text)
            self.updateItemCount()
        else:
            self.currentItem.setText(text)
            self.leaveEditMode()

        self.lineEdit.setText(None)
        self.lineEdit.setFocus()
        self.updateDelAllButton()

    @QtCore.pyqtSlot()
    def on_delAllButton_clicked(self):
        debug()
        self.itemList.clear()
        self.updateDelAllButton()
        self.updateItemCount()
        if self.mode == Modes.edit:
            self.leaveEditMode()

    @QtCore.pyqtSlot()
    def on_itemList_itemSelectionChanged(self):
        selectedIndexes = self.itemList.selectedIndexes()
        self.delButton.setEnabled(0 != len(selectedIndexes))
        self.editButton.setEnabled(1 == len(selectedIndexes))

        if self.mode == Modes.edit:
            self.leaveEditMode()

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def on_itemList_itemDoubleClicked(self, item):
        if self.mode == Modes.insert:
            self.enterEditMode(item)

    def leaveEditMode(self):
        self.currentItem = None
        self.mode = Modes.insert
        self.addButton.setText(BUTTON_ADD_TEXT)
        self.lineEdit.setStyleSheet("background-color: none;")
        self.editButton.setEnabled(1 == len(self.itemList.selectedIndexes()))

    def enterEditMode(self, item):
        self.editButton.setEnabled(False)
        self.currentItem = item
        self.mode = Modes.edit
        self.addButton.setText(BUTTON_EDIT_TEXT)
        self.lineEdit.setStyleSheet("background-color: yellow;")
        self.lineEdit.setText(item.text())
        self.currentItem = item

    @QtCore.pyqtSlot()
    def on_editButton_clicked(self):
        selectedItems = self.itemList.selectedItems()
        debug(selectedItems)
        self.enterEditMode(selectedItems[0])

    @QtCore.pyqtSlot()
    def on_itemList_itemClicked(self, item):
        if self.mode != Modes.insert:
            self.leaveEditMode()

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        debug(text)
        if 0 == len(text):
            self.addButton.setEnabled(False)
        else:
            self.addButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_delButton_clicked(self):
        if self.mode == Modes.edit:
            self.leaveEditMode()

        selectedItems = self.itemList.selectedItems()
        debug(selectedItems)
        for item in selectedItems:
            sip.delete(item)  # FIXME: not very pythonic, any better ideas?
        self.updateItemCount()

def _setAppIcon(app):
    if _platform == "win32":
        # Windows. It needs some special treatment for correct icon handling
        myappid = 'de.szut.loos.PyQt5Test'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app_icon = QtGui.QIcon()
    app_icon.addFile('icons/document-pictogram-16px.png', QtCore.QSize(16, 16))
    app_icon.addFile('icons/document-pictogram-24px.png', QtCore.QSize(24, 24))
    app_icon.addFile('icons/document-pictogram-32px.png', QtCore.QSize(32, 32))
    app_icon.addFile('icons/document-pictogram-48px.png', QtCore.QSize(48, 48))
    app_icon.addFile('icons/document-pictogram-48px.png', QtCore.QSize(64, 64))
    app_icon.addFile('icons/document-pictogram-256px.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    _setAppIcon(app)
    widget = ListerMainWindow()
    widget.show()
    sys.exit(app.exec_())
