import sys, os, datetime
from PyQt4 import QtCore, QtGui, uic, QtSql
import sqlite3
import calendar_mod
from createTask_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect(dbfile)
        self.ui.btn_start.clicked.connect(self.start)
        self.ui.btn_end.clicked.connect(self.end)
        self.ui.btn_process.clicked.connect(self.process)
        if os.path.exists(dbfile):
            db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(dbfile)
            db.open()
        else:
            QtQui.QMessageBox.critical(self,"Critical Error", "Database file was not found here")
            return None
        self.display()

    def getuser(self):
        cursor=self.conn.cursor()
        statement="select username from current_user where user="+"'"+"1"+"'"
        cursor.execute(statement)
        self.conn.commit()
        row=cursor.fetchall()
        row=str(row)
        row=row[3:8]
        return row

    def start(self):
        calendar = calendar_mod.MyForm(self)
        calendar.exec_()
        date = calendar.getdate()
        print(date)
        self.ui.de_start.setDisplayFormat('MMM d yyyy')
        self.ui.de_start.setDate(date)

    def end(self):
        calendar = calendar_mod.MyForm(self)
        calendar.exec_()
        date = calendar.getdate()
        print(date)
        self.ui.de_end.setDisplayFormat('MMM d yyyy')
        self.ui.de_end.setDate(date)

    def display(self):
        cursor=self.conn.cursor()
        self.ui.lw_activity.clear()
        self.ui.lw_activity.addItem("activity_id\tactivity_name\tactivity_type")
        self.activity=self.getuser()+"_activities"
        cursor.execute("select activity_id,activity_name,activity_type from "+self.activity+" order by activity_id asc")
        self.conn.commit()
        row=cursor.fetchall()
        print(row)
        for r in row:
            ac_id,ac_name,ac_type = r
            self.entry=str(ac_id)+"\t"+str(ac_name)+"\t"+str(ac_type)
            self.ui.lw_activity.addItem(self.entry)
           
    def process(self):
        name=self.ui.lne_task.text()
        self.item = self.ui.lw_activity.item(self.ui.lw_activity.currentRow()).text()
        self.item=str(self.item)
        ans=self.item
        end=ans.find("\t",2,len(ans))
        self.activity=str(self.item[2:end])
        self.type=str(self.item[end+1:])
        print(self.type)
        print(self.activity)
        assignedby=str(self.ui.lne_assignedby.text())
        duration=str(self.ui.lne_duration.text())
        priority=str(self.ui.lne_priority.text())
        start=self.ui.de_start.date()
        start=self.convertdate(start)
        end=self.ui.de_end.date()
        end=self.convertdate(end)
        print(start)
        print(end)
        datepriority=self.deadlinePriority(end)
        totalpriority=round(self.totalPriority(datepriority,int(priority)),0)
        
        ans=self.is_number(duration)
        if ans==True and priority.isdigit()==True:
            if int(priority)>=0 and int(priority)<=5:
                cursor=self.conn.cursor()
                self.tasks=self.getuser()+"_tasks"
                statement="insert into "+self.tasks+" (task_name,task_activity,task_type,assigned_by,duration,start_date,end_date,user_priority,date_priority,total_priority,status) VALUES ("+'"'+name+'","'+self.activity+'","'+self.type+'","'+assignedby+'",'+str(duration)+',"'+start+'","'+end+'",'+str(priority)+","+str(datepriority)+","+str(totalpriority)+",'pending')"
                print(statement)
                cursor.execute(statement)
                self.conn.commit()
                self.close()

        else:
            QtGui.QMessageBox.critical(self,"Critical Error", "Wrong data type entered in duration or priority. Please try again.")

    def is_number(self,num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def deadlinePriority(self,deadline):#inputs a string
              newtoday=datetime.datetime.now()
              print(newtoday)
              todayyear=newtoday.year
              todaymonth=newtoday.month
              todayday=newtoday.day
              today=datetime.date(todayyear,todaymonth,todayday)
              datePriority = 0
              dMonth = int(deadline[3]+deadline[4])
              dYear = int(deadline[6]+deadline[7]+deadline[8]+deadline[9])
              dDay= int(deadline[0]+deadline[1])
              d=datetime.date(dYear,dMonth,dDay)
              print(d)
              print(today)
              dif=(d-today).days
              dif=int(dif)
              print(dif)
              d2= today.day
              dm = today.month
              dy = today.year
              if dif<=1:
                  datePriority= 5
              elif dif<=3:
                  datePriority= 4
              elif dif<=7:
                  datePriority= 3
              elif dif<=14:
                  datePriority= 2
              else:
                  datePriority= 1
              return (datePriority)
  
    def totalPriority(self,deadlinePriority, userPriority): #both are from 1-5
        return (deadlinePriority*40/3+userPriority*20/3)


    def convertdate(self,date):
        selecteddate=str(date)
        if selecteddate[29]==')':
            selecteddate=selecteddate[19:29]
        else:
            selecteddate=selecteddate[19:30]
        print("\t\t\t"+selecteddate)
        dateselect=selecteddate.split(", ")
        day=dateselect[2]
        month=dateselect[1]
        year=dateselect[0]
        newday=""
        for j in day:
                if j=='[' or j=="'" or j=='(':
                    pass
                else:
                   newday=newday+j
        newyear=""
        for k in year:
            if k==']' or k=="'" or k==')':
                pass
            else:
               newyear=newyear+k
                   
        if len(newday)==1:
                    newday="0"+str(newday)
                    
        if len(month)==1:
            month="0"+str(month)
        dateoftask=newday+"/"+month+"/"+year
        return dateoftask

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    
