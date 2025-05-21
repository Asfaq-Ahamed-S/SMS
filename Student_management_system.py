from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk,filedialog
import os
import csv
import sqlite3
import io
import customtkinter as ctk
from datetime import datetime,date

dept_set = set()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

font_MTASC = ("Algerian",30,"bold")

lcn = sqlite3.connect('student_management.db')
lc = lcn.cursor()
lc.execute('''CREATE TABLE IF NOT EXISTS login(id INTEGER PRIMARY KEY,name TEXT NOT NULL,Gender TEXT NOT NULL,Mobile INTEGER NOT NULL,uname TEXT UNIQUE,password TEXT NOT NULL,role TEXT NOT NULL)''')
lcn.commit()

conn = sqlite3.connect('student_management.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY,regno TEXT UNIQUE,name TEXT NOT NULL,dept TEXT NOT NULL,Gender TEXT NOT NULL,marksheet_sem1 TEXT,marksheet_sem2 TEXT,marksheet_sem3 TEXT,marksheet_sem4 TEXT,marksheet_sem5 TEXT,marksheet_sem6 TEXT,UMISnumber TEXT NOT NULL,Aadhar INTEGER NOT NULL,Contact INTEGER NOT NULL,Email TEXT NOT NULL,PRESENTDAYS INTEGER)''')
conn.commit()

dcn = sqlite3.connect('student_management.db')
dc = dcn.cursor()
dc.execute('''CREATE TABLE IF NOT EXISTS dept(id INTEGER PRIMARY KEY,name Text)''')
dcn.commit()

fcn = sqlite3.connect('student_management.db')
fc = fcn.cursor()
fc.execute(''' CREATE TABLE IF NOT EXISTS CollegeFee (id INTEGER PRIMARY KEY,regno TEXT UNIQUE,dept TEXT NOT NULL,sem INTEGER,paid INTEGER DEFAULT 0,balance INTEGER,Total INTEGER,date TEXT)''')
fc.execute(''' CREATE TABLE IF NOT EXISTS BusFee (id INTEGER PRIMARY KEY,regno TEXT UNIQUE,dept TEXT NOT NULL,sem INTEGER,paid INTEGER DEFAULT 0,balance INTEGER,Total INTEGER,date TEXT)''')
fcn.commit()

acn = sqlite3.connect('student_management.db')
ac = acn.cursor()
ac.execute('''CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY,regno TEXT,date TEXT,days_present INTEGER,days_absent INTEGER,percentage INTEGER)''')
acn.commit()

base_path = os.getcwd()

csv_path = base_path + "\CSV"
try:
    os.mkdir(csv_path)
    
except FileExistsError:
    pass

dir_path_image = base_path + "\IMG"
try:
    os.mkdir(dir_path_image)
except FileExistsError:
    pass

font_underlined = ("Arial",12,"underline")

class DASHBOARD:

    def __init__(self):

        self.Dashboard = Tk()
        self.Dashboard.geometry("900x700")
        self.Dashboard.title("Dashboard")
        self.Dashboard.configure(bg="pink")
        self.Dashboard.resizable(height=False,width=False)

        menubar=Menu(self.Dashboard)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="LOG OUT",command=self.logout)
        menubar.add_cascade(label="Options",menu=filemenu)
        self.Dashboard.config(menu=menubar)

        button=ctk.CTkButton(master=self.Dashboard,text='Student',width=25,height=50,corner_radius=20,command=self.student_window)
        button.place(x=200,y=200)

        button=ctk.CTkButton(master=self.Dashboard,text='College Fee',width=25,height=50,corner_radius=20,command=self.CollegeFee)
        button.place(x=400,y=200)

        button=ctk.CTkButton(master=self.Dashboard,text='Bus Fee',width=25,height=50,corner_radius=20,command=self.BusFee)
        button.place(x=600,y=200)

        button=ctk.CTkButton(master=self.Dashboard,text='New\nDepartment',width=25,height=50,corner_radius=20,command=self.add_dept)
        button.place(x=200,y=400)

        button=ctk.CTkButton(master=self.Dashboard,text='Remove\nDepartment',width=25,height=50,corner_radius=20,command=self.rmv_dept)
        button.place(x=400,y=400)

        button=ctk.CTkButton(master=self.Dashboard,text='Marksheet',width=25,height=50,corner_radius=20,command=self.marksheet)
        button.place(x=600,y=400)

    def logout(self):

        self.Dashboard.destroy()
        LOGIN()

    def marksheet(self,student_id=0):

        self.Marksheet_window = Tk()
        self.Marksheet_window.geometry("1250x700")
        self.Marksheet_window.title("Student Details")
        self.Marksheet_window.configure(bg="teal")

        self.Reg_entry = ctk.CTkEntry(self.Marksheet_window, width=200,placeholder_text="REG.NO", height=40, corner_radius=20)
        self.Reg_entry.place(x=300,y=100)

        button = ctk.CTkButton(master=self.Marksheet_window,text='OK',width=5,height=37,corner_radius=20,command=self.entry_reg)
        button.place(x=440,y=101)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-1',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem1"))
        button.place(x=300,y=200)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-2',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem2"))
        button.place(x=450,y=200)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-3',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem3"))
        button.place(x=600,y=200)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-4',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem4"))
        button.place(x=300,y=350)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-5',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem5"))
        button.place(x=450,y=350)

        button=ctk.CTkButton(master=self.Marksheet_window,text='Semester-6',width=25,height=50,corner_radius=20,command=lambda s_id=student_id: self.view_marksheet(s_id,"marksheet_sem6"))
        button.place(x=600,y=350)

    def entry_reg(self):        

        student_id = self.Reg_entry.get()

        self.Marksheet_window.destroy()

        self.marksheet(student_id)

    def view_marksheet(self,student_id,sem_column):
        
        c.execute(f" SELECT {sem_column} FROM students WHERE regno = ?",(student_id,))
        result=c.fetchone()
        if result and result[0]:
            file_path = result[0]
            os.startfile(file_path)
        else:
            messagebox.showwarning("warning",f"No marksheet found for {sem_column,replace('_','').title()}.")

        self.Marksheet_window.mainloop()
        
    def student_window(self):

        self.Student_window = Toplevel(self.Dashboard)
        self.Student_window.geometry("1250x700")
        self.Student_window.title("Student Details")
        self.Student_window.configure(bg="teal")
        self.Student_window.resizable(height=False,width=False)

        menubar=Menu(self.Student_window)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="Sort",command=self.Sorting)
        filemenu.add_command(label="Search",command=self.Search)
        filemenu.add_command(label="Refresh",command=self.student_details)
        filemenu.add_command(label="Exit",command=self.back_stu)
        menubar.add_cascade(label="Options",menu=filemenu)
        self.Student_window.config(menu=menubar)

        sb=Scrollbar(self.Student_window,orient=VERTICAL)
        sb1=Scrollbar(self.Student_window,orient=HORIZONTAL)

        self.myTree = ttk.Treeview(self.Student_window)

        sb.config(command=self.myTree.yview)
        sb1.config(command=self.myTree.xview)
    
        self.myTree['columns']=('ID','Regno','Name','Dept','Gender','Sem1','Sem2','Sem3','Sem4','Sem5','Sem6','UMIS','Aadhar','Contact','Email','Days present')
    
        self.myTree.config(yscrollcommand=sb.set)
        self.myTree.config(xscrollcommand=sb1.set)
    
        self.myTree.column("#0",width=0,stretch=NO)
        self.myTree.column("#1",width=0,stretch=NO)
        self.myTree.column("#2",width=20)
        self.myTree.column("#3",width=50)
        self.myTree.column("#4",width=37)
        self.myTree.column("#5",width=10)
        self.myTree.column("#6",width=5)
        self.myTree.column("#7",width=5)
        self.myTree.column("#8",width=5)
        self.myTree.column("#9",width=5)
        self.myTree.column("#10",width=5)
        self.myTree.column("#11",width=5)
        self.myTree.column("#12",width=50)
        self.myTree.column("#13",width=15)
        self.myTree.column("#14",width=15)
        self.myTree.column("#15",width=85)
        self.myTree.column("#16",width=25)
    
        self.myTree.heading("#0",text="")
        self.myTree.heading("#1",text="ID")
        self.myTree.heading("#2",text="Regno")
        self.myTree.heading("#3",text="Name")
        self.myTree.heading("#4",text="Department")
        self.myTree.heading("#5",text="Gender")
        self.myTree.heading("#6",text="Sem1")
        self.myTree.heading("#7",text="Sem2")
        self.myTree.heading("#8",text="Sem3")
        self.myTree.heading("#9",text="Sem4")
        self.myTree.heading("#10",text="Sem5")
        self.myTree.heading("#11",text="Sem6")
        self.myTree.heading("#12",text="UMIS")
        self.myTree.heading("#13",text="Aadhar")
        self.myTree.heading("#14",text="Contact")
        self.myTree.heading("#15",text="Email")
        self.myTree.heading("#16",text="Days Present")
    
        sb.pack(side=RIGHT,fill=Y)
        sb1.pack(side=BOTTOM,fill=X)
        self.myTree.pack(expand=True, fill='both')

    def student_details(self):

        for row in self.myTree.get_children():

            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as conn:
        
            c=conn.cursor()

            for row in c.execute('SELECT * FROM students ORDER BY regno ASC'):

                conn.commit()
                self.myTree.insert('','end',values=row)

        self.Student_window.mainloop()

    def Sorting(self):

        self.Message = Toplevel(self.Dashboard)
        self.Message.geometry("400x250")
        self.Message.title("ADD")
        self.Message.resizable(height=False,width=False)

        font = (20)

        ttk.Label(self.Message,text="Select a Department",font=font).pack(pady="30")

        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)

        self.Sort=ttk.Combobox(self.Message,width="27")
        self.Sort['values']= tuple(dept_set)
        self.Sort.pack(pady="5")

        self.S_but=Button(self.Message,text="SORT",bg="blue",fg="white",command=self.insert_tree)
        self.S_but.pack(pady="5")

    def insert_tree(self):

        s_dept=self.Sort.get()

        if s_dept:

            self.Student_window.destroy()
            self.student_window()
    
            for row in self.myTree.get_children():
        
                self.myTree.delete(row)
        
            with sqlite3.connect('student_management.db') as conn:

                c=conn.cursor()

                for row in c.execute('SELECT * FROM students WHERE dept = ?',(s_dept,)):
            
                    conn.commit()
                    self.myTree.insert('','end',values=row)

    def Search(self):

        ttk.Label(self.Student_window,text="Enter a Reg.No").pack()

        self.search=Entry(self.Student_window,width="30")
        self.search.pack()

        s_but=Button(self.Student_window,text="SEARCH",bg="blue",fg="white",command=self.search_tree)
        s_but.pack()

    def search_tree(self):

        s_reg=self.search.get()

        self.Student_window.destroy()
        self.student_window()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)

        with sqlite3.connect('student_management.db') as conn:

            c=conn.cursor()

            for row in c.execute('SELECT * FROM students WHERE regno = ?',(s_reg,)):

                conn.commit()

                if row:

                    self.myTree.insert('','end',values=row)

                else:

                     messagebox.showerror('Invalid Input','Data not found')
    def add_dept(self):

        self.Dept_window = Toplevel(self.Dashboard)
        self.Dept_window.geometry("400x250")
        self.Dept_window.title("ADD")
        self.Dept_window.resizable(height=False,width=False)

        font = (20)

        ttk.Label(self.Dept_window,text="Enter New Department Name ",font=font).pack(pady="30")

        self.new_dept_value = Entry(self.Dept_window,width="50")
        self.new_dept_value.pack(pady="5")

        ttk.Button(self.Dept_window,text="Submit",command=self.new_dept).pack(pady="5")

    def new_dept(self):

        new = self.new_dept_value.get()
        self.Dept_window.destroy()

        if new:

            try:

                dc.execute('INSERT INTO dept(name)VALUES(?)',(new,))
                print('Success')
                dcn.commit()

                messagebox.showinfo('Success','Department added successfully')
                
            except:
                messagebox.showerror('Failed','Cannot Insert Value')

    def rmv_dept(self):

        self.Dept_window = Toplevel(self.Dashboard)
        self.Dept_window.geometry("400x250")
        self.Dept_window.title("Remove")
        self.Dept_window.resizable(height=False,width=False)

        font = (20)

        ttk.Label(self.Dept_window,text="Enter Department Name ",font=font).pack(pady="30")

        self.new_dept_value = Entry(self.Dept_window,width="50")
        self.new_dept_value.pack(pady="5")

        ttk.Button(self.Dept_window,text="Submit",command=self.dept_rmv).pack(pady="5")

    def dept_rmv(self):

        new = self.new_dept_value.get()
        self.Dept_window.destroy()

        if new:

            try:

                dc.execute('DELETE FROM dept WHERE name=?',(new,))
                print('Success')
                dcn.commit()

                messagebox.showinfo('Success','Department Deleted successfully')
                
            except:
                messagebox.showerror('Failed','Cannot Delete Value')

    def back_stu(self):

        self.Student_window.destroy()

    def CollegeFee(self):

        self.window=Tk()
        self.window.geometry("1250x700")
        self.window.title("S-M-S")
        self.window.configure(bg="teal")
        self.window.resizable(height=False,width=False)

        menubar=Menu(self.window)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="Exit",command=self.back_clg)
        menubar.add_cascade(label="Options",menu=filemenu)
        self.window.config(menu=menubar)
    
        sb=Scrollbar(self.window,orient=VERTICAL)
        sb1=Scrollbar(self.window,orient=HORIZONTAL)
        
        f=Frame(self.window,bg="black")
        f.pack(pady=5,fill=X)
    
        s_but=Button(f,text="SEARCH",bg="blue",fg="white",command=self.Search_Tree)
        s_but.pack(side=RIGHT)
    
        self.search=Entry(f,width="30")
        self.search.pack(side=RIGHT)
    
        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)
            
        self.Sort=ttk.Combobox(f,width="27")
        self.Sort['values']= tuple(dept_set)
        self.Sort.pack(side=LEFT)
    
        self.S_but=Button(f,text="SORT",bg="blue",fg="white",height=0,command=self.Sorting_Tree)
        self.S_but.pack(side=LEFT)
    
        self.myfont=Font(family="Algerian",weight="bold",size=20)
        self.myfont2=Font(size=12)
    
        l=Label(f,text="College Fee",fg="silver",bg="black",font=self.myfont)
        l.pack()
    
        f1=Frame(self.window,bg="teal",highlightbackground="black",highlightthickness=2)
        f1.pack(pady=20)
    
        stu_reg=Label(f1,text="Register no :",font=self.myfont2,fg="black",bg="teal")
        stu_reg.grid(row=5,column=3,sticky=E,padx=20)
    
        self.reg_entry=Entry(f1,width="30")
        self.reg_entry.grid(row=5,column=4)
    
        stu_dept=Label(f1,text="Department :",font=self.myfont2,fg="black",bg="teal")
        stu_dept.grid(row=7,column=3,sticky=E,pady=10,padx=20)

        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)
            
        self.dept_entry=ttk.Combobox(f1,width="27")
        self.dept_entry['values']= tuple(dept_set)
        self.dept_entry.grid(row=7,column=4)
    
        sem1=Label(f1,text="Semester :",font=self.myfont2,fg="black",bg="teal")
        sem1.grid(row=8,column=3,sticky=E,pady=10,padx=20)
        
        self.sem1_entry=Entry(f1,width="30")
        self.sem1_entry.grid(row=8,column=4)

        Total_amount = Label(f1,text="Total :",font=self.myfont2,fg="black",bg="teal")
        Total_amount.grid(row=9,column=3,sticky=E,pady=10,padx=20)

        self.Total_entry=Entry(f1,width="30")
        self.Total_entry.grid(row=9,column=4)

        Pay_amount = Label(f1,text="Amount Paying :",font=self.myfont2,fg="black",bg="teal")
        Pay_amount.grid(row=10,column=3,sticky=E,pady=10,padx=20)

        self.Pay_entry=Entry(f1,width="30")
        self.Pay_entry.grid(row=10,column=4)
    
        f3=Frame(self.window,bg="teal")
        f3.pack(pady=20)
    
        btn1=Button(f3,text="ADD",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.add_student)
        btn1.grid(row=15,column=3,padx=5)
       
        btn4 = Button(f3,text="Update",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.update_student)
        btn4.grid(row=15,column=4,padx=5)
    
        btn2=Button(f3,text="Clear",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.clear)
        btn2.grid(row=15,column=5,padx=5)
    
        btn3=Button(f3,text="Delete",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.delete_student)
        btn3.grid(row=15,column=6,padx=5)
    
        btn5=Button(f3,text="Select",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.selectrecord)
        btn5.grid(row=15,column=7,padx=5)
    
        self.myTree = ttk.Treeview(self.window)
    
        sb.config(command=self.myTree.yview)
        sb1.config(command=self.myTree.xview)
    
        self.myTree['columns']=('ID','Regno','Dept','Sem','Paid','Balance','Total','Date')
    
        self.myTree.config(yscrollcommand=sb.set)
        self.myTree.config(xscrollcommand=sb1.set)
    
        self.myTree.column("#0",width=0,stretch=NO)
        self.myTree.column("#1",width=0,stretch=NO)
        self.myTree.column("#2",width=50)
        self.myTree.column("#3",width=50)
        self.myTree.column("#4",width=50)
        self.myTree.column("#5",width=50)
        self.myTree.column("#6",width=50)
        self.myTree.column("#7",width=50)
        self.myTree.column("#8",width=50)
    
        self.myTree.heading("#0",text="")
        self.myTree.heading("#1",text="ID")
        self.myTree.heading("#2",text="Regno")
        self.myTree.heading("#3",text="Department")
        self.myTree.heading("#4",text="Semester")
        self.myTree.heading("#5",text="Paid")
        self.myTree.heading("#6",text="Balance")
        self.myTree.heading("#7",text="Total")
        self.myTree.heading("#8",text="Date")
    
        sb.pack(side=RIGHT,fill=Y)
        sb1.pack(side=BOTTOM,fill=X)
        self.myTree.pack(fill=X,pady=15)

        self.view_students()

    def add_student(self):
        regno=self.reg_entry.get()
        dept=self.dept_entry.get()
        Semester=self.sem1_entry.get()
        Total = self.Total_entry.get()
        Pay = self.Pay_entry.get()
        date = datetime.now()

        Balance = int(Total)-int(Pay)
   
        if regno and dept and Semester and Total and Pay and date:
       
            fc.execute('INSERT INTO CollegeFee (regno,dept,sem,paid,balance,Total,date)VALUES(?,?,?,?,?,?,?)',(regno,dept,Semester,Pay,Balance,Total,date))
            fcn.commit()
            messagebox.showinfo('Success','Student added successfully')
            self.view_students()
            self.clear()

        else:

            messagebox.showwarning('Input Error','please fill out all fields')

    def Search_Tree(self):

        s_reg=self.search.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)

        with sqlite3.connect('student_management.db') as conn:

            c=conn.cursor()

            for row in c.execute('SELECT * FROM CollegeFee WHERE regno = ?',(s_reg,)):

                conn.commit()

                if row:

                    self.myTree.insert('','end',values=row)

                else:

                     messagebox.showerror('Invalid Input','Data not found')
            

    def Sorting_Tree(self):

        s_dept=self.Sort.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as fcn:

            fc=fcn.cursor()

            for row in fc.execute('SELECT * FROM CollegeFee WHERE dept = ?',(s_dept,)):
            
                fcn.commit()
                self.myTree.insert('','end',values=row)

    def view_students(self):

        for row in self.myTree.get_children():

            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as conn:
        
            c=conn.cursor()

            for row in c.execute('SELECT * FROM CollegeFee ORDER BY regno ASC'):

                conn.commit()
                self.myTree.insert('','end',values=row)

    def delete_student(self):
    
        selected=self.myTree.focus()

        if selected:

            stuid=self.myTree.item(selected,'values')[0]
            c.execute('DELETE FROM CollegeFee WHERE id=?',(stuid))
            conn.commit()
            messagebox.showinfo('Success','Student deleted successfully')
            self.view_students()

    def clear(self):

        self.reg_entry.delete(0,END)
        self.dept_entry.delete(0,END)
        self.sem1_entry.delete(0,END)
        self.Total_entry.delete(0,END)
        self.Pay_entry.delete(0,END)

    def selectrecord(self):
   
        selected=self.myTree.focus()

        if selected :
            
            stuid=self.myTree.item(selected,'values')
            self.reg_entry.insert(0,stuid[1])
            self.dept_entry.insert(0,stuid[2])
            self.sem1_entry.insert(0,stuid[3])
            self.Total_entry.insert(0,stuid[4])
            self.Pay_entry.insert(0,stuid[5])

    def update_student(self):

        selected=self.myTree.focus()
    
        if selected:
        
            stuid=self.myTree.item(selected,'values')[0]
            new_regno=self.reg_entry.get()
            new_dept=self.dept_entry.get()
            new_sm1=self.sem1_entry.get()
            new_Total=self.Total_entry.get()
            new_Pay=self.Pay_entry.get()
            date = datetime.now()

            Balance = int(new_Total)-int(new_Pay)
           
            if new_regno and new_dept and new_sm1 and new_Total and new_Pay and Balance:
                c.execute('UPDATE CollegeFee SET regno=?,dept=?,sem=?,Total=?,paid=?,balance=?,date=? WHERE id=?',(new_regno,new_dept,new_sm1,new_Total,new_Pay,Balance,date,stuid))
                conn.commit()
                messagebox.showinfo('Success','student updated successfully')
                self.view_students()
                self.clear()
            else:
                messagebox.showwarning('Input Error','Please select a field')

    def BusFee(self):

        self.window=Tk()
        self.window.geometry("1250x700")
        self.window.title("S-M-S")
        self.window.configure(bg="teal")
        self.window.resizable(height=False,width=False)

        menubar=Menu(self.window)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="Exit",command=self.back_clg)
        menubar.add_cascade(label="Options",menu=filemenu)
        self.window.config(menu=menubar)
    
        sb=Scrollbar(self.window,orient=VERTICAL)
        sb1=Scrollbar(self.window,orient=HORIZONTAL)
        
        f=Frame(self.window,bg="black")
        f.pack(pady=5,fill=X)
    
        s_but=Button(f,text="SEARCH",bg="blue",fg="white",command=self.Search_Tree_bus)
        s_but.pack(side=RIGHT)
    
        self.search=Entry(f,width="30")
        self.search.pack(side=RIGHT)
    
        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)
            
        self.Sort=ttk.Combobox(f,width="27")
        self.Sort['values']= tuple(dept_set)
        self.Sort.pack(side=LEFT)
    
        self.S_but=Button(f,text="SORT",bg="blue",fg="white",height=0,command=self.Sorting_Tree_bus)
        self.S_but.pack(side=LEFT)
    
        self.myfont=Font(family="Algerian",weight="bold",size=20)
        self.myfont2=Font(size=12)
    
        l=Label(f,text="Bus Fee",fg="silver",bg="black",font=self.myfont)
        l.pack()
    
        f1=Frame(self.window,bg="teal",highlightbackground="black",highlightthickness=2)
        f1.pack(pady=20)
    
        stu_reg=Label(f1,text="Register no :",font=self.myfont2,fg="black",bg="teal")
        stu_reg.grid(row=5,column=3,sticky=E,padx=20)
    
        self.reg_entry=Entry(f1,width="30")
        self.reg_entry.grid(row=5,column=4)
    
        stu_dept=Label(f1,text="Department :",font=self.myfont2,fg="black",bg="teal")
        stu_dept.grid(row=7,column=3,sticky=E,pady=10,padx=20)

        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)
            
        self.dept_entry=ttk.Combobox(f1,width="27")
        self.dept_entry['values']= tuple(dept_set)
        self.dept_entry.grid(row=7,column=4)
    
        sem1=Label(f1,text="Semester :",font=self.myfont2,fg="black",bg="teal")
        sem1.grid(row=8,column=3,sticky=E,pady=10,padx=20)
        
        self.sem1_entry=Entry(f1,width="30")
        self.sem1_entry.grid(row=8,column=4)

        Total_amount = Label(f1,text="Total :",font=self.myfont2,fg="black",bg="teal")
        Total_amount.grid(row=9,column=3,sticky=E,pady=10,padx=20)

        self.Total_entry=Entry(f1,width="30")
        self.Total_entry.grid(row=9,column=4)

        Pay_amount = Label(f1,text="Amount Paying :",font=self.myfont2,fg="black",bg="teal")
        Pay_amount.grid(row=10,column=3,sticky=E,pady=10,padx=20)

        self.Pay_entry=Entry(f1,width="30")
        self.Pay_entry.grid(row=10,column=4)
    
        f3=Frame(self.window,bg="teal")
        f3.pack(pady=20)
    
        btn1=Button(f3,text="ADD",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.add_student_bus)
        btn1.grid(row=15,column=3,padx=5)
       
        btn4 = Button(f3,text="Update",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.update_student_bus)
        btn4.grid(row=15,column=4,padx=5)
    
        btn2=Button(f3,text="Clear",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.clear)
        btn2.grid(row=15,column=5,padx=5)
    
        btn3=Button(f3,text="Delete",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.delete_student_bus)
        btn3.grid(row=15,column=6,padx=5)
    
        btn5=Button(f3,text="Select",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.selectrecord)
        btn5.grid(row=15,column=7,padx=5)
    
        self.myTree = ttk.Treeview(self.window)
    
        sb.config(command=self.myTree.yview)
        sb1.config(command=self.myTree.xview)
    
        self.myTree['columns']=('ID','Regno','Dept','Sem','Paid','Balance','Total','Date')
    
        self.myTree.config(yscrollcommand=sb.set)
        self.myTree.config(xscrollcommand=sb1.set)
    
        self.myTree.column("#0",width=0,stretch=NO)
        self.myTree.column("#1",width=0,stretch=NO)
        self.myTree.column("#2",width=50)
        self.myTree.column("#3",width=50)
        self.myTree.column("#4",width=50)
        self.myTree.column("#5",width=50)
        self.myTree.column("#6",width=50)
        self.myTree.column("#7",width=50)
        self.myTree.column("#8",width=50)
    
        self.myTree.heading("#0",text="")
        self.myTree.heading("#1",text="ID")
        self.myTree.heading("#2",text="Regno")
        self.myTree.heading("#3",text="Department")
        self.myTree.heading("#4",text="Semester")
        self.myTree.heading("#5",text="Paid")
        self.myTree.heading("#6",text="Balance")
        self.myTree.heading("#7",text="Total")
        self.myTree.heading("#8",text="Date")
    
        sb.pack(side=RIGHT,fill=Y)
        sb1.pack(side=BOTTOM,fill=X)
        self.myTree.pack(fill=X,pady=15)

        self.view_students_bus()

    def add_student_bus(self):
        regno=self.reg_entry.get()
        dept=self.dept_entry.get()
        Semester=self.sem1_entry.get()
        Total = self.Total_entry.get()
        Pay = self.Pay_entry.get()
        date = datetime.now()

        Balance = int(Total)-int(Pay)
   
        if regno and dept and Semester and Total and Pay and date:
       
            fc.execute('INSERT INTO BusFee (regno,dept,sem,paid,balance,Total,date)VALUES(?,?,?,?,?,?,?)',(regno,dept,Semester,Pay,Balance,Total,date))
            fcn.commit()
            messagebox.showinfo('Success','Student added successfully')
            self.view_students_bus()
            self.clear()

        else:

            messagebox.showwarning('Input Error','please fill out all fields')

    def delete_student_bus(self):
    
        selected=self.myTree.focus()

        if selected:

            stuid=self.myTree.item(selected,'values')[0]
            c.execute('DELETE FROM BusFee WHERE id=?',(stuid))
            conn.commit()
            messagebox.showinfo('Success','Student deleted successfully')
            self.view_students_bus()

    def view_students_bus(self):

        for row in self.myTree.get_children():

            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as conn:
        
            c=conn.cursor()

            for row in c.execute('SELECT * FROM BusFee ORDER BY regno ASC'):

                conn.commit()
                self.myTree.insert('','end',values=row)

    def update_student_bus(self):

        selected=self.myTree.focus()
    
        if selected:
        
            stuid=self.myTree.item(selected,'values')[0]
            new_regno=self.reg_entry.get()
            new_dept=self.dept_entry.get()
            new_sm1=self.sem1_entry.get()
            new_Total=self.Total_entry.get()
            new_Pay=self.Pay_entry.get()
            date = datetime.now()

            Balance = int(new_Total)-int(new_Pay)
           
            if new_regno and new_dept and new_sm1 and new_Total and new_Pay and Balance and date:
                c.execute('UPDATE BusFee SET regno=?,dept=?,sem=?,Total=?,paid=?,balance=?,date=? WHERE id=?',(new_regno,new_dept,new_sm1,new_Total,new_Pay,Balance,date,stuid))
                conn.commit()
                messagebox.showinfo('Success','student updated successfully')
                self.view_students_bus()
                self.clear()
            else:
                messagebox.showwarning('Input Error','Please select a field')
    def Search_Tree_bus(self):

        s_reg=self.search.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)

        with sqlite3.connect('student_management.db') as conn:

            c=conn.cursor()

            for row in c.execute('SELECT * FROM BusFee WHERE regno = ?',(s_reg,)):

                conn.commit()

                if row:

                    self.myTree.insert('','end',values=row)

                else:

                     messagebox.showerror('Invalid Input','Data not found')
            

    def Sorting_Tree_bus(self):

        s_dept=self.Sort.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as fcn:

            fc=fcn.cursor()

            for row in fc.execute('SELECT * FROM BusFee WHERE dept = ?',(s_dept,)):
            
                fcn.commit()
                self.myTree.insert('','end',values=row)

    def back_clg(self):

        self.window.destroy()
                   
class STU_Entry:

    def __init__(self):
    
        self.window=Tk()
        self.window.geometry("1250x700")
        self.window.title("S-M-S")
        self.window.configure(bg="teal")
        self.window.resizable(height=False,width=False)
    
        sb=Scrollbar(self.window,orient=VERTICAL)
        sb1=Scrollbar(self.window,orient=HORIZONTAL)

        menubar=Menu(self.window)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="Export",command=self.Export_Data)
        filemenu.add_command(label="Refresh",command=self.view_students)
        filemenu.add_command(label="Attendance",command=self.Attendance)
        filemenu.add_command(label="LOG-OUT",command=self.logout)
        menubar.add_cascade(label="File",menu=filemenu)
        self.window.config(menu=menubar)
        
        f=Frame(self.window,bg="black")
        f.pack(pady=5,fill=X)
    
        s_but=Button(f,text="SEARCH",bg="blue",fg="white",command=self.Search)
        s_but.pack(side=RIGHT)
    
        self.search=Entry(f,width="30")
        self.search.pack(side=RIGHT)
    
        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        print(depts)

        for dept in depts:

            dept_set.add(dept)
            
        self.Sort=ttk.Combobox(f,width="27")
        self.Sort['values']= tuple(dept_set)
        self.Sort.pack(side=LEFT)
    
        self.S_but=Button(f,text="SORT",bg="blue",fg="white",height=0,command=self.Sorting)
        self.S_but.pack(side=LEFT)
    
        self.myfont=Font(family="Algerian",weight="bold",size=20)
        self.myfont2=Font(size=12)
    
        l=Label(f,text="STUDENT DATAS",fg="silver",bg="black",font=self.myfont)
        l.pack()
    
        f1=Frame(self.window,bg="teal",highlightbackground="black",highlightthickness=2)
        f1.pack(pady=20)
    
        stu_reg=Label(f1,text="Register no :",font=self.myfont2,fg="black",bg="teal")
        stu_reg.grid(row=5,column=3,sticky=E,padx=20)
    
        self.reg_entry=Entry(f1,width="30")
        self.reg_entry.grid(row=5,column=4)
    
        stu_name=Label(f1,text="Student Name :",font=self.myfont2,fg="black",bg="teal")
        stu_name.grid(row=6,column=3,sticky=E,pady=10,padx=20)
    
        self.name_entry=Entry(f1,width="30")
        self.name_entry.grid(row=6,column=4)
    
        stu_dept=Label(f1,text="Department :",font=self.myfont2,fg="black",bg="teal")
        stu_dept.grid(row=7,column=3,sticky=E,pady=10,padx=20)

        dc.execute('SELECT name FROM dept')
        depts = dc.fetchall()

        for dept in depts:

            dept_set.add(dept)
            
        self.dept_entry=ttk.Combobox(f1,width="27")
        self.dept_entry['values']= tuple(dept_set)
        self.dept_entry.grid(row=7,column=4)
    
        sem1=Label(f1,text="sem1 :",font=self.myfont2,fg="black",bg="teal")
        sem1.grid(row=8,column=3,sticky=E,pady=10,padx=20)
        
        self.sem1_entry=Entry(f1,width="30")
        self.sem1_entry.grid(row=8,column=4)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem1"))
        upload_btn.grid(row=8,column=4,sticky=E)
    
        sem2=Label(f1,text="sem2 :",font=self.myfont2,fg="black",bg="teal")
        sem2.grid(row=9,column=3,sticky=E,pady=10,padx=20)
    
        self.sem2_entry=Entry(f1,width="30")
        self.sem2_entry.grid(row=9,column=4)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem2"))
        upload_btn.grid(row=9,column=4,sticky=E)
    
        sem3=Label(f1,text="sem3 :",font=self.myfont2,fg="black",bg="teal")
        sem3.grid(row=10,column=3,sticky=E,pady=10,padx=20)
    
        self.sem3_entry=Entry(f1,width="30")
        self.sem3_entry.grid(row=10,column=4)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem3"))
        upload_btn.grid(row=10,column=4,sticky=E)
    
        sem4=Label(f1,text="sem4 :",font=self.myfont2,fg="black",bg="teal")
        sem4.grid(row=11,column=3,sticky=E,pady=10,padx=20)
    
        self.sem4_entry=Entry(f1,width="30")
        self.sem4_entry.grid(row=11,column=4)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem4"))
        upload_btn.grid(row=11,column=4,sticky=E)
    
        sem5=Label(f1,text="sem5 :",font=self.myfont2,fg="black",bg="teal")
        sem5.grid(row=5,column=6,sticky=E,pady=5,padx=10)
    
        self.sem5_entry=Entry(f1,width="30")
        self.sem5_entry.grid(row=5,column=7)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem5"))
        upload_btn.grid(row=5,column=7,sticky=E)
    
        sem6=Label(f1,text="sem6 :",font=self.myfont2,fg="black",bg="teal")
        sem6.grid(row=6,column=6,sticky=E,pady=5,padx=10)
    
        self.sem6_entry=Entry(f1,width="30")
        self.sem6_entry.grid(row=6,column=7)

        upload_btn = ctk.CTkButton(f1,text="upload",width=10,height=1,corner_radius=30,command = lambda: self.upload_marksheet("marksheet_sem6"))
        upload_btn.grid(row=6,column=7,sticky=E)
    
        umis=Label(f1,text="UMIS number :",font=self.myfont2,fg="black",bg="teal")
        umis.grid(row=7,column=6,sticky=E,pady=5,padx=10)
    
        self.umis_entry=Entry(f1,width="30")
        self.umis_entry.grid(row=7,column=7)
    
        aadhar=Label(f1,text="Aadhar number :",font=self.myfont2,fg="black",bg="teal")
        aadhar.grid(row=8,column=6,sticky=E,pady=5,padx=10)
    
        self.aadhar_entry=Entry(f1,width="30")
        self.aadhar_entry.grid(row=8,column=7)
    
        contact=Label(f1,text="Contact :",font=self.myfont2,fg="black",bg="teal")
        contact.grid(row=9,column=6,sticky=E,pady=5,padx=10)
    
        self.contact_entry=Entry(f1,width="30")
        self.contact_entry.grid(row=9,column=7)
    
        email=Label(f1,text="Email id :",font=self.myfont2,fg="black",bg="teal")
        email.grid(row=10,column=6,sticky=E,pady=5,padx=10)
    
        self.email_entry=Entry(f1,width="30")
        self.email_entry.grid(row=10,column=7)
    
        gender=Label(f1,text="Gender :",font=self.myfont2,fg="black",bg="teal")
        gender.grid(row=11,column=6,sticky=E,pady=5,padx=10)
    
        self.chk1=IntVar()
        self.chk2=Radiobutton(f1,text="Male",variable=self.chk1,value=1,bg="teal")
        self.chk2.grid(row=11,column=7)
        self.chk3=Radiobutton(f1,text="Female",variable=self.chk1,value=2,bg="teal")
        self.chk3.grid(row=11,column=8)
        self.chk4=Radiobutton(f1,text="Others",variable=self.chk1,value=3,bg="teal")
        self.chk4.grid(row=11,column=9)
    
        f3=Frame(self.window,bg="teal")
        f3.pack(pady=20)
    
        btn1=Button(f3,text="ADD",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.add_student)
        btn1.grid(row=15,column=3,padx=5)
       
        btn4 = Button(f3,text="Update",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.update_student)
        btn4.grid(row=15,column=4,padx=5)
    
        btn2=Button(f3,text="Clear",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.clear)
        btn2.grid(row=15,column=5,padx=5)
    
        btn3=Button(f3,text="Delete",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.delete_student)
        btn3.grid(row=15,column=6,padx=5)
    
        btn5=Button(f3,text="Select",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.selectrecord)
        btn5.grid(row=15,column=7,padx=5)
    
        self.myTree = ttk.Treeview(self.window)
    
        sb.config(command=self.myTree.yview)
        sb1.config(command=self.myTree.xview)
    
        self.myTree['columns']=('ID','Regno','Name','Dept','Gender','Sem1','Sem2','Sem3','Sem4','Sem5','Sem6','UMIS','Aadhar','Contact','Email','Days present')
    
        self.myTree.config(yscrollcommand=sb.set)
        self.myTree.config(xscrollcommand=sb1.set)
    
        self.myTree.column("#0",width=0,stretch=NO)
        self.myTree.column("#1",width=0,stretch=NO)
        self.myTree.column("#2",width=50)
        self.myTree.column("#3",width=50)
        self.myTree.column("#4",width=50)
        self.myTree.column("#5",width=50)
        self.myTree.column("#6",width=0,stretch=NO)
        self.myTree.column("#7",width=0,stretch=NO)
        self.myTree.column("#8",width=0,stretch=NO)
        self.myTree.column("#9",width=0,stretch=NO)
        self.myTree.column("#10",width=0,stretch=NO)
        self.myTree.column("#11",width=0,stretch=NO)
        self.myTree.column("#12",width=50)
        self.myTree.column("#13",width=50)
        self.myTree.column("#14",width=50)
        self.myTree.column("#15",width=50)
        self.myTree.column("#16",width=50)
    
        self.myTree.heading("#0",text="")
        self.myTree.heading("#1",text="ID")
        self.myTree.heading("#2",text="Regno")
        self.myTree.heading("#3",text="Name")
        self.myTree.heading("#4",text="Department")
        self.myTree.heading("#5",text="Gender")
        self.myTree.heading("#6",text="Sem1")
        self.myTree.heading("#7",text="Sem2")
        self.myTree.heading("#8",text="Sem3")
        self.myTree.heading("#9",text="Sem4")
        self.myTree.heading("#10",text="Sem5")
        self.myTree.heading("#11",text="Sem6")
        self.myTree.heading("#12",text="UMIS")
        self.myTree.heading("#13",text="Aadhar")
        self.myTree.heading("#14",text="Contact")
        self.myTree.heading("#15",text="Email")
        self.myTree.heading("#16",text="Days Present")
    
        sb.pack(side=RIGHT,fill=Y)
        sb1.pack(side=BOTTOM,fill=X)
        self.myTree.pack(fill=X,pady=15)

        self.view_students()
        LOGIN.Destroy()

    def logout(self):

        self.window.destroy()
        LOGIN()

    def upload_marksheet(self, sem_column):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files","*.pdf")])

        if file_path:
            setattr(self, sem_column, file_path)
            messagebox.showinfo("Success",f"Marksheet for {sem_column.replace('_','').title()} uploaded successfully.")

    def Export_Data(self):
   
        file=filedialog.asksaveasfilename(initialdir=csv_path,title="SaveCSV",filetype=(("CSV File","*.csv"),("All Files","*.*")))
        with open(file,mode='w',newline='')as myfile:
            exp_writer = csv.writer(myfile,delimiter='\t')
            for i in self.myTree.get_children():
                row = self.myTree.item(i)['values']
                exp_writer.writerow(row)
        self.view_students()

    def add_student(self):
        regno=self.reg_entry.get()
        name=self.name_entry.get()
        dept=self.dept_entry.get()
        marksheet_sem1=getattr(self,"marksheet_sem1",None)
        marksheet_sem2=getattr(self,"marksheet_sem2",None)
        marksheet_sem3=getattr(self,"marksheet_sem3",None)
        marksheet_sem4=getattr(self,"marksheet_sem4",None)
        marksheet_sem5=getattr(self,"marksheet_sem5",None)
        marksheet_sem6=getattr(self,"marksheet_sem6",None)
        UMISno=self.umis_entry.get()
        Aadharno=self.aadhar_entry.get()
        Contactno=self.contact_entry.get()
        Email=self.email_entry.get()
   
        if self.chk1.get()==1:
            Gender=self.chk2.cget("text")

        elif self.chk1.get()==2:
            Gender=self.chk3.cget("text")

        else:
            Gender=self.chk4.cget("text")
   
        if regno and name and dept and Gender and UMISno and Aadharno and Contactno and Email:
       
            c.execute('INSERT INTO students (regno,name,dept,Gender,marksheet_sem1,marksheet_sem2,marksheet_sem3,marksheet_sem4,marksheet_sem5,marksheet_sem6,UMISnumber,Aadhar,Contact,Email)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(regno,name,dept,Gender,marksheet_sem1,marksheet_sem2,marksheet_sem3,marksheet_sem4,marksheet_sem5,marksheet_sem6,UMISno,Aadharno,Contactno,Email))
            conn.commit()
            messagebox.showinfo('Success','Student added successfully')
            self.view_students()
            self.clear()

        else:

            messagebox.showwarning('Input Error','please fill out all fields')

    def Search(self):

        s_reg=self.search.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)

        with sqlite3.connect('student_management.db') as conn:

            c=conn.cursor()

            for row in c.execute('SELECT * FROM students WHERE regno = ?',(s_reg,)):

                conn.commit()

                if row:

                    self.myTree.insert('','end',values=row)

                else:

                    messagebox.showerror('Invalid Input','Data not found')

                    self.view_students()

    def Search_atd(self):

        s_reg=self.search.get()
    
        for row in self.myTree2.get_children():
        
            self.myTree2.delete(row)

        with sqlite3.connect('student_management.db') as acn:

            ac=acn.cursor()

            for row in ac.execute('SELECT * FROM attendance WHERE regno = ?',(s_reg,)):

                acn.commit()

                if row:

                    self.myTree2.insert('','end',values=row)

                else:

                    messagebox.showerror('Invalid Input','Data not found')
                    self.view_students_atd()

    def Sorting(self):

        s_dept=self.Sort.get()
    
        for row in self.myTree.get_children():
        
            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as conn:

            c=conn.cursor()

            for row in c.execute('SELECT * FROM students WHERE dept = ?',(s_dept,)):
            
                conn.commit()
                if row:
                    
                    self.myTree.insert('','end',values=row)
                else:
                    self.view_students()

    def view_students(self):

        for row in self.myTree.get_children():

            self.myTree.delete(row)
        
        with sqlite3.connect('student_management.db') as conn:
        
            c=conn.cursor()

            for row in c.execute('SELECT * FROM students ORDER BY regno ASC'):

                conn.commit()
                self.myTree.insert('','end',values=row)

 
    def delete_student(self):

        try:
    
            selected=self.myTree.focus()

            if selected:

                stuid=self.myTree.item(selected,'values')[0]
                c.execute('DELETE FROM students WHERE id=?',(stuid))
                conn.commit()
                messagebox.showinfo('Success','Student deleted successfully')
                self.view_students()
        except:

            selected=self.myTree2.focus()

            if selected:

                stuid=self.myTree2.item(selected,'values')[0]
                ac.execute('DELETE FROM attendance WHERE id=?',(stuid))
                acn.commit()
                messagebox.showinfo('Success','Student deleted successfully')
                self.view_students_atd()

    def clear(self):

        try:

            self.reg_entry.delete(0,END)
            self.name_entry.delete(0,END)
            self.dept_entry.delete(0,END)
            self.sem1_entry.delete(0,END)
            self.sem2_entry.delete(0,END)
            self.sem3_entry.delete(0,END)
            self.sem4_entry.delete(0,END)
            self.sem5_entry.delete(0,END)
            self.sem6_entry.delete(0,END)
            self.umis_entry.delete(0,END)
            self.aadhar_entry.delete(0,END)
            self.contact_entry.delete(0,END)
            self.email_entry.delete(0,END)
            self.view_students()

        except:

            pass

    def selectrecord(self):

        try:
            selected=self.myTree.focus()

            if selected :
            
                stuid=self.myTree.item(selected,'values')
                self.reg_entry.insert(0,stuid[1])
                self.name_entry.insert(0,stuid[2])
                self.dept_entry.insert(0,stuid[3])
                self.sem1_entry.insert(0,stuid[5])
                self.sem2_entry.insert(0,stuid[6])
                self.sem3_entry.insert(0,stuid[7])
                self.sem4_entry.insert(0,stuid[8])
                self.sem5_entry.insert(0,stuid[9])
                self.sem6_entry.insert(0,stuid[10])
                self.umis_entry.insert(0,stuid[11])
                self.aadhar_entry.insert(0,stuid[12])
                self.contact_entry.insert(0,stuid[13])
                self.email_entry.insert(0,stuid[14])

        except:

            selected = self.myTree2.focus()

            if selected :

                stuid = self.myTree2.item(selected,'values')
                self.reg_entry.insert(0,stuid[1])

    def update_student(self):

        selected=self.myTree.focus()
    
        if selected:
        
            stuid=self.myTree.item(selected,'values')[0]
            new_regno=self.reg_entry.get()
            new_name=self.name_entry.get()
            new_dept=self.dept_entry.get()

            if self.chk1.get()==1:
                new_Gender=self.chk2.cget("text")
            elif self.chk1.get()==2:
                new_Gender=self.chk3.cget("text")
            else:
                new_Gender=self.chk4.cget("text")
        
            new_sm1=self.sem1_entry.get()
            new_sm2=self.sem2_entry.get()
            new_sm3=self.sem3_entry.get()
            new_sm4=self.sem4_entry.get()
            new_sm5=self.sem5_entry.get()
            new_sm6=self.sem6_entry.get()
            new_UMISno=self.umis_entry.get()
            new_Aadharno=self.aadhar_entry.get()
            new_Contactno=self.contact_entry.get()
            new_Email=self.email_entry.get()
        
            if self.chk1.get()==1:
                new_Gender=self.chk2.cget("text")
            elif self.chk1.get()==2:
                new_Gender=self.chk3.cget("text")
            else:
                new_Gender=self.chk4.cget("text")

            if new_regno and new_name and new_dept and new_Gender and new_sm1 and new_sm2 and new_sm3 and new_sm4 and new_sm5 and new_sm6 and new_UMISno and new_Aadharno and new_Contactno and new_Email:
                c.execute('UPDATE students SET regno=?,name=?,dept=?,Gender=?,marksheet_sem1=?,marksheet_sem2=?,marksheet_sem3=?,marksheet_sem4=?,marksheet_sem5=?,marksheet_sem6=?,UMISnumber=?,Aadhar=?,Contact=?,Email=? WHERE id=?',(new_regno,new_name,new_dept,new_Gender,new_sm1,new_sm2,new_sm3,new_sm4,new_sm5,new_sm6,new_UMISno,new_Aadharno,new_Contactno,new_Email,stuid))
                conn.commit()
                messagebox.showinfo('Success','student updated successfully')
                self.view_students()
                self.clear()
            else:
                messagebox.showwarning('Input Error','Please select a field')

    def Save_Image():
        pass

    def Attendance(self):

        self.window.destroy()

        self.window3=Tk()
        self.window3.geometry("1000x500")
        self.window3.title("S-M-S")
        self.window3.configure(bg="teal")
        self.window3.resizable(height=False,width=False)

        menubar=Menu(self.window3)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="Exit",command=self.back_atd)
        menubar.add_cascade(label="Options",menu=filemenu)
        self.window3.config(menu=menubar)
    
        sb=Scrollbar(self.window3,orient=VERTICAL)
        sb1=Scrollbar(self.window3,orient=HORIZONTAL)
        
        f=Frame(self.window3,bg="black")
        f.pack(pady=5,fill=X)
    
        s_but=Button(f,text="SEARCH",bg="blue",fg="white",command=self.Search_atd)
        s_but.pack(side=RIGHT)
    
        self.search=Entry(f,width="30")
        self.search.pack(side=RIGHT)
    
        l=Label(f,text="Attendance",fg="silver",bg="black",font=self.myfont)
        l.pack()
    
        f1=Frame(self.window3,bg="teal",highlightbackground="black",highlightthickness=2)
        f1.pack(pady=20)
    
        stu_reg=Label(f1,text="Register no :",font=self.myfont2,fg="black",bg="teal")
        stu_reg.grid(row=5,column=3,sticky=E,padx=20)
    
        self.reg_entry=Entry(f1,width="30")
        self.reg_entry.grid(row=5,column=4)
    
        stu_dept=Label(f1,text="Status :",font=self.myfont2,fg="black",bg="teal")
        stu_dept.grid(row=7,column=3,sticky=E,pady=10,padx=20)
            
        self.dept_entry=ttk.Combobox(f1,width="27")
        self.dept_entry['values']= ('Present','Absent')
        self.dept_entry.grid(row=7,column=4)
    
        f3=Frame(self.window3,bg="teal")
        f3.pack(pady=20)
    
        btn1=Button(f3,text="ADD",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.add_student_atd)
        btn1.grid(row=15,column=3,padx=5)
    
        btn2=Button(f3,text="Clear",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.clear)
        btn2.grid(row=15,column=5,padx=5)
    
        btn3=Button(f3,text="Delete",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.delete_student)
        btn3.grid(row=15,column=6,padx=5)
    
        btn5=Button(f3,text="Select",width=7,fg="white",bg="navy",activebackground="cyan",activeforeground="black",command=self.selectrecord)
        btn5.grid(row=15,column=7,padx=5)
    
        self.myTree2 = ttk.Treeview(self.window3)
    
        sb.config(command=self.myTree.yview)
        sb1.config(command=self.myTree.xview)
    
        self.myTree2['columns']=('ID','Regno','Date','Days_Present','Days_Absent','Percentage')
    
        self.myTree2.config(yscrollcommand=sb.set)
        self.myTree2.config(xscrollcommand=sb1.set)
    
        self.myTree2.column("#0",width=0,stretch=NO)
        self.myTree2.column("#1",width=0,stretch=NO)
        self.myTree2.column("#2",width=50)
        self.myTree2.column("#3",width=50)
        self.myTree2.column("#4",width=50)
        self.myTree2.column("#5",width=50)
        self.myTree2.column("#6",width=50)
    
        self.myTree2.heading("#0",text="")
        self.myTree2.heading("#1",text="ID")
        self.myTree2.heading("#2",text="Regno")
        self.myTree2.heading("#3",text="Date")
        self.myTree2.heading("#4",text="Days_Present")
        self.myTree2.heading("#5",text="Days_Absent")
        self.myTree2.heading("#6",text="Percentage")
    
        sb.pack(side=RIGHT,fill=Y)
        sb1.pack(side=BOTTOM,fill=X)
        self.myTree2.pack(fill=X,pady=15)

        self.view_students_atd()

    def back_atd(self):

        self.window3.destroy()
        STU_Entry()

    def add_student_atd(self):

        regno = self.reg_entry.get()
        status = self.dept_entry.get()
        date_today = date.today()

        ac.execute("SELECT *FROM attendance WHERE regno = ?", (regno,))
        record = ac.fetchone()

        if record:
            days_present = record[3]
            days_absent = record[4]

            if status == "Present":
                days_present += 1

            else:
                days_absent +=1

            total_days = days_present + days_absent
            percentage = (days_present / 90) * 100

            try:

                ac.execute("""UPDATE attendance SET date = ?, days_present = ?, days_absent = ?, percentage = ? WHERE regno = ?""", (date_today, days_present, days_absent, percentage, regno))
                acn.commit()
                messagebox.showinfo("Success", "Attendance updated successfully")
                self.view_students_atd()
                
            except:

                messagebox.showerror("Failed", "Try Again")

        else:

            if status == "Present":
                days_present = 1
                days_absent = 0

            else:
                days_present = 0
                days_absent = 1

            percentage = (days_present / 90) * 100

            try:
                
                ac.execute("""INSERT INTO attendance (regno,date, days_present, days_absent, percentage) VALUES (?, ?, ?, ?, ?)""", (regno, date_today, days_present, days_absent, percentage))
                acn. commit()
                messagebox.showinfo("Success", "Attendance updated successfully")
                self.view_students_atd()

            except:

                messagebox.showerror("Failed", "Try Again")
                
        self.reg_entry.delete(0,END)
        self.dept_entry.set('')
        
    def view_students_atd(self):

        for row in self.myTree2.get_children():

            self.myTree2.delete(row)
        
        with sqlite3.connect('student_management.db') as acn:
        
            ac=acn.cursor()

            for row in ac.execute('SELECT * FROM attendance ORDER BY regno ASC'):

                acn.commit()
                self.myTree2.insert('','end',values=row)

class Sign_Up:

    def __init__(self):

        self.signup_window=ctk.CTk()
        self.signup_window.geometry("500x500")
        self.signup_window.title("Signup")
        self.signup_window.resizable(height=False,width=False)

        MTASC_label = Label(self.signup_window,text="MTASC",font=font_MTASC)
        MTASC_label.place(x=180,y=20)

        Sname_Label =ctk.CTkLabel(self.signup_window,text="Name",font=("Times New Roman",16))
        Sname_Label.place(x=100,y=100)

        self.Sname_Entry = ctk.CTkEntry(self.signup_window, width=200, height=30, corner_radius=10)
        self.Sname_Entry.place(x=150, y=100)

        Sgender_Label = ctk.CTkLabel(self.signup_window,text="Gender",font=("Times New Roman",16))
        Sgender_Label.place(x=100,y=150)

        self.Sgender_Entry=ctk.CTkComboBox(self.signup_window,width=200,height=30,corner_radius=10,values=["Male","Female","Others"])
        self.Sgender_Entry.place(x=150,y=150)

        Snum_Label = ctk.CTkLabel(self.signup_window,text="Mobile",font=("Times New Roman",16))
        Snum_Label.place(x=100,y=200)

        self.Snum_Entry = ctk.CTkEntry(self.signup_window, width=200, height=30, corner_radius=10)
        self.Snum_Entry.place(x=150, y=200)

        SUname_Label = ctk.CTkLabel(self.signup_window,text="Username",font=("Times New Roman",16))
        SUname_Label.place(x=100,y=250)

        self.SUname_Entry = ctk.CTkEntry(self.signup_window, width=185, height=30, corner_radius=10)
        self.SUname_Entry.place(x=165, y=250)

        Spass_Label = ctk.CTkLabel(self.signup_window,text="Password",font=("Times New Roman",16))
        Spass_Label.place(x=100,y=300)

        self.Spass_Entry = ctk.CTkEntry(self.signup_window, width=185, height=30, corner_radius=10)
        self.Spass_Entry.place(x=165, y=300)

        Role_Label = ctk.CTkLabel(self.signup_window,text="Role",font=("Times New Roman",16))
        Role_Label.place(x=100,y=350)

        self.Role_Entry=ctk.CTkComboBox(self.signup_window,width=200,height=30,corner_radius=10,values=["Admin","Staff"])
        self.Role_Entry.place(x=150,y=350)

        signup_button = ctk.CTkButton(self.signup_window,text="Create",font=("Ariel",16,"bold"),fg_color="transparent",hover_color="teal",text_color="blue",width=100, height=40, corner_radius=20,command=self.Create_Account)
        signup_button.place(x=200,y=400)

        self.signup_window.mainloop()

    def Create_Account(self):

        Name = self.Sname_Entry.get()
        Gender = self.Sgender_Entry.get()
        Mobile = self.Snum_Entry.get()
        Username = self.SUname_Entry.get()
        Password = self.Spass_Entry.get()
        Role = self.Role_Entry.get()

        if Name and Gender and Mobile and Username and Password and Role:

            try:
                with sqlite3.connect('student_management.db')as lcn:
                    
                    lc = lcn.cursor()
                    lc.execute('INSERT INTO login(name,Gender,Mobile,uname,password,role)VALUES(?,?,?,?,?,?)',(Name,Gender,Mobile,Username,Password,Role))
                    lcn.commit()

                    messagebox.showinfo('Success','Account Created Succesfully')

                    #login()

                    self.signup_window.destroy()

            except:

                messagebox.showwarning('Input Error','Username already exists')
        
        else:

            messagebox.showwarning('Input Error','please fill out all fields')


class LOGIN:

    def __init__(self):

        self.login_window = ctk.CTk()
        self.login_window.geometry("500x500")
        self.login_window.title("LOGIN")
        self.login_window.resizable(height=False,width=False)
    
        LOGIN_label=ctk.CTkLabel(self.login_window,text="LOGIN",font=font_MTASC)
        LOGIN_label.place(x=220,y=20)

        User_Label = ctk.CTkLabel(self.login_window,text="USERNAME",bg_color="transparent")
        User_Label.place(x=97,y=105)

        self.User_Entry = ctk.CTkEntry(self.login_window, width=200, height=40, corner_radius=20)
        self.User_Entry.place(x=170, y=100)

        Pass_Label = ctk.CTkLabel(self.login_window,text="PASSWORD",bg_color="transparent")
        Pass_Label.place(x=97,y=166)

        self.Pass_Entry = ctk.CTkEntry(self.login_window, width=200, height=40, corner_radius=20)
        self.Pass_Entry.place(x=170, y=160)

        login_button = ctk.CTkButton(self.login_window,text="LOGIN",fg_color="transparent",hover_color="teal",text_color="blue",width=100, height=40, corner_radius=20,command=self.Check_User)
        login_button.place(x=210,y=225)

        signup_label = ctk.CTkLabel(self.login_window,text="Don't have an account?",bg_color="transparent")
        signup_label.place(x=150,y=280)

        signup_button = ctk.CTkButton(self.login_window,text="signup",font=font_underlined,fg_color="transparent",hover_color="teal",text_color="blue",width=10, height=5, corner_radius=20,command=Sign_Up)
        signup_button.place(x=280,y=282)

        self.login_window.mainloop()

    def Check_User(self):
    
        user = self.User_Entry.get()
        password = self.Pass_Entry.get()

        if user and password:
   
            lc.execute('SELECT password FROM login WHERE uname=?',(user,))
            Pass = lc.fetchone()
            print(Pass[0])
            lc.execute('SELECT role FROM login WHERE uname=?',(user,))
            Role = lc.fetchone()
            print(Role[0])
            try:
                
                if Pass[0] == password:

                    if Role[0] == "Staff":

                        try:
                        
                            STU_Entry()
                            
                        except:
                            pass
                        

                    elif Role[0] == "Admin":

                        try:
                        
                            DASHBOARD()
                            
                        except:
                            pass
                        
                else:

                    messagebox.showerror('Input Error','Password is incorrect')
            except:

                messagebox.showerror('Input Error','Username doesnot exists')
                
    def Destroy():
        
        self.login_window.destroy()

LOGIN()
#mainwindow.mainloop()
lcn.close()
conn.close()
