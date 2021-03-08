from PyQt5 import QtWidgets
import pyperclip
import sqlite3
import sys

class UserControlWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.UserTable()
        self.ControlUI()
    
    def UserTable(self):
        self.connection = sqlite3.connect("passwordDatabase.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS Users (UserName TEXT, Password TEXT)")
        self.connection.commit()

    def ControlUI(self):
        self.warning = QtWidgets.QLabel("")
        self.username = QtWidgets.QLineEdit()
        self.usernameString = QtWidgets.QLabel("Username")
        self.passwordString = QtWidgets.QLabel("Password")
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton = QtWidgets.QPushButton("Sign in")
        self.regButton = QtWidgets.QPushButton("Register")

        controlh_box = QtWidgets.QHBoxLayout()
        controlh_box.addWidget(self.usernameString)
        controlh_box.addStretch()
        controlh_box.addWidget(self.username)

        controlh_box2 = QtWidgets.QHBoxLayout()
        controlh_box2.addWidget(self.passwordString)
        controlh_box2.addStretch()
        controlh_box2.addWidget(self.password)

        controlh_box3 = QtWidgets.QHBoxLayout()
        controlh_box3.addStretch()
        controlh_box3.addWidget(self.warning)
        controlh_box3.addStretch()

        controlv_box = QtWidgets.QVBoxLayout()
        controlv_box.addLayout(controlh_box)
        controlv_box.addLayout(controlh_box2)
        controlv_box.addStretch()
        controlv_box.addLayout(controlh_box3)
        controlv_box.addWidget(self.loginButton)
        controlv_box.addWidget(self.regButton)

        self.setLayout(controlv_box)
        self.loginButton.clicked.connect(self.Login)
        self.regButton.clicked.connect(self.Register)
        self.setWindowTitle("Login")
        self.setMinimumHeight(150)
        self.setMaximumHeight(150)
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)

        self.show()
    
    def Login(self):
        isim = self.username.text()
        parola = self.password.text()

        self.cursor.execute("SELECT * FROM Users WHERE UserName = ? AND Password = ?",(isim,parola))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.warning.setText("Username or password is incorrect.")
        else:
            self.mainWindow = MainWindow(isim)
            self.warning.setText("Signed in successfully")
            self.mainWindow.resetSpaces()
            self.mainWindow.show()
            self.close()
    
    def Register(self):
        isim = self.username.text()
        parola = self.password.text()

        if isim == "" or parola == "":
            self.warning.setText("Name and Password fields cannot be left blank!")
            return False

        self.cursor.execute("SELECT * FROM Users WHERE UserName = ? AND Password = ?",(isim,parola))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.cursor.execute("INSERT INTO Users VALUES(?, ?)", (isim, parola))
            self.connection.commit()
            self.warning.setText("Registration Successful")
        else:
            self.warning.setText("Such a user already exists")

class MainWindow(QtWidgets.QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.init_ui()
    
    def start_connection(self,user):
        if user == None:
            print("User is not exists")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (Name TEXT, Password TEXT)")
            self.connection.commit()

    def init_ui(self):
        self.name = QtWidgets.QLineEdit()
        self.nameString = QtWidgets.QLabel("Name of the Program")

        self.passw = QtWidgets.QLineEdit()
        self.passwString = QtWidgets.QLabel("Password")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)

        self.answer = QtWidgets.QLabel("")
        self.savepass = QtWidgets.QPushButton("Save")
        self.allpassw = QtWidgets.QPushButton("My Passwords")
        self.generatorButton = QtWidgets.QPushButton("Generate Random Password")

        mainH_box2 = QtWidgets.QHBoxLayout()
        mainH_box2.addStretch()
        mainH_box2.addWidget(self.answer)
        mainH_box2.addStretch()

        mainV_box = QtWidgets.QVBoxLayout()
        mainV_box.addStretch()
        mainV_box.addWidget(self.nameString)
        mainV_box.addWidget(self.name)
        mainV_box.addWidget(self.passwString)
        mainV_box.addWidget(self.passw)
        mainV_box.addLayout(mainH_box2)
        mainV_box.addStretch()
        mainV_box.addWidget(self.savepass)
        mainV_box.addWidget(self.allpassw)
        mainV_box.addWidget(self.generatorButton)

        mainH_box = QtWidgets.QHBoxLayout()
        mainH_box.addLayout(mainV_box)

        self.setLayout(mainH_box)

        self.savepass.clicked.connect(self.addPassword)
        self.allpassw.clicked.connect(self.allPasswords)
        self.generatorButton.clicked.connect(self.passwordGenerator)

        self.setWindowTitle("Main Window")
        self.setMinimumHeight(230)
        self.setMaximumHeight(230)
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)
    
    def passwordGenerator(self):
        from extras import passwordGenerator
        randomPassword = passwordGenerator.main()
        self.answer.setText(f"Random password: {randomPassword}")
        self.passw.setText(randomPassword)

    def allPasswords(self):
        self.secondWindow = AllPasswordsWindow(self.user)
        self.secondWindow.show()
        self.hide()

    def addPassword(self):
        isim = self.name.text()
        parola = self.passw.text()

        if isim == "" or parola == "":
            self.answer.setText("Name and Password fields cannot be left blank!")
            return False

        self.start_connection(self.user)

        self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (isim,))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.cursor.execute(f"INSERT INTO {self.user} VALUES(?, ?)", (isim, parola))
            self.connection.commit()
            self.answer.setText("Registration Successful!")
        else:
            if self.editMode:
                self.cursor.execute(f"UPDATE {self.user} SET Password = ? WHERE Name = ?", (parola, isim))
                self.connection.commit()
                self.answer.setText("Password updated successfully")
            else:
                self.answer.setText("This password has already been saved!")
    
    def resetSpaces(self):
        self.name.setText("")
        self.passw.setText("")
        self.answer.setText("")
    
    def setSpaces(self, name, passw):
        self.name.setText(name)
        self.passw.setText(passw)
        
    def setEditMode(self, editMode):
        self.editMode = editMode
    
class AllPasswordsWindow(QtWidgets.QWidget):

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.allpass_ui()
    
    def start_connection(self):
        if self.user == None:
            print("User yok")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (Name TEXT, Password TEXT)")
            self.connection.commit()

    def allpass_ui(self):
        self.start_connection()
        self.cursor.execute(f"SELECT Name FROM {self.user}")
        data = self.cursor.fetchall()

        self.searchBar = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton("Search")
        self.showPass = QtWidgets.QPushButton("Show Password")
        self.editPass = QtWidgets.QPushButton("Edit Password")
        self.deletePass = QtWidgets.QPushButton("Delete Password")
        self.passList = QtWidgets.QListWidget()

        for i in range(len(data)):
            self.passList.insertItem(i, data[i][0])

        passH_box1 = QtWidgets.QHBoxLayout()
        passH_box1.addWidget(self.searchBar)
        passH_box1.addWidget(self.searchButton)

        passH_box2 = QtWidgets.QHBoxLayout()
        passH_box2.addWidget(self.showPass)
        passH_box2.addWidget(self.editPass)
        passH_box2.addWidget(self.deletePass)

        passV_box = QtWidgets.QVBoxLayout()
        passV_box.addLayout(passH_box1)
        passV_box.addWidget(self.passList)
        passV_box.addLayout(passH_box2)

        self.passList.itemActivated.connect(self.showPassword_dc)
        self.showPass.clicked.connect(self.showPassword)
        self.editPass.clicked.connect(self.editPassword)
        self.deletePass.clicked.connect(self.deletePassword)
        self.searchButton.clicked.connect(self.searchPasswords)

        self.setLayout(passV_box)
        self.setWindowTitle("My Passwords")
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)
        self.setMinimumWidth(400)
        self.setMaximumWidth(700)
    
    def searchPasswords(self):
        name = self.searchBar.text()
        self.passList.clear()
        if name == "":
            self.cursor.execute(f"SELECT Name FROM {self.user}")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.passList.insertItem(i, data[i][0])
        else:
            self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Name LIKE '%{name}%'")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.passList.insertItem(i, data[i][0])
        self.passList.repaint()

    def showPassword(self):
        if self.passList.currentItem() != None:
            item = self.passList.currentItem().text()
            self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (item,))
            data = self.cursor.fetchall()
            self.showWindow = ShowPasswordsWindow(data[0][0], data[0][1], self.user)
            self.showWindow.show()
            self.hide()
        else:
            return False

    def showPassword_dc(self, item):
        self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (item.text(),))
        data = self.cursor.fetchall()
        self.showWindow = ShowPasswordsWindow(data[0][0], data[0][1], self.user)
        self.showWindow.show()
        self.hide()

    def editPassword(self):
        if self.passList.currentItem() != None:
            item = self.passList.currentItem().text()
            self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (item,))
            data = self.cursor.fetchall()
            self.editWindow = MainWindow(self.user)
            self.editWindow.setSpaces(data[0][0], data[0][1])
            self.editWindow.setEditMode(editMode=True)
            self.editWindow.show()
            self.hide()
        else:
            return False

    def deletePassword(self):
        if self.passList.currentItem() != None:
            item = self.passList.currentItem().text()
            self.cursor.execute(f"DELETE FROM {self.user} WHERE Name = ?", (item,))
            self.connection.commit()
            self.passList.clear()
            self.cursor.execute(f"SELECT Name FROM {self.user}")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.passList.insertItem(i, data[i][0])
            self.passList.repaint()
        else:
            return False
    
    def closeEvent(self, event):
        self.mainWindow = MainWindow(self.user)
        self.mainWindow.show() 

class ShowPasswordsWindow(QtWidgets.QWidget):

    def __init__(self, program_name, password, user):
        super().__init__()
        self.user = user
        self.program_name = program_name
        self.password = password
        self.show_ui()

    def show_ui(self):
        self.nameString = QtWidgets.QLabel("Name of the Program")
        self.name = QtWidgets.QLineEdit(self.program_name)
        self.name.setReadOnly(True)
        self.passString = QtWidgets.QLabel("Password")
        self.passwordLine = QtWidgets.QLineEdit(self.password)
        self.passwordLine.setReadOnly(True)
        self.copyButton = QtWidgets.QPushButton("Copy Password")
        self.info = QtWidgets.QLabel("")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.copyButton)
        h_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.nameString)
        v_box.addWidget(self.name)
        v_box.addWidget(self.passString)
        v_box.addWidget(self.passwordLine)
        v_box.addWidget(self.info)
        v_box.addStretch()
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle(self.program_name)

        self.copyButton.clicked.connect(self.CopyPassword)

        self.setMinimumHeight(170)
        self.setMaximumHeight(170)
        self.setMinimumWidth(300)
        self.setMaximumWidth(300)

    def CopyPassword(self):
        pyperclip.copy(self.password)
        self.info.setText("Password copied successfully")

    def closeEvent(self, event):
        self.mainWindow = MainWindow(self.user)
        self.mainWindow.show()        

app = QtWidgets.QApplication(sys.argv)
pencere = UserControlWindow()
sys.exit(app.exec_())
