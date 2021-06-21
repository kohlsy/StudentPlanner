import sys
import os
from PyQt4 import QtCore, QtGui, uic, QtSql
import sqlite3
import signup_mod
from signin_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect("studentplanner.db")
        self.ui.btn_login.clicked.connect(self.login)
        self.ui.btn_signup.clicked.connect(self.signup)
        activitytable=""
        self.activitytable=activitytable
        taskstable=""
        self.taskstable=taskstable
        if os.path.exists(dbfile):
             db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
             db.setDatabaseName(dbfile)
             db.open()
             #QtGui.QMessageBox.critical(self,"message", "Database opened")
        else:
             QtGui.QMessageBox.critical(self,"Critical Error", "Database file was not found here")
             return None

    def login(self):
        password=self.ui.lne_password.text()
        newpass=""
        for i in password:
            newpass=newpass+chr(ord(i)+4)
        comma='"'
        cursor=self.conn.cursor()
        select="select * from users where username="+comma+self.ui.lne_username.text()+comma+" and password="+comma+newpass+comma
        print(select)
        cursor.execute(select)
        self.conn.commit()
        r=cursor.fetchall()
        if r==[]:
            QtGui.QMessageBox.critical(self,"Critical Error", "Username or Password incorrect")
        else:
            statement="Update current_user set username="+'"'+str(self.ui.lne_username.text())+'"'+" where user="+"'"+"1"+"'"
            print(statement)
            cursor.execute(statement)
            self.conn.commit()
            self.activitytable=str(self.ui.lne_username.text())+"_activities"
            self.taskstable=str(self.ui.lne_username.text())+"_tasks"
           # app=QtGui.QApplication(sys.argv)
           # sys.exit(app.exec_())
           # self.tables()
            w = QtGui.QWidget()
            QtGui.QMessageBox.information(w, "Message", "You have successfully signed in")
            self.close()

    def signup(self):
        signup = signup_mod.MyForm(self)
        signup.exec()

    def tables(self):
        activity=self.activitytable
        tasks=self.taskstable
        print(activity)
        print(tasks)
        return activity,tasks

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    

