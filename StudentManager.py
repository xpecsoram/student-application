#import 
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk

#for save as dialog
from tkinter.filedialog import asksaveasfile

# importing the csv module
import csv
## Connecting to the database

## importing 'mysql.connector' for connection to mysql database


import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error


## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'password'
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="")
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)  # "buffered=True".makes db_cursor.row_count return actual number of records selected otherwise would return -1


#class is used to handle student info
class StudentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")
        
        #set all lables 
        self.lblTitle = tk.Label(self, text="Manage Students", font=("Helvetica", 16), bg="yellow", fg="green")
        self.lblFName = tk.Label(self, text="Enter FirstName:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblLName = tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblMajor = tk.Label(self, text="Enter Major:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblAge = tk.Label(self, text="Enter Age:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblWorking = tk.Label(self, text="Working:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblNative = tk.Label(self, text="Native English Speaking:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSelect = tk.Label(self, text="Please select one record below to update or delete", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSearch = tk.Label(self, text="Please Enter Roll No:",font=("Helvetica", 10), bg="blue", fg="yellow")
        
        #set all entity fields
        self.entFName = tk.Entry(self)
        self.entLName = tk.Entry(self)
        self.entMajor = tk.Entry(self)
        self.entAge = tk.Entry(self)
        self.entWorking = tk.Entry(self)
        self.calNative = tk.Entry(self)
        self.entSearch = tk.Entry(self)

        #set buttons
        self.btn_student = tk.Button(self, text="Students", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_student)
        self.btn_courses = tk.Button(self, text="Courses", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_course)
        self.btn_enroll = tk.Button(self, text="Enroll", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_enroll)
        self.btn_csv = tk.Button(self, text="Export Student CSV", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=student_csv)
        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.register_student)
        self.btn_update = tk.Button(self,text="Update",font=("Helvetica",11),bg="yellow", fg="blue",command=self.update_student_data)
        self.btn_delete = tk.Button(self, text="Delete", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.delete_student_data)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.clear_form)
        self.btn_show_all = tk.Button(self, text="Show All", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.load_student_data)
        self.btn_search = tk.Button(self, text="Search", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.show_search_record)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)
        
        #set access table columns and rows
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
        self.tvStudent= ttk.Treeview(self,show="headings",height="5", columns=columns)
        self.tvStudent.heading('#1', text='RollNo', anchor='center')
        self.tvStudent.column('#1', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#2', text='FirstName', anchor='center')
        self.tvStudent.column('#2', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#3', text='LastName', anchor='center')
        self.tvStudent.column('#3',width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#4', text='Major', anchor='center')
        self.tvStudent.column('#4',width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#5', text='Age', anchor='center')
        self.tvStudent.column('#5',width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#6', text='Working', anchor='center')
        self.tvStudent.column('#6', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#7', text='Native Language', anchor='center')
        self.tvStudent.column('#7', width=10, anchor='center', stretch=True)

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvStudent.yview)
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)
        self.tvStudent.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvStudent.xview)
        hsb.place(x=40 , y=310+200+1, width=620 + 20)
        self.tvStudent.configure(xscroll=hsb.set)
        self.tvStudent.bind("<<TreeviewSelect>>", self.show_selected_record)
        
        # set label places and entity places
        self.lblTitle.place(x=280, y=30,  height=27, width=300)
        self.lblFName.place(x=175, y=70,  height=23, width=100)
        self.lblLName.place(x=175, y=100,  height=23, width=100)
        self.lblMajor.place(x=171, y=129,  height=23, width=104)
        self.lblAge.place(x=210, y=158,  height=23, width=65)
        self.lblWorking.place(x=205, y=187,  height=23, width=71)
        self.lblNative.place(x=128, y=217, height=23, width=148)
        self.lblSelect.place(x=150, y=280, height=23, width=400)
        self.lblSearch.place(x=174, y=560, height=23, width=134)

        self.entFName.place(x=277, y=72, height=21, width=186)
        self.entLName.place(x=277, y=100, height=21, width=186)
        self.entMajor.place(x=277, y=129, height=21, width=186)
        self.entAge.place(x=277, y=158, height=21, width=186)
        self.entWorking.place(x=278, y=188, height=21, width=186)
        self.calNative.place(x=278, y=218, height=21, width=186)
        
        #set all buttons and search box places
        self.entSearch.place(x=310, y=560, height=21, width=186)
        self.btn_register.place(x=290, y=245, height=25, width=76)
        self.btn_student.place(x=10, y=45, height=25, width=76)
        self.btn_courses.place(x=10, y=75, height=25, width=76)
        self.btn_enroll.place(x=10, y=105, height=25, width=76)
        self.btn_csv.place(x=10, y=135, height=25, width=150)
        self.btn_update.place(x=370, y=245, height=25, width=76)
        self.btn_delete.place(x=460, y=245, height=25, width=76)
        self.btn_clear.place(x=548, y=245, height=25, width=76)
        self.btn_show_all.place(x=630, y=245, height=25, width=76)
        self.btn_search.place(x=498, y=558, height=26, width=60)
        self.btn_exit.place(x=320, y=610,  height=31, width=60)
        self.tvStudent.place(x=40, y=310, height=200, width=640)
        self.create_table()
        self.load_student_data()

    #set clear method that is used to clear all entity fields
    def clear_form(self):
      self.entFName.delete(0, tk.END)
      self.entLName.delete(0, tk.END)
      self.entMajor.delete(0, tk.END)
      self.entAge.delete(0, tk.END)
      self.entWorking.delete(0, tk.END)
      self.calNative.delete(0, tk.END)


  #method is used to exit 
    def exit(self):
      MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
      if MsgBox == 'yes':
        self.destroy()
    #method is used to delete row from db and also from frontend
    def delete_student_data(self):
      MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected student record', icon='warning')
      if MsgBox == 'yes':
          if db_connection.is_connected() == False:
              db_connection.connect()
          db_cursor.execute("use Student")  # Interact with Student Database
          # deleteing selected student record
          Delete = "delete from student_master where RollNo='%s'" % (roll_no)
          db_cursor.execute(Delete)
          db_connection.commit()
          mb.showinfo("Information", "Student Record Deleted Succssfully")
          self.load_student_data()
          self.entFName.delete(0, tk.END)
          self.entLName.delete(0, tk.END)
          self.entMajor .delete(0, tk.END)
          self.entAge.delete(0, tk.END)
          self.entWorking.delete(0, tk.END)
          self.calNative.delete(0, tk.END)



    #method is used to create table if table is not exist.
    def create_table(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        # executing cursor with execute method and pass SQL query
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Student")  # Create a Database Named Student
        db_cursor.execute("use Student")  # Interact with Student Database
        # creating required tables
        db_cursor.execute("create table if not exists Student_master(Id INT(10) NOT NULL  PRIMARY KEY AUTO_INCREMENT,rollno INT(15),fname VARCHAR(30),lname VARCHAR(30),major VARCHAR(20),age VARCHAR(30),working VARCHAR(100),native VARCHAR(30))AUTO_INCREMENT=1")
        db_connection.commit()
#method is used to insert data into database table and also show on frontend table view
    def register_student(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        fname = self.entFName.get()  # Retrieving entered first name
        lname = self.entLName.get()  # Retrieving entered last name
        major = self.entMajor.get()  # Retrieving entered major number
        age = self.entAge.get()  # Retrieving entered age name
        working = self.entWorking.get()  # Retrieving entered working 
        native = self.calNative.get()  # Retrieving choosen Native language
        # validating Entry Widgets
        if fname == "":
            mb.showinfo('Information', "Please Enter Firstname")
            self.entFName.focus_set()
            return
        if lname == "":
            mb.showinfo('Information', "Please Enter Lastname")
            self.entLName.focus_set()
            return

        if major == "":
            mb.showinfo('Information', "Please Enter Major")
            self.entMajor.focus_set()
            return
        if age == "":
            mb.showinfo('Information', "Please Enter Age")
            self.entAge.focus_set()
            return
        if working == "":
            mb.showinfo('Information', "Please Enter Working")
            self.entWorking.focus_set()
            return
        if native == "":
            mb.showinfo('Information', "Please Enter Native")
            self.calNative.focus_set()
            return


        # Inserting record into student_master table of student database
        try:
            rollno =int(self.fetch_max_roll_no())
            print("New Student Id: " + str(rollno))
            query2 = "INSERT INTO student_master (rollno, fname,lname,major,age,working,native) VALUES (%s, %s,%s, %s,%s, %s, %s)"
            # implement query Sentence
            db_cursor.execute(query2, (rollno, fname, lname,major, age, working,native))
            mb.showinfo('Information', "Student Registration Successfully")
            # Submit to database for execution
            db_connection.commit()
            self.load_student_data()
        except mysql.connector.Error as err:
            print(err)
            # Rollback in case there is any error
            db_connection.rollback()
            mb.showinfo('Information', "Data insertion failed!!!")
        finally:
           db_connection.close()

    def fetch_max_roll_no(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use Student")  # Interact with Student Database
        rollno  = 0
        query1 = "SELECT rollno FROM student_master order by  id DESC LIMIT 1"
        # implement query Sentence
        db_cursor.execute(query1)  # Retrieving maximum student id no
        print("No of Record Fetched:" + str(db_cursor.rowcount))
        if db_cursor.rowcount == 0:
            rollno = 1
        else:
            rows = db_cursor.fetchall()
            for row in rows:
                rollno = row[0]
            rollno = rollno + 1
        print("Max Student Id: " + str(rollno))
        return rollno
#method is used to search using id
    def show_search_record(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        s_roll_no = self.entSearch.get()  # Retrieving entered first name
        print(s_roll_no)
        if  s_roll_no == "":
            mb.showinfo('Information', "Please Enter Student Roll")
            self.entSearch.focus_set()
            return
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT rollno,fname,lname,major,age,working,native FROM student_master where rollno='" + s_roll_no + "'"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        RollNo = ""
        First_Name = ""
        Last_Name = ""
        Major = ""
        Age = ""
        Working = ""
        Native =""
        for row in rows:
            RollNo = row[0]
            First_Name = row[1]
            Last_Name = row[2]
            Major = row[3]
            Age = row[4]
            Working = row[5]
            Native = row[6]
            
            self.tvStudent.insert("", 'end', text=RollNo, values=(RollNo, First_Name, Last_Name, Major, Age, Working,Native))

#method is used to fill entity with specific row
    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.tvStudent.selection():
            item = self.tvStudent.item(selection)
        global roll_no
        roll_no,first_name,last_name,major,age,working,native = item["values"][0:7]
        self.entFName.insert(0, first_name)
        self.entLName.insert(0, last_name)
        self.entAge.insert(0, age)
        self.entWorking .insert(0, working)
        self.entMajor.insert(0, major)
        self.calNative.insert(0, native)
        return roll_no
#method is used to update record 
    def update_student_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        print("Updating")
        db_cursor.execute("use Student")  # Interact with Student Database
        First_Name = self.entFName.get()
        Last_Name = self.entLName.get()
        Major = self.entMajor.get()
        Age = self.entAge.get()
        Working = self.entWorking.get()
        Native = self.calNative.get()
        
        Update = "Update student_master set fname='%s', lname='%s', major='%s', age='%s', working='%s',native='%s' where rollno='%s'" % (
        First_Name, Last_Name, Major, Age,Working,Native, roll_no)
        db_cursor.execute(Update)
        db_connection.commit()
        mb.showinfo("Info", "Selected Student Record Updated Successfully ")
        self.load_student_data()

    def load_student_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
       # self.calNative.delete(0, tk.END)#clears the date entry widget
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT rollno,fname,lname,major,age,working,native FROM student_master"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        RollNo = ""
        First_Name = ""
        Last_Name = ""
        Major = ""
        Age = ""
        Working = ""
        Native =""
        for row in rows:
            RollNo = row[0]
            First_Name = row[1]
            Last_Name = row[2]
            Major = row[3]
            Age = row[4]
            Working = row[5]
            Native = row[6]
            self.tvStudent.insert("", 'end', text=RollNo, values=(RollNo, First_Name, Last_Name, Major, Age, Working,Native))
###################end of student class ##############






####Below class is used to handle courses######
###############################################

#class is used to handle course info
class CourseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")
        
        #set all lables 
        self.lblTitle = tk.Label(self, text="Manage Courses", font=("Helvetica", 16), bg="yellow", fg="green")
        self.lbltitle = tk.Label(self, text="Title:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblLiberal = tk.Label(self, text="Liberal Studies:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblCredit = tk.Label(self, text="Credits:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSelect = tk.Label(self, text="Please select one record below to update or delete", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSearch = tk.Label(self, text="Please Enter ID:",font=("Helvetica", 10), bg="blue", fg="yellow")
        
        #set all entity fields
        self.enttitle = tk.Entry(self)
        self.entLiberal = tk.Entry(self)
        self.entCredit = tk.Entry(self)
        self.entSearch = tk.Entry(self)
        
        #set buttons
        self.btn_student = tk.Button(self, text="Students", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_student)
        self.btn_courses = tk.Button(self, text="Courses", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_course)
        self.btn_enroll = tk.Button(self, text="Enroll", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_enroll)
        self.btn_csv = tk.Button(self, text="Export Student CSV", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=course_csv)
        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.register_course)
        self.btn_update = tk.Button(self,text="Update",font=("Helvetica",11),bg="yellow", fg="blue",command=self.update_student_data)
        self.btn_delete = tk.Button(self, text="Delete", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.delete_course_data)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.clear_form)
        self.btn_show_all = tk.Button(self, text="Show All", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.load_course_data)
        self.btn_search = tk.Button(self, text="Search", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.show_course_search_record)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)
        
        #set access table columns and rows
        columns = ("#1", "#2", "#3", "#4")
        self.tvStudent= ttk.Treeview(self,show="headings",height="5", columns=columns)
        self.tvStudent.heading('#1', text='ID', anchor='center')
        self.tvStudent.column('#1', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#2', text='Tittle', anchor='center')
        self.tvStudent.column('#2', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#3', text='Liberal Studied', anchor='center')
        self.tvStudent.column('#3',width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#4', text='Credit', anchor='center')
        self.tvStudent.column('#4',width=10, anchor='center', stretch=True)

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvStudent.yview)
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)
        self.tvStudent.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvStudent.xview)
        hsb.place(x=40 , y=310+200+1, width=620 + 20)
        self.tvStudent.configure(xscroll=hsb.set)
        self.tvStudent.bind("<<TreeviewSelect>>", self.show_selected_record)
        
        # set label places and entity places
        self.lblTitle.place(x=280, y=30,  height=27, width=300)
        self.lbltitle.place(x=175, y=70,  height=23, width=100)
        self.lblLiberal.place(x=175, y=100,  height=23, width=100)
        self.lblCredit.place(x=171, y=129,  height=23, width=104)

        self.lblSelect.place(x=150, y=280, height=23, width=400)
        self.lblSearch.place(x=174, y=560, height=23, width=134)

        self.enttitle.place(x=277, y=72, height=21, width=186)
        self.entLiberal.place(x=277, y=100, height=21, width=186)
        self.entCredit.place(x=277, y=129, height=21, width=186)

        #set all buttons and search box places
        self.entSearch.place(x=310, y=560, height=21, width=186)
        self.btn_register.place(x=290, y=245, height=25, width=76)
        self.btn_student.place(x=10, y=45, height=25, width=76)
        self.btn_courses.place(x=10, y=75, height=25, width=76)
        self.btn_enroll.place(x=10, y=105, height=25, width=76)
        self.btn_csv.place(x=10, y=135, height=25, width=150)
        self.btn_update.place(x=370, y=245, height=25, width=76)
        self.btn_delete.place(x=460, y=245, height=25, width=76)
        self.btn_clear.place(x=548, y=245, height=25, width=76)
        self.btn_show_all.place(x=630, y=245, height=25, width=76)
        self.btn_search.place(x=498, y=558, height=26, width=60)
        self.btn_exit.place(x=320, y=610,  height=31, width=60)
        self.tvStudent.place(x=40, y=310, height=200, width=640)
        self.create_table()
        self.load_course_data()

    #set clear method that is used to clear all entity fields
    def clear_form(self):
      self.enttitle.delete(0, tk.END)
      self.entLiberal.delete(0, tk.END)
      self.entCredit.delete(0, tk.END)


  #method is used to exit 
    def exit(self):
      MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
      if MsgBox == 'yes':
        self.destroy()
    #method is used to delete row from db and also from frontend
    def delete_course_data(self):
      MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected student record', icon='warning')
      if MsgBox == 'yes':
          if db_connection.is_connected() == False:
              db_connection.connect()
          db_cursor.execute("use Student")  # Interact with Student Database
          # deleteing selected student record
          Delete = "delete from courses where id='%s'" % (id)
          db_cursor.execute(Delete)
          db_connection.commit()
          mb.showinfo("Information", "Course Record Deleted Succssfully")
          self.load_course_data()
          self.enttitle.delete(0, tk.END)
          self.entLiberal.delete(0, tk.END)
          self.entCredit.delete(0, tk.END)



    #method is used to create table if table is not exist.
    def create_table(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        # executing cursor with execute method and pass SQL query
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Student")  # Create a Database Named Student
        db_cursor.execute("use Student")  # Interact with Student Database
        # creating required tables
        db_cursor.execute("create table if not exists courses(Id INT(11) NOT NULL  PRIMARY KEY AUTO_INCREMENT,title VARCHAR(30),liberal VARCHAR(30),credit INT(11))AUTO_INCREMENT=1")
        db_connection.commit()
#method is used to insert data into database table and also show on frontend table view
    def register_course(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        title = self.enttitle.get()  # Retrieving entered first name
        Liberal = self.entLiberal.get()  # Retrieving entered last name
        Credit = self.entCredit.get()  # Retrieving entered major number
        # validating Entry Widgets
        if title == "":
            mb.showinfo('Information', "Please Enter Title")
            self.enttitle.focus_set()
            return
        if Liberal == "":
            mb.showinfo('Information', "Please Select Liberal Studied")
            self.entLiberal.focus_set()
            return

        if Credit == "":
            mb.showinfo('Information', "Please Enter Credit")
            self.entCredit.focus_set()
            return
        
        # Inserting record into student_master table of student database
        try:
            id =int(self.fetch_max_id())
            print("New Student Id: " + str(id))
            query2 = "INSERT INTO courses (title,liberal,credit) VALUES (%s, %s,%s)"
            # implement query Sentence
            db_cursor.execute(query2, (title, Liberal,Credit))
            mb.showinfo('Information', "Course Registration Successfully")
            # Submit to database for execution
            db_connection.commit()
            self.load_course_data()
        except mysql.connector.Error as err:
            print(err)
            # Rollback in case there is any error
            db_connection.rollback()
            mb.showinfo('Information', "Data insertion failed!!!")
        finally:
           db_connection.close()

    def fetch_max_id(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use Student")  # Interact with Student Database
        id  = 0
        query1 = "SELECT id FROM courses order by  id DESC LIMIT 1"
        # implement query Sentence
        db_cursor.execute(query1)  # Retrieving maximum student id no
        print("No of Record Fetched:" + str(db_cursor.rowcount))
        if db_cursor.rowcount == 0:
            id = 1
        else:
            rows = db_cursor.fetchall()
            for row in rows:
                id = row[0]
            id = id + 1
        print("Max Student Id: " + str(id))
        return id
#method is used to search using id
    def show_course_search_record(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        s_id = self.entSearch.get()  # Retrieving entered first name
        print(s_id)
        if  s_id == "":
            mb.showinfo('Information', "Please Enter Student ID")
            self.entSearch.focus_set()
            return
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT id,title,liberal,credit FROM courses where id='" + s_id + "'"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        ID = ""
        title = ""
        Liberal = ""
        Credit = ""

        for row in rows:
            ID = row[0]
            title = row[1]
            Liberal = row[2]
            Credit = row[3]
           
            self.tvStudent.insert("", 'end', text=ID, values=(ID, title,Liberal, Credit))

#method is used to fill entity with specific row
    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.tvStudent.selection():
            item = self.tvStudent.item(selection)
        global id
        id,title,Liberal,Credit = item["values"][0:4]
        self.enttitle.insert(0, title)
        self.entLiberal.insert(0, Liberal)
        self.entCredit.insert(0, Credit)
        return id
#method is used to update record 
    def update_student_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        print("Updating")
        db_cursor.execute("use Student")  # Interact with Student Database
        title = self.enttitle.get()
        Liberal = self.entLiberal.get()
        Credit = self.entCredit.get()
        
        Update = "Update courses set title='%s', liberal='%s', credit='%s'where id='%s'" % (
        title,Liberal, Credit,id)
        db_cursor.execute(Update)
        db_connection.commit()
        mb.showinfo("Info", "Selected Student Record Updated Successfully ")
        self.load_course_data()

    def load_course_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
       # self.calNative.delete(0, tk.END)#clears the date entry widget
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT id,title,liberal,credit FROM courses"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()
        id=""
        title = ""
        Liberal = ""
        Credit = ""

        for row in rows:
            id = row[0]
            title = row[1]
            Liberal = row[2]
            Credit = row[3]

            self.tvStudent.insert("", 'end', text=id, values=(id,title, Liberal, Credit))

################end of courses class##############




####Below class is used to handle enroll courses######
###############################################

#class is used to handle course info
class EnrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("1200x800")
        
        #set all lables 
        self.lblTitle = tk.Label(self, text="Manage Enrollment", font=("Helvetica", 16), bg="yellow", fg="green")
        self.lblstudent = tk.Label(self, text="Student:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblcourse = tk.Label(self, text="Course:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblgrade = tk.Label(self, text="Grade:", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSelect = tk.Label(self, text="Please select one record below to update or delete", font=("Helvetica", 10), bg="blue", fg="yellow")
        self.lblSearch = tk.Label(self, text="Please Enter ID:",font=("Helvetica", 10), bg="blue", fg="yellow")
        
        #set all entity fields
        self.entstudent = tk.Entry(self)
        self.entcourse = tk.Entry(self)
        self.entgrade = tk.Entry(self)
        self.entSearch = tk.Entry(self)
        
        #set buttons
        self.btn_student = tk.Button(self, text="Students", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_student)
        self.btn_courses = tk.Button(self, text="Courses", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_course)
        self.btn_enroll = tk.Button(self, text="Enroll", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=open_enroll)
        self.btn_csv = tk.Button(self, text="Export Student CSV", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=enroll_csv)
        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="yellow", fg="blue",
                                      command=self.register_enroll)
        self.btn_update = tk.Button(self,text="Update",font=("Helvetica",11),bg="yellow", fg="blue",command=self.update_enroll_data)
        self.btn_delete = tk.Button(self, text="Delete", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.delete_enroll_data)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="yellow", fg="blue",
                                    command=self.clear_form)
        self.btn_show_all = tk.Button(self, text="Show All", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.load_enroll_data)
        self.btn_search = tk.Button(self, text="Search", font=("Helvetica", 11), bg="yellow", fg="blue",
                                   command=self.show_enroll_search_record)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)
        
        #set access table columns and rows
        columns = ("#1", "#2", "#3", "#4")
        self.tvStudent= ttk.Treeview(self,show="headings",height="5", columns=columns)
        self.tvStudent.heading('#1', text='ID', anchor='center')
        self.tvStudent.column('#1', width=60, anchor='center', stretch=False)
        self.tvStudent.heading('#2', text='Student', anchor='center')
        self.tvStudent.column('#2', width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#3', text='Course', anchor='center')
        self.tvStudent.column('#3',width=10, anchor='center', stretch=True)
        self.tvStudent.heading('#4', text='Grade', anchor='center')
        self.tvStudent.column('#4',width=10, anchor='center', stretch=True)

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvStudent.yview)
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)
        self.tvStudent.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvStudent.xview)
        hsb.place(x=40 , y=310+200+1, width=620 + 20)
        self.tvStudent.configure(xscroll=hsb.set)
        self.tvStudent.bind("<<TreeviewSelect>>", self.show_selected_record)
        
        # set label places and entity places
        self.lblTitle.place(x=280, y=30,  height=27, width=300)
        self.lblstudent.place(x=175, y=70,  height=23, width=100)
        self.lblcourse.place(x=175, y=100,  height=23, width=100)
        self.lblgrade.place(x=171, y=129,  height=23, width=104)

        self.lblSelect.place(x=150, y=280, height=23, width=400)
        self.lblSearch.place(x=174, y=560, height=23, width=134)

        self.entstudent.place(x=277, y=72, height=21, width=186)
        self.entcourse.place(x=277, y=100, height=21, width=186)
        self.entgrade.place(x=277, y=129, height=21, width=186)

        #set all buttons and search box places
        self.entSearch.place(x=310, y=560, height=21, width=186)
        self.btn_register.place(x=290, y=245, height=25, width=76)
        self.btn_student.place(x=10, y=45, height=25, width=76)
        self.btn_courses.place(x=10, y=75, height=25, width=76)
        self.btn_enroll.place(x=10, y=105, height=25, width=76)
        self.btn_csv.place(x=10, y=135, height=25, width=150)
        self.btn_update.place(x=370, y=245, height=25, width=76)
        self.btn_delete.place(x=460, y=245, height=25, width=76)
        self.btn_clear.place(x=548, y=245, height=25, width=76)
        self.btn_show_all.place(x=630, y=245, height=25, width=76)
        self.btn_search.place(x=498, y=558, height=26, width=60)
        self.btn_exit.place(x=320, y=610,  height=31, width=60)
        self.tvStudent.place(x=40, y=310, height=200, width=640)
        self.create_table()
        self.load_enroll_data()

    #set clear method that is used to clear all entity fields
    def clear_form(self):
      self.entstudent.delete(0, tk.END)
      self.entcourse.delete(0, tk.END)
      self.entgrade.delete(0, tk.END)


  #method is used to exit 
    def exit(self):
      MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
      if MsgBox == 'yes':
        self.destroy()
    #method is used to delete row from db and also from frontend
    def delete_enroll_data(self):
      MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected student record', icon='warning')
      if MsgBox == 'yes':
          if db_connection.is_connected() == False:
              db_connection.connect()
          db_cursor.execute("use Student")  # Interact with Student Database
          # deleteing selected student record
          Delete = "delete from enroll where id='%s'" % (id)
          db_cursor.execute(Delete)
          db_connection.commit()
          mb.showinfo("Information", "Course Record Deleted Succssfully")
          self.load_enroll_data()
          self.entstudent.delete(0, tk.END)
          self.entcourse.delete(0, tk.END)
          self.entgrade.delete(0, tk.END)



    #method is used to create table if table is not exist.
    def create_table(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        # executing cursor with execute method and pass SQL query
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS Student")  # Create a Database Named Student
        db_cursor.execute("use Student")  # Interact with Student Database
        # creating required tables
        db_cursor.execute("create table if not exists enroll(Id INT(11) NOT NULL  PRIMARY KEY AUTO_INCREMENT,student VARCHAR(100),course VARCHAR(100),grade VARCHAR(100))AUTO_INCREMENT=1")
        db_connection.commit()
#method is used to insert data into database table and also show on frontend table view
    def register_enroll(self):
        if db_connection.is_connected() == False:
          db_connection.connect()
        student = self.entstudent.get()  # Retrieving entered first name
        course = self.entcourse.get()  # Retrieving entered last name
        grade = self.entgrade.get()  # Retrieving entered major number
        # validating Entry Widgets
        if student == "":
            mb.showinfo('Information', "Please Select Student")
            self.entstudent.focus_set()
            return
        if course == "":
            mb.showinfo('Information', "Please Select Course")
            self.entcourse.focus_set()
            return

        if grade == "":
            mb.showinfo('Information', "Please Enter grade")
            self.entgrade.focus_set()
            return
        
        # Inserting record into student_master table of student database
        try:
            id =int(self.fetch_max_id())
            print("New Student Id: " + str(id))
            query2 = "INSERT INTO enroll (student,course,grade) VALUES (%s, %s,%s)"
            # implement query Sentence
            db_cursor.execute(query2, (student, course,grade))
            mb.showinfo('Information', "Enroll Successfully")
            # Submit to database for execution
            db_connection.commit()
            self.load_enroll_data()
        except mysql.connector.Error as err:
            print(err)
            # Rollback in case there is any error
            db_connection.rollback()
            mb.showinfo('Information', "Data insertion failed!!!")
        finally:
           db_connection.close()

    def fetch_max_id(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use Student")  # Interact with Student Database
        id  = 0
        query1 = "SELECT id FROM enroll order by  id DESC LIMIT 1"
        # implement query Sentence
        db_cursor.execute(query1)  # Retrieving maximum student id no
        print("No of Record Fetched:" + str(db_cursor.rowcount))
        if db_cursor.rowcount == 0:
            id = 1
        else:
            rows = db_cursor.fetchall()
            for row in rows:
                id = row[0]
            id = id + 1
        print("Max Enroll Id: " + str(id))
        return id
#method is used to search using id
    def show_enroll_search_record(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        s_id = self.entSearch.get()  # Retrieving entered first name
        print(s_id)
        if  s_id == "":
            mb.showinfo('Information', "Please Enter Student ID")
            self.entSearch.focus_set()
            return
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT id,student,course,grade FROM enroll where id='" + s_id + "'"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()

        ID = ""
        student = ""
        course = ""
        grade = ""

        for row in rows:
            ID = row[0]
            student = row[1]
            course = row[2]
            grade = row[3]
           
            self.tvStudent.insert("", 'end', text=ID, values=(ID, student,course,grade))

#method is used to fill entity with specific row
    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.tvStudent.selection():
            item = self.tvStudent.item(selection)
        global id
        id,student,course,grade = item["values"][0:4]
        self.entstudent.insert(0, student)
        self.entcourse.insert(0, course)
        self.entgrade.insert(0, grade)
        return id
#method is used to update record 
    def update_enroll_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        print("Updating")
        db_cursor.execute("use Student")  # Interact with Student Database
        student = self.entstudent.get()
        course = self.entcourse.get()
        grade = self.entgrade.get()
        
        Update = "Update enroll set student='%s',course='%s', grade='%s'where id='%s'" % (student,course, grade,id)
        db_cursor.execute(Update)
        db_connection.commit()
        mb.showinfo("Info", "Selected Enroll Updated Successfully ")
        self.load_enroll_data()

    def load_enroll_data(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
       # self.calNative.delete(0, tk.END)#clears the date entry widget
        self.tvStudent.delete(*self.tvStudent.get_children())  # clears the treeview tvStudent
        # Inserting record into student_master table of student database
        db_cursor.execute("use Student")  # Interact with Bank Database
        sql = "SELECT id,student,course,grade FROM enroll"
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
        print("Total Data Entries:" + str(total))
        rows = db_cursor.fetchall()
        id=""
        student = ""
        course = ""
        grade= ""

        for row in rows:
            id = row[0]
            student = row[1]
            course = row[2]
            grade = row[3]

            self.tvStudent.insert("", 'end', text=id, values=(id,student, course, grade))

################end of enroll courses class##############


#open student gui
def open_student():
    global app
    app.destroy();
    app= StudentApp()
#open course gui    
def open_course():
    global app
    app.destroy();
    app= CourseApp()
#open enroll gui
def open_enroll():
    global app
    app.destroy();
    app= EnrollApp()

#export student csv
def student_csv():
    # to open save as dialoge box
    files = [('All Files', '*.*'), 
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    file = asksaveasfile(filetypes = files, defaultextension = ".csv")
    fields = ['Roll NO', 'First Name', 'Last Name', 'Major','Age','Working','Native Language']
    if db_connection.is_connected() == False:
            db_connection.connect()
    db_cursor.execute("use Student")  # Interact with Bank Database
    sql = "SELECT rollno,fname,lname,major,age,working,native FROM student_master"
    db_cursor.execute(sql)
    total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
    print("Total Data Entries:" + str(total))
    rows = db_cursor.fetchall()
    # writing to csv file
    with file as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
      
        # writing the fields
        csvwriter.writerow(fields)
      
        # writing the data rows
        csvwriter.writerows(rows)
    

#export course csv
def course_csv():
    # to open save as dialoge box
    files = [('All Files', '*.*'), 
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    file = asksaveasfile(filetypes = files, defaultextension = ".csv")
    fields = ['ID', 'Title', 'Liberal Studied', 'Credit']
    if db_connection.is_connected() == False:
            db_connection.connect()
    db_cursor.execute("use Student")  # Interact with Bank Database
    sql = "SELECT id,title,liberal,credit FROM courses"
    db_cursor.execute(sql)
    total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
    print("Total Data Entries:" + str(total))
    rows = db_cursor.fetchall()
    # writing to csv file
    with file as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
      
        # writing the fields
        csvwriter.writerow(fields)
      
        # writing the data rows
        csvwriter.writerows(rows)
        
#export enroll csv
def enroll_csv():
    # to open save as dialoge box
    files = [('All Files', '*.*'), 
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    file = asksaveasfile(filetypes = files, defaultextension = ".csv")
    fields = ['ID', 'Student', 'Course', 'Grade']
    if db_connection.is_connected() == False:
            db_connection.connect()
    db_cursor.execute("use Student")  # Interact with Bank Database
    sql = "SELECT id,student,course,grade FROM enroll"
    db_cursor.execute(sql)
    total = db_cursor.rowcount
        #if total ==0:
            #mb.showinfo("Info", "Nothing To Display,Please add data")
            #return
    print("Total Data Entries:" + str(total))
    rows = db_cursor.fetchall()
    # writing to csv file
    with file as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
      
        # writing the fields
        csvwriter.writerow(fields)
      
        # writing the data rows
        csvwriter.writerows(rows)
if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()