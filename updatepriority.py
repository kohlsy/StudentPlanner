import sys, datetime
from PyQt4 import QtCore, QtGui, uic, QtSql
import sqlite3
class Priority:
    def __init__(self):
        print("hi")
        self.taskstable=""
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect("studentplanner.db")
        self.updatepriority()

    def updatepriority(self):
        cursor=self.conn.cursor()
        statement="select username from users"
        cursor.execute(statement)
        self.conn.commit()
        row=cursor.fetchall()
        print(row)
        for i in row:
            self.taskstable=""
            i=str(i)
            name=i[2:len(i)-3]
            print(name)
            self.taskstable=name+"_tasks"
            cursor.execute("select user_priority,end_date from "+self.taskstable)
            self.conn.commit()
            date=cursor.fetchall()
            taskid=1
            print(self.taskstable)
            if date!=[]:
                for j in date:
                    j=str(j)
                    print(j)
                    userpriority=int(j[1])
                    print(userpriority)
                    enddate=j[5:len(j)-2]
                    print(enddate)
                    datepriority=int(self.deadlinePriority(enddate))
                    totalpriority=round(self.totalPriority(datepriority,userpriority),0)
                    print(datepriority)
                    print(totalpriority)
                    update="update "+self.taskstable+" set date_priority="+str(datepriority)+" , total_priority="+str(totalpriority)+" where  task_id="+str(taskid)
                    print("\t\t\t"+update)
                    cursor.execute(update)
                    self.conn.commit()
                    taskid=taskid+1

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
              if dif<0:
                  datePriority=0
              elif dif<=1:
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
