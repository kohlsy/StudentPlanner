import sys,os
from PyQt4 import QtCore, QtGui, uic,QtSql
import sqlite3
from activities_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect("studentplanner.db")
        self.ui.btn_Add.clicked.connect(self.openAddRow)
        self.ui.btn_Save.clicked.connect(self.openSave)    
        if os.path.exists(dbfile):
            db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(dbfile)
            db.open()
        else:
            QtQui.QMessageBox.critical(self,"Critical Error", "Database file was not found here")
            return None
        self.getuser()
        self.openRetrieve()

    def getuser(self):
        cursor=self.conn.cursor()
        statement="select username from current_user where user="+"'"+"1"+"'"
        cursor.execute(statement)
        self.conn.commit()
        row=cursor.fetchall()
        row=str(row)
        row=row[3:8]
        return row
        
    def openRetrieve(self):
           self.activity=self.getuser()+"_activities"
           print(self.activity)
           self.model=QtSql.QSqlTableModel(self)
           self.model.setTable('"'+self.activity+'"')
           self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
           self.model.select()
           self.ui.tv_data.setModel(self.model)
        #this is where we will bind the event handlers
#This is where we will insert the functions (defs)
    def openAddRow(self):
        self.model.insertRows(self.model.rowCount(),1)
    def openSave(self):
        self.model.submitAll()
        self.model.select()


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
