from datetime import date
import sqlite3
import tkinter
from tkinter import messagebox
from easygui import *
from tkinter import *
from turtle import *
import random
from tkinter import ttk
import string
import tkinter.messagebox as tk
import re

conn = sqlite3.connect('leaveDb.db')
cur = conn.cursor()

conn.execute("CREATE TABLE IF NOT EXISTS balance (employee_id text,sickleave int,maternityleave int,emergencyleave int)")
conn.execute("CREATE TABLE IF NOT EXISTS STATUS (leave_id int,employee_id text,leave text, cur_date text, Date1 text,Date2 text,days int,status text, hrstatus text)")
conn.execute("CREATE TABLE IF NOT EXISTS employee (register_id text, employee_id text, Name text, ContactNumber text, employee_mail text, employee_blood_group text, employee_address text, Password text)")


class AdminClass:
    
    def AdminLogin(self):

        message = "Enter Username and Password"
        title = "Deen Login"
        fieldnames = ["Username", "Password"]
        field = []
        field = multpasswordbox(message, title, fieldnames)
        if field[0] == 'admin' and field[1] == 'admin':
            messagebox.showinfo("Admin Login", "Login Successful")
            self.adminwindow()
        else:
            messagebox.showerror("Error info", "Incorrect username or password")



    def adminwindow(self):

        adminmainwindow = Toplevel()
        adminmainwindow.wm_attributes('-fullscreen', '1')
        
        informationEmployee = Button(adminmainwindow, text = 'All Employee information', command = self.EmployeeAllInformationWindow, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        informationEmployee.pack(fill=X)

        LeaveListButton = Button(adminmainwindow, text = 'Leave approval list', command = self.leavelist, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        LeaveListButton.pack(fill=X)

        ApprovalButton = Button(adminmainwindow, text = 'Approve leave', command = self.LeaveApproval, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        ApprovalButton.pack(fill=X)

        LogoutBtn = Button(adminmainwindow, text = 'Logout', command = adminmainwindow.destroy, bd=12, relief=GROOVE, fg="red",bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        LogoutBtn.pack(fill=X) 
    
    
    
    def EmployeeAllInformationWindow(self):

        allEmployeeInformation = Toplevel()
        # allEmployeeInformation.geometry('1230x290')
        allEmployeeInformation.resizable(0, 0)

        appLabel = Label(allEmployeeInformation, text="All Employee Information", fg="#06a099", width=40)
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()
        
        tree = ttk.Treeview(allEmployeeInformation)
        tree.pack(side = 'left')
        
        verscrlbar = ttk.Scrollbar(allEmployeeInformation, command = tree.yview)  
        verscrlbar.pack(side ='left', fill = "y") 
    
        tree.configure(yscrollcommand = verscrlbar.set) 

        tree["columns"] = ('one', 'two', 'three', 'four', 'five', 'six')
        tree['show'] = 'headings'

        tree.column("one", anchor = 'c', minwidth = 0, width = 150)
        tree.column("two", anchor = 'c', minwidth = 0, width = 150)
        tree.column("three", anchor = 'c', minwidth = 0, width = 150)
        tree.column("four", anchor = 'c', minwidth = 0, width = 200)
        tree.column("five", anchor = 'c', minwidth = 0, width = 150)
        tree.column("six", anchor = 'c', minwidth = 0, width = 400)

        tree.heading("one", text = "Employee ID")
        tree.heading("two", text = "Name")
        tree.heading("three", text = "Contact Number")
        tree.heading("four", text = "Employee Mail")
        tree.heading("five", text = "Blood Group")
        tree.heading("six", text = "Address")
        
        cursor = conn.execute('SELECT employee_id, Name, ContactNumber, employee_mail, employee_blood_group, employee_address FROM employee')
        i = 1

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5]))
            i = i + 1

    
    
    def leavelist(self):

        global leavelistwindow
        leavelistwindow = Toplevel()
        leavelistwindow.resizable(0, 0)

        appLabel = Label(leavelistwindow, text="Leave Approval List", fg="#06a099", width=40)
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()

        date_button = Button(leavelistwindow, text = "Choose Date", command = self.date_record)
        date_button.place(x = 1100, y = 20)

        tree = ttk.Treeview(leavelistwindow)
        tree.pack(side = 'left')
        
        verscrlbar = ttk.Scrollbar(leavelistwindow, command = tree.yview)  
        verscrlbar.pack(side ='left', fill = "y") 
    
        tree.configure(yscrollcommand = verscrlbar.set)
        tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight")
        tree.column('one', anchor = 'c', minwidth=0, width=180)
        tree.column('two', anchor = 'c', minwidth=0, width=180)
        tree.column('three', anchor = 'c', minwidth=0, width=180)
        tree.column('four', anchor = 'c', minwidth=0, width=180)
        tree.column('five', anchor = 'c', minwidth=0, width=180)
        tree.column('six', anchor = 'c', minwidth=0, width=180)
        tree.column('seven', anchor = 'c', minwidth=0, width=180)
        tree.column('eight', anchor = 'c', minwidth=0, width=180)

        tree['show'] = 'headings'


        tree.heading("one", text="Leave ID")
        tree.heading("two", text="Employee ID")
        tree.heading("three", text="Leave Type")
        tree.heading("four", text="Date")
        tree.heading("five", text="From Date")
        tree.heading("six", text="To Date")
        tree.heading("seven", text="Total Number Of Days")
        tree.heading("eight", text = "Status")

        cursor = conn.execute('SELECT * FROM status')

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


    def date_record(self):

        message = "Enter Date"
        title = "Date Record"
        fieldnames = ["Enter Date"]
        field = []
        field = multenterbox(message, title, fieldnames)
        leavelistwindow.destroy()

        global datewindow
        datewindow = Toplevel()
        datewindow.title("Date Record")
        
        appLabel = Label(datewindow, text="Leave Approval List", fg="#06a099", width=40)
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()

        tree = ttk.Treeview(datewindow)
        tree.pack(side = 'left')
        
        verscrlbar = ttk.Scrollbar(datewindow, command = tree.yview)  
        verscrlbar.pack(side ='left', fill = "y") 
    
        tree.configure(yscrollcommand = verscrlbar.set)

        tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight")
        tree.column('one', anchor = 'c', minwidth=0, width=180)
        tree.column('two', anchor = 'c', minwidth=0, width=180)
        tree.column('three', anchor = 'c', minwidth=0, width=180)
        tree.column('four', anchor = 'c', minwidth=0, width=180)
        tree.column('five', anchor = 'c', minwidth=0, width=180)
        tree.column('six', anchor = 'c', minwidth=0, width=180)
        tree.column('seven', anchor = 'c', minwidth=0, width=180)
        tree.column('eight', anchor = 'c', minwidth=0, width=180)

        tree['show'] = 'headings'
        
        tree.heading("one", text="Leave ID")
        tree.heading("two", text="Employee ID")
        tree.heading("three", text="Leave Type")
        tree.heading("four", text="Date")
        tree.heading("five", text="From Date")
        tree.heading("six", text="To Date")
        tree.heading("seven", text="Total Number Of Days")
        tree.heading("eight", text = "Status")

        cursor = conn.execute('SELECT * FROM status WHERE cur_date = ?', [field[0]])

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))




    def LeaveApproval(self):

        message = "Enter leave_id"
        title = "leave approval"
        fieldNames = ["Leave_id"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)
        message1 = "Approve/Deny"
        title1 = "leave approval"
        choices = ["approve", "deny"]
        choice = choicebox(message1, title1, choices)

        if choice == 'approve':
            conn.execute("UPDATE STATUS SET status = ? WHERE leave_id= ?", ('Approved', fieldValues[0]))
            conn.execute("UPDATE STATUS SET hrstatus = ? WHERE leave_id= ?", ('Pending', fieldValues[0]))
        else:
            conn.execute("UPDATE STATUS SET status = ? WHERE leave_id= ?", ('Denied', fieldValues[0]))
            conn.execute("UPDATE STATUS SET hrstatus = ? WHERE leave_id= ?", ('Denied', fieldValues[0]))

        conn.commit()



class HRClass(AdminClass):

    def HRLogin(self):
        message = "Enter Username and Password"
        title = "HR Login"
        fieldnames = ["Username", "Password"]
        field = []
        field = multpasswordbox(message, title, fieldnames)
        if field[0] == 'HRpwd' and field[1] == 'HRpwd':
            messagebox.showinfo("HR Login", "Login Successfully")
            self.adminwindow()
        else:
            messagebox.showerror("Error info", "Incorrect username or password")

    

    def leavelist(self):

        global leavelistwindow
        leavelistwindow = Toplevel()
        leavelistwindow.resizable(0, 0)

        appLabel = Label(leavelistwindow, text="Leave Approval List", fg="#06a099", width=40)
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()

        date_button = Button(leavelistwindow, text = "Choose Date", command = self.date_record)
        date_button.place(x = 1100, y = 20)

        tree = ttk.Treeview(leavelistwindow)
        tree.pack(side = 'left')
        
        verscrlbar = ttk.Scrollbar(leavelistwindow, command = tree.yview)  
        verscrlbar.pack(side ='left', fill = "y") 
    
        tree.configure(yscrollcommand = verscrlbar.set)
        tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight")
        tree.column('one', anchor = 'c', minwidth=0, width=180)
        tree.column('two', anchor = 'c', minwidth=0, width=180)
        tree.column('three', anchor = 'c', minwidth=0, width=180)
        tree.column('four', anchor = 'c', minwidth=0, width=180)
        tree.column('five', anchor = 'c', minwidth=0, width=180)
        tree.column('six', anchor = 'c', minwidth=0, width=180)
        tree.column('seven', anchor = 'c', minwidth=0, width=180)
        tree.column('eight', anchor = 'c', minwidth=0, width=180)

        tree['show'] = 'headings'


        tree.heading("one", text="Leave ID")
        tree.heading("two", text="Employee ID")
        tree.heading("three", text="Leave Type")
        tree.heading("four", text="Date")
        tree.heading("five", text="From Date")
        tree.heading("six", text="To Date")
        tree.heading("seven", text="Total Number Of Days")
        tree.heading("eight", text = "Status")

        

        cursor = conn.execute('SELECT * FROM status')

        for row in cursor:
            if row[7] == 'Approved' and row[8] == 'Pending':
                tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8]))
    


    def LeaveApproval(self):

        message = "Enter leave_id"
        title = "leave approval"
        fieldNames = ["Leave_id"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)
        message1 = "Approve/Deny"
        title1 = "leave approval"
        choices = ["approve", "deny"]
        choice = choicebox(message1, title1, choices)

        if choice == 'approve':
            conn.execute("UPDATE STATUS SET hrstatus = ? WHERE leave_id= ?", ('Approved', fieldValues[0]))
        else:
            conn.execute("UPDATE STATUS SET hrstatus = ? WHERE leave_id= ?", ('Denied', fieldValues[0]))

        conn.commit()

        if choice == 'approve':
            cur.execute("SELECT leave FROM STATUS WHERE leave_id=?", (fieldValues[0],))
            row = cur.fetchall()
            col = row

            for row in conn.execute("SELECT employee_id FROM STATUS WHERE leave_id=?", (fieldValues[0],)):
                exampleId = row[0]

            for row in conn.execute("SELECT days FROM STATUS WHERE leave_id=?", (fieldValues[0],)):
                exampleDays = row[0]

            for row in conn.execute("SELECT sickleave from balance where employee_id=?", (exampleId,)):
                balance1 = row[0]

            for row in conn.execute("SELECT maternityleave from balance where employee_id=?", (exampleId,)):
                balance2 = row[0]

            for row in conn.execute("SELECT emergencyleave from balance where employee_id=?", (exampleId,)):
                balance3 = row[0]

            if (col[0] == ('Sick Leave',)):
                conn.execute("UPDATE balance SET sickleave =? WHERE employee_id= ?", ((balance1 - exampleDays), (exampleId)))

            if (col[0] == ('Maternity Leave',)):
                conn.execute("UPDATE balance SET maternityleave =? WHERE employee_id= ?", ((balance2 - exampleDays), (exampleId)))

            if (col[0] == ('Emergency Leave',)):
                conn.execute("UPDATE balance SET emergencyleave =? WHERE employee_id= ?", ((balance3 - exampleDays), (exampleId)))
        conn.commit()



class EmployeeClass:
    
    def EmployeeLogin(self):

        f=0
        message = "Enter Employee ID and Password"
        title = "Employee Login"
        fieldnames = ["Employee ID", "Password"]
        field = []
        field = multpasswordbox(message, title, fieldnames)

        for row in conn.execute('SELECT * FROM employee'):
            if field[0] == row[1] and field[1] == row[7]:
                global login
                login = field[0]
                f = 1
                messagebox.showinfo("Employee Login", "Login Successful")
                root.destroy()
                self.EmployeeLoginWindow()
                break
        if f != 1:
            messagebox.showerror("Error info", "Incorrect employee id or password")



    def EmployeeLoginWindow(self):

        # employee login window after successful login
        global LoginWindow
        LoginWindow = Tk()
        LoginWindow.title("Leave Management")
        LoginWindow.wm_attributes('-fullscreen', '1')

        informationEmployee = Button(LoginWindow, text = 'Employee information', command = self.EmployeeInformationWindow, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        informationEmployee.pack(fill=X)

        submit = Button(LoginWindow, text = 'Submit Leave', command = self.apply, bd=12, relief = GROOVE, fg = "black", bg = "yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        submit.pack(fill=X)

        LeaveBalance = Button(LoginWindow, text= 'Leave Balance', command = self.balance, bd = 12, relief = GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        LeaveBalance.pack(fill=X)

        LeaveApplicationStatus = Button(LoginWindow, text= 'Last leave status', command = self.EmployeeLeaveStatus, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        LeaveApplicationStatus.pack(fill=X)

        AllLeaveStatus = Button(LoginWindow, text='All leave status', command = self.EmployeeAllStatus, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        AllLeaveStatus.pack(fill=X)

        LogoutBtn = Button(LoginWindow, text = 'Logout', command = self.Employeelogout, bd=12, relief=GROOVE, fg="red", bg="yellow", font=("Calibri", 36, "bold"), activebackground = "yellow")
        LogoutBtn.pack(fill=X)

        LoginWindow.mainloop()

    
    def EmployeeInformationWindow(self):

        employeeInformation = Toplevel()
        employeeInformation.resizable(0, 0)

        tree = ttk.Treeview(employeeInformation)
        
        tree["columns"] = ('one', 'two', 'three', 'four', 'five', 'six')
        
        tree.column("one", anchor = 'c', minwidth = 0, width = 150)
        tree.column("two", anchor = 'c', minwidth = 0, width = 150)
        tree.column("three", anchor = 'c', minwidth = 0, width = 150)
        tree.column("four", anchor = 'c', minwidth = 0, width = 200)
        tree.column("five", anchor = 'c', minwidth = 0, width = 150)
        tree.column("six", anchor = 'c', minwidth = 0, width = 400)
        
        tree['show'] = 'headings'
        tree.heading("one", text = "Employee ID")
        tree.heading("two", text = "Name")
        tree.heading("three", text = "Contact Number")
        tree.heading("four", text = "Employee Mail")
        tree.heading("five", text = "Blood Group")
        tree.heading("six", text = "Address")
        
        cursor = conn.execute('SELECT employee_id, Name, ContactNumber, employee_mail, employee_blood_group, employee_address FROM employee where employee_id=?', [login])
        i = 1

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5]))
            i = i + 1
        tree.pack() 



    def apply(self):

        global employee_id
        message = "Enter the following details "
        title = "Leave Apply"
        fieldNames = ["From", "To", "days"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)
        temp = re.findall(r'\d+', fieldValues[0]) 
        res = list(map(int, temp)) 

        temp1 = re.findall(r'\d+', fieldValues[1]) 
        res1 = list(map(int, temp1))

        date1 = date(res[2], res[1], res[0])
        date2 = date(res1[2], res1[1], res1[0])
        date3 =  (date2-date1).days+1

        if str(date3) == fieldValues[2]:

            message1 = "Select type of leave"
            title1 = "Type of leave"
            choices = ["Sick Leave", "Maternity Leave", "Emergency Leave"]
            choice = choicebox(message1, title1, choices)
            leaveid = random.randint(1000, 10000)
            
            today = date.today()
            global date_current
            date_current = today.strftime("%d/%m/%Y")

            for row in conn.execute("SELECT sickleave from balance where employee_id=?", [login]):
                balance1 = row[0]
            
            for row in conn.execute("SELECT maternityleave from balance where employee_id=?", [login]):
                balance2 = row[0]

            for row in conn.execute("SELECT emergencyleave from balance where employee_id=?", [login]):
                balance3 = row[0]

            if choice == "Sick Leave":        
                if balance1 >= (int)(fieldValues[2]):
                    conn.execute("INSERT INTO STATUS(leave_id, employee_id, leave, cur_date, Date1, Date2, days, status, hrstatus) VALUES (?,?,?,?,?,?,?,?,?)",(leaveid, login, choice, date_current, fieldValues[0], fieldValues[1], fieldValues[2], "Pending", "Pending"))
                    messagebox.showinfo("Leave", "Leave Applied successfully.....")
                    conn.commit()
                else:
                    tk.showerror("Sick Leave Warning","NO SUFFICIENT BALANCE!!!!!!!!!!!!!!")
            
            if choice == "Maternity Leave":
                if balance2 >= (int)(fieldValues[2]):
                    conn.execute("INSERT INTO STATUS(leave_id, employee_id, leave, cur_date, Date1, Date2, days, status, hrstatus) VALUES (?,?,?,?,?,?,?,?,?)",(leaveid, login, choice, date_current, fieldValues[0], fieldValues[1], fieldValues[2], "Pending", "Pending"))
                    tk.showinfo("Leave", "Leave Applied successfully.....")
                    conn.commit()
                else:
                    tk.showerror("Maternity Leave Warning","NO SUFFICIENT BALANCE!!!!!!!!!!!!!!")
            
            if choice == "Emergency Leave":
                if balance3 >= (int)(fieldValues[2]):
                    conn.execute("INSERT INTO STATUS(leave_id, employee_id, leave, cur_date, Date1, Date2, days, status, hrstatus) VALUES (?,?,?,?,?,?,?,?,?)",(leaveid, login, choice, date_current, fieldValues[0], fieldValues[1], fieldValues[2], "Pending", "Pending"))
                    tk.showinfo("Leave", "Leave Applied successfully.....")
                    conn.commit()
                else:
                    tk.showerror("Emergengy Leave Warning","NO SUFFICIENT BALANCE!!!!!!!!!!!!!!")
        
        else:
            messagebox.showerror("Error", "Total Number of Days Does not Match.....")
    
    
    
    def balance(self):

        global login
        global balanced
        balanced = []
        for i in conn.execute('SELECT * FROM balance WHERE employee_id = ?', [login]):
            balanced = i
        self.WindowBalance()
    


    def WindowBalance(self):

        balanceWindow = Toplevel()
        balanceWindow.resizable(0, 0)
        label_1 = Label(balanceWindow, text = "Employee ID=", fg="black", justify=LEFT, font=("Calibri", 16))
        label_2 = Label(balanceWindow, text = balanced[0], font=("Calibri", 16))
        label_3 = Label(balanceWindow, text ="Sick Leave=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_4 = Label(balanceWindow, text = balanced[1], font=("Calibri", 16))
        label_5 = Label(balanceWindow, text = "Maternity Leave=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_6 = Label(balanceWindow, text = balanced[2], font=("Calibri", 16))
        label_7 = Label(balanceWindow, text = "Emergency Leave=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_8 = Label(balanceWindow, text = balanced[3], font=("Calibri", 16))
        label_1.grid(row=0, column=0)
        label_2.grid(row=0, column=1)
        label_3.grid(row=1, column=0)
        label_4.grid(row=1, column=1)
        label_5.grid(row=2, column=0)
        label_6.grid(row=2, column=1)
        label_7.grid(row=3, column=0)
        label_8.grid(row=3, column=1)


    def EmployeeLeaveStatus(self):

        global leaveStatus 
        leaveStatus = []
        for i in conn.execute('SELECT * FROM STATUS where employee_id=?', [login]):
            leaveStatus = i
        self.WindowStatus()
    


    def WindowStatus(self):
    
        StatusWindow = Toplevel()
        StatusWindow.resizable(0, 0)

        label_1 = Label(StatusWindow, text = "Employee ID=", fg="black", justify=LEFT, font=("Calibri", 16))
        label_2 = Label(StatusWindow, text = leaveStatus[1], font=("Calibri", 16))
        label_3 = Label(StatusWindow, text = "Type=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_4 = Label(StatusWindow, text = leaveStatus[2], font=("Calibri", 16))
        label_5 = Label(StatusWindow, text = "Start=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_6 = Label(StatusWindow, text = leaveStatus[4], font=("Calibri", 16))
        label_7 = Label(StatusWindow, text = "End=", fg="black", font=("Calibri", 16), justify=LEFT)
        label_8 = Label(StatusWindow, text= leaveStatus[5], font=("Calibri", 16))
        label_9 = Label(StatusWindow, text = "Status:", fg="black", font=("Calibri", 16), justify=LEFT)
        label_10 = Label(StatusWindow, text = leaveStatus[8], font=("Calibri", 16))
        label_11 = Label(StatusWindow, text ="Leave ID:", fg="black", font=("Calibri", 16), justify=LEFT)
        label_12 = Label(StatusWindow, text = leaveStatus[0], font=("Calibri", 16))
        label_11.grid(row=0, column=0)
        label_12.grid(row=0, column=1)
        label_1.grid(row=1, column=0)
        label_2.grid(row=1, column=1)
        label_3.grid(row=2, column=0)
        label_4.grid(row=2, column=1)
        label_5.grid(row=3, column=0)
        label_6.grid(row=3, column=1)
        label_7.grid(row=4, column=0)
        label_8.grid(row=4, column=1)
        label_9.grid(row=5, column=0)
        label_10.grid(row=5, column=1)


    def EmployeeAllStatus(self):

        allStatus = Toplevel()
        allStatus.geometry('1379x287')
        allStatus.resizable(0, 0)
        
        appLabel = Label(allStatus, text="All Leave Status", fg="#06a099", width=40)
        appLabel.config(font=("Sylfaen", 30))
        appLabel.pack()
        
        tree = ttk.Treeview(allStatus)
        tree.pack(side = 'left')
        
        verscrlbar = ttk.Scrollbar(allStatus, command = tree.yview)  
        verscrlbar.pack(side ='left', fill = "y") 
    
        tree.configure(yscrollcommand = verscrlbar.set)


        tree["columns"] = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight')

        tree.column("one", anchor = 'c', minwidth = 0, width = 170)
        tree.column("two", anchor = 'c', minwidth = 0, width = 170)
        tree.column("three", anchor = 'c', minwidth = 0, width = 170)
        tree.column("four", anchor = 'c', minwidth = 0, width = 170)
        tree.column("five", anchor = 'c', minwidth = 0, width = 170)
        tree.column("six", anchor = 'c', minwidth = 0, width = 170)
        tree.column("seven", anchor = 'c', minwidth = 0, width = 170)
        tree.column('eight', anchor = 'c', minwidth = 0, width = 170)

        tree['show'] = 'headings'

        tree.heading("one", text="Leave ID")
        tree.heading("two", text="Employee ID")
        tree.heading("three", text="Leave Type")
        tree.heading("four", text="Date")
        tree.heading("five", text="From Date")
        tree.heading("six", text="To Date")
        tree.heading("seven", text="Total Number Of Days")
        tree.heading("eight", text = "Status")

        cursor = conn.execute('SELECT * FROM status WHERE employee_id = ?', [login])

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8]))
        tree.pack()



    def Employeelogout(self):
        LoginWindow.destroy()
        mainwindow()



class update_info_class:

    
    def update_information(self):
        
        f = 0
        message = "Enter Employee ID and Register ID"
        title = "Update Information"
        fieldnames1 = ["Employee ID", "Register ID"]
        field1 = []
        field1 = multpasswordbox(message, title, fieldnames1)
        
        for row in conn.execute("SELECT * FROM employee"):
            if field1[0] == row[1] and field1[1] == row[0]:
                global resid
                resid = field1[1]
                f = 1
                tk.showinfo("Employee Login", "Login Successful")
                root.destroy()
                self.UpdateWindow()
                break
        if f == 0:
            tk.showerror("Error info", "Incorrect employee id or Register ID")

    def UpdateWindow(self):
        
        global UpdateWindow
        UpdateWindow = Tk()
        UpdateWindow.wm_attributes('-fullscreen', '1')

        informationEmployee = Button(UpdateWindow, text = 'Employee information', command = self.Employee_Information_Window, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        informationEmployee.pack(fill=X)

        updatename = Button(UpdateWindow, text = 'Update Name', command= self.update_name, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        updatename.pack(fill=X)

        updatephonenumber = Button(UpdateWindow, text = 'Update Phone Number', command = self.update_Phone_Number, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        updatephonenumber.pack(fill=X)

        changepassword = Button(UpdateWindow, text = 'Change Password', command = self.change_password, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        changepassword.pack(fill=X)
        
        updatemail = Button(UpdateWindow, text = 'Update Mail ID', command = self.update_Emp_mail, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        updatemail.pack(fill=X)

        updateaddress = Button(UpdateWindow, text = 'Update Address', command = self.update_Emp_address, bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), activebackground = "yellow")
        updateaddress.pack(fill=X)

        LogoutBtn = Button(UpdateWindow, text = 'Logout', command = self.Employeelogout, bd=12, relief=GROOVE, fg="red", bg="yellow", font=("Calibri", 36, "bold"), activebackground = "yellow")
        LogoutBtn.pack(fill=X)

        UpdateWindow.mainloop()



    def  Employeelogout(self):
        UpdateWindow.destroy()
        mainwindow()

    
    def Employee_Information_Window(self):
        
        employeeInformation = Toplevel()
        employeeInformation.resizable(0, 0)
        tree = ttk.Treeview(employeeInformation)

        
        tree["columns"] = ('one', 'two', 'three', 'four', 'five', 'six')
        tree.column("one", anchor = 'c', minwidth = 0, width = 150)
        tree.column("two", anchor = 'c', minwidth = 0, width = 150)
        tree.column("three", anchor = 'c', minwidth = 0, width = 150)
        tree.column("four", anchor = 'c', minwidth = 0, width = 200)
        tree.column("five", anchor = 'c', minwidth = 0, width = 150)
        tree.column("six", anchor = 'c', minwidth = 0, width = 400)


        tree['show'] = 'headings'
        tree.heading("one", text = "Employee ID")
        tree.heading("two", text = "Name")
        tree.heading("three", text = "Contact Number")
        tree.heading("four", text = "Mail ID")
        tree.heading("five", text = "Blood Group")
        tree.heading("six", text = "Address")


        cursor = conn.execute('SELECT employee_id, Name, ContactNumber, employee_mail, employee_blood_group, employee_address FROM employee where register_id=?', [resid])
        i = 1

        for row in cursor:
            tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5]))
            i = i + 1
        tree.pack()


    
    def update_name(self):
        
        message = "Enter Employee Name"
        title = "Update Name"
        fieldNames = ["Enter Employee Name"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)

        conn.execute("UPDATE employee SET Name =? WHERE register_id = ?", ((fieldValues[0]), (resid)))
        conn.commit()
        tkinter.messagebox.showinfo("Update Name", "Name Updated Successfully")    



    def update_Phone_Number(self):
        
        message = "Enter Employee Phone Number"
        title = "Update Phone Number"
        fieldNames = ["Enter Employee Phone Number"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)

        conn.execute("UPDATE employee SET ContactNumber =? WHERE register_id = ?", ((fieldValues[0]), (resid)))
        conn.commit()
        tkinter.messagebox.showinfo("Update Phone Number", "Phone Number Updated Successfully")


    def update_Emp_address(self):
        
        message = "Enter Employee Address"
        title = "Update Address"
        fieldNames = ["Enter Employee Address"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)

        conn.execute("UPDATE employee SET employee_address =? WHERE register_id = ?", ((fieldValues[0]), (resid)))
        conn.commit()
        tkinter.messagebox.showinfo("Update Address", "Address Updated Successfully")




    def update_Emp_mail(self):
        
        message = "Enter Employee Mail ID"
        title = "Update Mail ID"
        fieldNames = ["Enter Mail ID"]
        fieldValues = []
        fieldValues = multenterbox(message, title, fieldNames)

        conn.execute("UPDATE employee SET employee_mail =? WHERE register_id = ?", ((fieldValues[0]), (resid)))
        conn.commit()


    def change_password(self):
        
        message = "Enter Password"
        title = "Change Password"
        fieldNames = ["New Password","Confirm Password"]
        fieldValues = []
        fieldValues = multpasswordbox(message, title, fieldNames)

        if fieldValues[0] == fieldValues[1]:
            conn.execute("UPDATE employee SET Password =? WHERE register_id = ?", ((fieldValues[1]), (resid)))
            conn.commit()
            tkinter.messagebox.showinfo("Change Password", "Password Updated Successfully")
        else:
            tk.showerror("Warning", "Password Does not Match")


class RegistrationClass:

        def registration(self):
            flag = 0
            message = "Enter Details of Employee"
            title = "Registration"
            fieldNames = ["Name", "Contact Number", "Mail ID", "Blood Group","Address", "Password"]
            fieldValues = []
            fieldValues = multpasswordbox(message, title, fieldNames)
            while 1:
                if fieldValues == None:
                    break
                errmsg = ""
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

                if errmsg == "": break

                fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

            registerid = random.randint(10000,100000)
                
            sample_str = ''.join((random.choice(string.ascii_letters) for i in range(2)))
            sample_str += ''.join((random.choice(string.digits) for i in range(4)))

            sample_list = list(sample_str)
            random.shuffle(sample_list)
            
            global employee_id
            employee_id = ''.join(sample_list)

            conn.execute("INSERT INTO employee (register_id, employee_id, Name, ContactNumber, employee_mail, employee_blood_group, employee_address, Password) VALUES (?,?,?,?,?,?,?,?)",(registerid, employee_id, fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4], fieldValues[5]))
            conn.execute("INSERT INTO balance (employee_id, sickleave, maternityleave, emergencyleave) VALUES (?,?,?,?)", (employee_id, 12, 12, 50))
            emp_info = "Your EMPLOYEE ID IS ", employee_id, "You have been given a Register ID Number which is very confidential \n Your Register ID Number is ", registerid
            messagebox.showinfo("Employee Regestration", "Employee Registered Successfully....")
            messagebox.showinfo("Employee Registration", emp_info)
            conn.commit()

def mainwindow():

    global root

    root = Tk()
    root.wm_attributes('-fullscreen', '1')
    root.title("Leave Management System")
    # C:\Users\ABHISHEK\Documents\Leave-Management-System\OOPS-project
    root.iconbitmap(default='leavelogo.ico')

    obj1 = AdminClass()
    obj2 = EmployeeClass()
    obj3 = update_info_class()
    obj4 = RegistrationClass()
    obj5 = HRClass()

    MainLabel = Label(root, text="Employee Leave Management System", bd=12, relief=GROOVE, fg="Black", bg="Yellow",font=("Calibri", 72, "bold"))
    MainLabel.pack(fill=X)

    AdminLgnBtn = Button(root, text='HR login',  bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), command=obj5.HRLogin, activebackground = "yellow")
    AdminLgnBtn.pack(fill=X)

    AdminLgnBtn = Button(root, text='Dean login',  bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), command=obj1.AdminLogin, activebackground = "yellow")
    AdminLgnBtn.pack(fill=X)

    # HRLgnBtn = Button(root, text='HR login',  bd=12, relief=GROOVE, fg="black", bg="yellow",font=("Calibri", 36, "bold"), command = HRLogin, activebackground = "yellow")
    # HRLgnBtn.pack(fill=X)

    EmployeeRegistration = Button(root, text='Employee registration', command = obj4.registration, bd=12, relief=GROOVE, fg="black", bg="yellow", font=("Calibri", 36, "bold"), activebackground = "yellow")
    EmployeeRegistration.pack(fill=X)

    LoginBtn = Button(root, text='Employee login', bd=12, relief=GROOVE, fg="black", bg="yellow", font=("Calibri", 36, "bold"), command=obj2.EmployeeLogin, activebackground = "yellow")
    LoginBtn.pack(fill = X)

    updatebutton = Button(root, text = "Update Information", bd = 12, relief=GROOVE, fg="black", bg="yellow", font=("Calibri", 36, "bold"), command = obj3.update_information, activebackground = "yellow")
    updatebutton.pack(fill = X)

    ExitBtn = Button(root, text='Exit', command=root.destroy, bd=12, relief=GROOVE, fg="red", bg="yellow", font=("Calibri", 40, "bold"), activebackground = "yellow")
    ExitBtn.pack(fill=X)

    root.mainloop()



if __name__ == "__main__":
    mainwindow()