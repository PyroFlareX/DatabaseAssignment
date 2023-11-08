import sqlite3
import csv

sqliteConnection = sqlite3.connect('students.db')
cursor = sqliteConnection.cursor()

class Student:
	def __init__(self):
		self.id = 0
		self.FirstName = ""
		self.LastName= ""
		self.GPA = 0.0
		self.Major = ""
		self.FacultyAdvisor = ""
		self.Address = ""
		self.City = ""
		self.State = ""
		self.ZipCode = ""
		self.MobilePhoneNumber =''
		self.isDeleted = 0

def createTable():
	cursor.execute("""CREATE TABLE Student(
	StudentId INTEGER PRIMARY KEY,
	FirstName TEXT,
	LastName TEXT,
	GPA REAL,
	Major TEXT,
	FacultyAdvisor TEXT,
	Address TEXT,
	City TEXT,
	State TEXT,
	ZipCode TEXT,
	MobilePhoneNumber TEXT,
	isDeleted INTEGER);""")
	sqliteConnection.commit()

def importCSV():
	with open("students.csv", newline='') as csvfile:
		freader = csv.reader(csvfile)
		i = 0
		for row in freader:
			s = Student()
			s.id = i
			s.FirstName = row[0]
			s.LastName = row[1]
			s.GPA = float(row[8])
			s.Major = row[7]
			s.FacultyAdvisor = "None!" # row[0]
			s.Address = row[2]
			s.City = row[3]
			s.State = row[4]
			s.ZipCode = row[5]
			s.MobilePhoneNumber = row[6]
			s.isDeleted = 0
			cursor.execute("INSERT INTO Student(StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
			(i, s.FirstName, s.LastName, s.GPA, s.Major, s.FacultyAdvisor, s.Address, s.City, s.State, s.ZipCode, s.MobilePhoneNumber, s.isDeleted))
			i += 1
		sqliteConnection.commit()

def displayAllStudents():
	students = cursor.execute("SELECT * FROM Student WHERE isDeleted = 0").fetchall()
	sqliteConnection.commit()
	for stu in students:
		print(stu)

def addNewStudent():
	s = Student()

	new_id = getDatabaseSize()
	#initialize this student
	s.id = new_id
	s.FirstName = input("Input the Student's First Name: ")
	s.LastName = input("Input the Student's Last Name: ")
	while True:
		GPA = input("Input the Student's GPA: ")
		try:
			s.GPA = float(GPA)
			break
		except ValueError:
			GPA = input("Input the Student's GPA: ")
			
	s.Major = input("Input the Student's Major: ")
	s.FacultyAdvisor = input("Input the Student's Faculty Advisor: ")
	s.Address = input("Input the Student's Address: ")
	s.City =  input("Input the Student's City: ")
	s.State = input("Input the Student's full State: ")
	s.ZipCode = input("Input the Student's Zip Code: ")
	s.MobilePhoneNumber = input("Input the Student's Phone Number: ")
	s.isDeleted = 0

	print("The information for the student you entered is: ")
	print(s.id, s.FirstName,s.LastName, s.GPA, s.Major, s.FacultyAdvisor, s.Address, s.City, s.State, s.ZipCode, s.MobilePhoneNumber, s.isDeleted)
	ans = input("Do you still want to add this student? (y/n): ")
	if ans != "y":
		return
	
	cursor.execute("INSERT INTO Student(StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", 
		(s.id, s.FirstName,s.LastName, s.GPA, s.Major, s.FacultyAdvisor, s.Address, s.City, s.State, s.ZipCode, s.MobilePhoneNumber, s.isDeleted))
	sqliteConnection.commit()

def updateStudent():
	student_id = -1
	while True:
		i = input("Please input a valid student id for the student to update: ")
		if(i.isnumeric()):
			if(int(i) >= 0 and int(i) < 101):
				student_id = int(i)
				break
			else:
				continue
		else:
			continue
	if not(student_id >= 0 and student_id < 101):
		print("Failed to get valid student id!")
		return

	fields = ["Major", "FacultyAdvisor", "MobilePhoneNumber"]

	field = " "
	while not (field in fields):
		field = input("Which field should be used? Major, FacultyAdvisor, or MobilePhoneNumber? : ")

	value_for_field = input("What value should the field be replaced by?: ")
	while True:
		ans = input("Are you sure? (y/n)")
		if(ans == "y"):
			break
		else:
			value_for_field = input("What value should the field be replaced by?: ")
			continue

	# Do the SQL stuff
	cursor.execute(
		f"UPDATE Student SET {field} = ? WHERE StudentId = ?",
		(value_for_field, student_id)
	)
	sqliteConnection.commit()

def deleteStudent():
	student_id = -1
	while True:
		i = input("Please input a valid student id for the student to update: ")
		if(i.isnumeric()):
			if(int(i) >= 0 and int(i) < 101):
				student_id = int(i)
				break
			else:
				continue
		else:
			continue
	if not(student_id >= 0 and student_id < getDatabaseSize()):
		print("Failed to get valid student id!")
		return
	
	cursor.execute(
		"UPDATE Student SET isDeleted = 1 WHERE StudentId = ?",
		(student_id,),
	)
	sqliteConnection.commit()

def searchBy():
	fields = ["Major", "GPA", "FacultyAdvisor", "City", "State"]

	field = " "
	while not (field in fields):
		field = input("Which field should be used? Major, FacultyAdvisor, GPA, City, or State? : ")

	value_for_field = input("What value should the field be searched by?: ")
	while True:
		ans = input("Are you sure? (y/n)")
		if(ans == "y"):
			break
		else:
			value_for_field = input("What value should the field be searched by?: ")

	query = f"SELECT * FROM Student WHERE {field} = ? AND isDeleted = 0"
	students = cursor.execute(query, (value_for_field)).fetchall()

	sqliteConnection.commit()
	for stu in students:
		print(stu)

def main_menu():
	while True:
		print("Menu Options:")
		print("\t1. Create Table")
		print("\t2. Import CSV")
		print("\t3. Display All Students")
		print("\t4. Add New Student")
		print("\t5. Update Student")
		print("\t6. Delete Student")
		print("\t7. Search by Category")
		print("\t8. Quit")

		valid = range(1,9)
		val = -1
		while not val in valid:
			val = input("Input a valid number in the menu to choose an option: ")
			if val.isnumeric():
				val = int(val)

		if val == 1:
			createTable()
		elif val == 2:
			importCSV()
		elif val == 3:
			displayAllStudents()
		elif val == 4:
			addNewStudent()
		elif val == 5:
			updateStudent()
		elif val == 6:
			deleteStudent()
		elif val == 7:
			searchBy()
		elif val == 8:
			print("Quiting")
			break
		else:
			print("Invalid Menu Option!")
			break

def getDatabaseSize():
	student_list = cursor.execute("SELECT * FROM Student").fetchall()
	sqliteConnection.commit()
	new_id = len(student_list)
	return new_id

main_menu()

sqliteConnection.commit()

# close the connection
sqliteConnection.close()