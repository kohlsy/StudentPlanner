import sys,datetime
from PyQt4 import QtCore, QtGui, uic
import sqlite3
import timeslot_mod
from schedule_auto import *
class MyForm(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btn_add.clicked.connect(self.add)
        self.ui.btn_process.clicked.connect(self.process)
        self.st=[]
        self.et=[]
        self.dif=[]
        dbfile="studentplanner.db"
        self.conn=sqlite3.connect("studentplanner.db")

    def getuser(self):
        cursor=self.conn.cursor()
        statement="select username from current_user where user="+"'"+"1"+"'"
        cursor.execute(statement)
        self.conn.commit()
        row=cursor.fetchall()
        row=str(row)
        row=row[3:8]
        return row

    def add(self):
        timeperiod = timeslot_mod.MyForm(self)
        timeperiod.exec()
        timeslot=timeperiod.slot()
        ans=self.timedif(timeslot)
        self.st.append(ans[0])
        self.et.append(ans[1])
        self.dif.append(ans[2])
        print(ans[0])
        print(ans[1])
        self.ui.lw_free.addItem(timeslot)

    def process(self):
        self.ids=[]
        self.tasks=[]
        self.duration=[]
        self.priority=[]
        cursor=self.conn.cursor()
        tablename=self.getuser()+"_tasks"
        cursor.execute("select task_id from " +tablename+" order by total_priority asc")
        self.conn.commit()
        ids=cursor.fetchall()
        ids=str(ids)
        for i in ids:
            if i[0].isdigit()==True:
                num=i[0]
               # print(num)
                self.ids.append(num)
                
        print(self.ids)

        cursor=self.conn.cursor()
        cursor.execute("select task_name from " +tablename+" order by total_priority desc")
        self.conn.commit()
        tasks=cursor.fetchall()
        for j in tasks:
                num=str(j)
              #  print(num)
                num=num[2:len(num)-3]
                #print(num)
                self.tasks.append(num)
        print(self.tasks)
        
        cursor=self.conn.cursor()
        cursor.execute("select duration from " +tablename+" order by total_priority asc")
        self.conn.commit()
        duration=cursor.fetchall()
        for k in duration:
            k=str(k)
            k=k[1:len(k)-2]
            k=float(k)
            k=k*60
            self.duration.append(k)
        print(self.duration)

        cursor=self.conn.cursor()
        cursor.execute("select total_priority from " +tablename+" order by total_priority asc")
        self.conn.commit()
        priority=cursor.fetchall()
        for l in priority:
            l=str(l)
            l=l[1:len(l)-2]
            l=int(l)
            self.priority.append(l)
        print(self.priority)
        
        self.createSchedule(self.dif,self.st,self.et,self.ids,self.tasks,self.duration,self.priority)

    def createSchedule(self,timeDif, timeSlotStarts, timeSlotEnds, taskId, tasks, duration, priority):# timeDif in minutes
        slotStart=""
        print("\n\n\n\n\n\n\n")
        print(duration)
        print("\n\n\n\n\n")
        timeDifTotal = 0
        print(timeSlotStarts)
        for i in timeDif:
            timeDifTotal = timeDifTotal+i
        
        freeTime = timeDif
##        ## These arrays will contain content from the database
##        taskId = [1,2,3,4,5] # sorted by priority
##        tasks = ["math","physics","spanish","chemistry","english"] # sorted by priority
##        duration = [30,70,32,64,163] # sorted by priority(in minutes)
##        priority = [5,4,3,3,2] # sorted by priority
        j=0
        time = duration[j]
        currentDate = datetime.datetime.now()
        g=0
        done=False
        for i in range(0,len(timeDif)):
            timeDif = freeTime[i]
            if priority[j] == 5 and time>timeDifTotal:
                print("Enter more time")
                break
            elif time<timeDif:            
                print("\t\t\t\t\t"+slotStart)
                timeDif = freeTime[i]
                slotStart = timeSlotStarts[i]
                slotEnd = ""
            while(time<timeDif):
                timeDif = timeDif-time
                startHr = str(slotStart[0])+str(slotStart[1])
                startMin = str(slotStart[3])+str(slotStart[4])
                h = str(int(time//60))
                m = str(int(time%60))
                minutes = str(int(startMin)+int(m))
                hours = str(int(startHr)+int(h))
                totalHrs = hours
                hours = str(int(hours)%24)
                if int(hours)>=6 and totalHrs>hours:
                    print("Please enter time slots before 6:00 on the next day")
                    g=1
                    break
                if int(minutes)>=60:
                    hours = str(int(hours)+1)
                    minutes = str(int(minutes)%60)
                if minutes == "0":
                    minutes = "00"
                if len(hours)==1:
                    hours = "0"+hours
                slotEnd = hours+":"+minutes
                slotTime = slotStart+"-"+slotEnd
                print(slotTime+" - "+tasks[j])
                self.ui.lw_time.addItem(str(slotTime))
                self.ui.lw_task.addItem(str(tasks[j]))
                slotStart = slotEnd
                j = j+1
                if j == len(duration):
                    break
                else:
                    time = duration[j]
            if g==1 or j == len(duration):
                j = j-1
                done = True
                break

            if time==timeDif:
                timeDif=0
                slotTime = slotStart+"-"+timeSlotEnds[i]
                print(slotTime+" - "+tasks[j])
                self.ui.lw_time.addItem(str(slotTime))
                self.ui.lw_task.addItem(str(tasks[j]))
            elif time>timeDif:
                time = time-timeDif
                slotTime = slotStart+"-"+timeSlotEnds[i]
                print(slotTime+" - "+tasks[j])
                self.ui.lw_time.addItem(str(slotTime))
                self.ui.lw_task.addItem(str(tasks[j]))

           # self.ui.lw_task.addItem(str(time)+" minutes left of "+str(tasks[j]+", task Id = "+str(taskId[j])))

        if g==0:
            if done==True:
                print("All tasks have been completed")
                print("You have "+str(timeDif)+"minutes free")
                self.ui.lw_task.addItem("All tasks have been completed")
                self.ui.lw_task.addItem("You have "+str(timeDif)+"minutes free")
                return(-1)
            else:
                print(str(time)+" minutes left of "+str(tasks[j]+", task Id = "+str(taskId[j])))
                self.ui.lw_task.addItem(str(time)+" minutes left of "+str(tasks[j]+", task Id = "+str(taskId[j])))
                return (time,taskId[j])
    
    def timedif(self,x):
        print("Working..."+str(x))
        x=str(x)
        timedifh=0
        timedifm=0
        firsthr=0
        firstmts=0
        lasthr=0
        lastmts=0
        counter=0
        if x[0].isdigit()==True and x[1].isdigit()==True and x[3].isdigit()==True and x[4].isdigit()==True and x[10].isdigit()==True and x[9].isdigit()==True and x[7].isdigit()==True and x[6].isdigit()==True and x[2]==":" and x[8]==":" and x[5]=="-":
            print("fine")
        else:
            print("error")       
                
        for i in x:
            if i=="-":
                firsthr=x[counter-5]+x[counter-4]
                firstmts=x[counter-2]+x[counter-1]
                lasthr=x[counter+1]+x[counter+2]
                lastmts=x[counter+4]+x[counter+5]
                
            counter=counter+1
                
        print(str(firsthr)+":"+str(firstmts)+"-"+str(lasthr)+":"+str(lastmts))

        if firstmts>lastmts:
            timedifh=int(lasthr)-int(firsthr)-1
            timedifm=60-(int(firstmts)-int(lastmts))
            print(str(timedifh)+"working")
        if firstmts<=lastmts:
            timedifh=int(lasthr)-int(firsthr)
            timedifm=int(lastmts)-int(firstmts)
            print(str(timedifh)+"working")

        starttime=str(firsthr)+":"+str(firstmts)
        endtime=str(lasthr)+":"+str(lastmts)
        ans=timedifh*60+timedifm
        return starttime,endtime,ans

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=MyForm()
    myapp.show()
    sys.exit(app.exec_())
    

