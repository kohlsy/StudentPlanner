import sys, os
from PyQt4 import QtCore, QtGui, uic, QtSql
import sqlite3
import createTask_mod
from tasks_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect(dbfile)
        self.taskstable=self.getuser()+"_tasks"
        self.ui.btn_add.clicked.connect(self.openAddRow)
        self.ui.btn_save.clicked.connect(self.openSave)
        self.ui.btn_filtersort.clicked.connect(self.filtersort)
        if os.path.exists(dbfile):
            db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(dbfile)
            db.open()
            #QtGui.QMessageBox.critical(self,"message", "Database opened")
        else:
            QtGui.QMessageBox.critical(self,"Critical Error", "Database file was not found here")
            return None
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
        self.tasks=self.getuser()+"_tasks"
        print(self.tasks)
        self.model=QtSql.QSqlTableModel(self)
        self.model.setTable('"'+self.tasks+'"')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.ui.tv_data.setModel(self.model)
        
        #self.model = QtSql.QSqlQueryModel(self)
        #print(self.taskstable)
        #query="select task_id, task_name,task_activity,task_type,assigned_by,duration,start_date,end_date,user_priority from "+'"'+self.taskstable+'"'
        #print(query)
        #self.model.setQuery(query)
        #self.ui.tv_data.setModel(self.model) 

    def openAddRow(self):
        addtask = createTask_mod.MyForm(self)
        addtask.exec()
        
    def openSave(self):
        self.close()
        self.model.submitAll()
        self.model.select()

    def filtersort(self):
        direction = "asc"
        filt=str(self.ui.cb_options.currentText())
        sort=str(self.ui.cb_sort.currentText())
        filtline=str(self.ui.lne_filter.text())
        self.model = QtSql.QSqlQueryModel(self)
        
        if sort=="total_priority":
            direction = "desc"
        print(self.taskstable)
        if sort=="end_date":
            sort=" SUBSTR(end_date, 7,10) asc,substr(end_date,4,5) asc, substr(end_date,1,2),SUBSTR(start_date, 7,10) asc,substr(start_date,4,5) asc, substr(start_date,1,2) "
        if sort=="start_date":
            sort=" SUBSTR(start_date, 7,10) asc,substr(start_date,4,5) asc, substr(start_date,1,2),SUBSTR(end_date, 7,10) asc,substr(end_date,4,5) asc, substr(end_date,1,2) "
        query = "select * from "+self.taskstable+" where "+filt+" = "+'"'+filtline+'"'+" order by "+sort+" "+direction+";"
        print(query)
        self.model.setQuery(query)
        self.ui.tv_data.setModel(self.model)

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
