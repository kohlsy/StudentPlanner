import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3
from calendar_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_submit.clicked.connect(self.getdate)

    def getdate(self):
        self.x = self.ui.calendarWidget.selectedDate()
        print(self.x)
        return self.x
        self.close()

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    

