import sys,time
from PyQt4 import QtCore, QtGui, uic, QtSql
import sqlite3
from signup_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_done.clicked.connect(self.process)
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect("studentplanner.db")

    def process(self):
        cursor=self.conn.cursor()
        comma='"'
        select="select * from users where username="+comma+self.ui.lne_username.text()+comma
        cursor.execute(select)
        self.conn.commit()
        r=cursor.fetchall()
        newpass=""
        password=str(self.ui.lne_password.text())
        for i in password:
            newpass=newpass+chr(ord(i)+4)
        if r==[] and self.ui.lne_password.text()==self.ui.lne_confirm.text():
            self.tableactivities=str(self.ui.lne_username.text())+"_activities"
            self.tabletasks=str(self.ui.lne_username.text())+"_tasks"
            statement1="insert into users (username,password) values ("+comma+self.ui.lne_username.text()+comma+","+comma+newpass+comma+");"
            print(statement1)
            cursor.execute(statement1)
            self.conn.commit()
            statement2="CREATE TABLE `"+self.tabletasks+"` (`task_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`task_name`	INTEGER NOT NULL,`task_activity`	INTEGER NOT NULL,`task_type`	INTEGER NOT NULL,`assigned_by`	INTEGER NOT NULL,`duration`	INTEGER NOT NULL,`start_date`	DATE NOT NULL,`end_date`	DATE NOT NULL,`user_priority`	INTEGER NOT NULL,`date_priority`	INTEGER NOT NULL,`total_priority`	INTEGER NOT NULL,`status`	TEXT NOT NULL);"
            print(statement2)
            cursor.execute(statement2)
            statement3="CREATE TABLE `"+self.tableactivities+"` (`activity_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`activity_name`	varchar(100) NOT NULL UNIQUE,`activity_type`	varchar(20) NOT NULL);"
            print(statement3)
            cursor.execute(statement3)
            w = QtGui.QWidget()      
            QtGui.QMessageBox.information(w, "Message", "You have been signed up")
            self.close()
            
        elif r==[] and self.ui.lne_password.text()!=self.ui.lne_confirm.text():
            QtGui.QMessageBox.critical(self,"Critical Error", "Passwords do not match. Please try again.")
            
        else:
            QtGui.QMessageBox.critical(self,"Critical Error", "Username already taken. Please try again.")

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    

