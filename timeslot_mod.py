import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3
from timeslot_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        a=""
        self.a=a
        self.ui.setupUi(self)
        self.ui.btn_done.clicked.connect(self.timeslot)
        
    def timeslot(self):
        self.a=self.ui.lne_interval.text()
        x = self.slot()
        print(x)
        self.close()

    def slot(self):
        period=self.a
        return period

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
