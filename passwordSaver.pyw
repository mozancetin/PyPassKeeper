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
        self.editMode = False
        self.user = user
        self.init_ui()
    
    def start_connection(self,user):
        if user == None:
            print("User is not exists")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (Name TEXT, Password TEXT, Category TEXT)")
            self.connection.commit()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {user}C (Categories TEXT)")
            self.connection.commit()

            self.cursor.execute(f"SELECT * FROM {user}C WHERE Categories = ?", ("Uncategorized",))
            data = self.cursor.fetchall()
            if len(data) == 0:
                self.cursor.execute(f"INSERT INTO {user}C VALUES(?)", ("Uncategorized",))
                self.connection.commit()

    def init_ui(self):
        self.name = QtWidgets.QLineEdit()
        self.nameString = QtWidgets.QLabel("Name of the Program")

        self.comboLabel = QtWidgets.QLabel("Categories")

        self.passw = QtWidgets.QLineEdit()
        self.passwString = QtWidgets.QLabel("Password")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)

        self.answer = QtWidgets.QLabel("")
        self.savepass = QtWidgets.QPushButton("Save")
        self.allpassw = QtWidgets.QPushButton("All Passwords")
        self.categories = QtWidgets.QPushButton("Categories")
        self.generatorButton = QtWidgets.QPushButton("Generate Random Password")
        self.combo_Box = QtWidgets.QComboBox()

        self.start_connection(self.user)
        self.cursor.execute(f"SELECT * FROM {self.user}C")
        data = self.cursor.fetchall()
        for i in range(len(data)):
            self.combo_Box.addItem(data[i][0])
        index = self.combo_Box.findText("Uncategorized")
        if index >= 0:
            self.combo_Box.setCurrentIndex(index)

        mainH_box3 = QtWidgets.QHBoxLayout()
        mainH_box3.addWidget(self.categories)
        mainH_box3.addWidget(self.allpassw)

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
        mainV_box.addWidget(self.comboLabel)
        mainV_box.addWidget(self.combo_Box)
        mainV_box.addLayout(mainH_box2)
        mainV_box.addStretch()
        mainV_box.addWidget(self.savepass)
        mainV_box.addLayout(mainH_box3)
        mainV_box.addWidget(self.generatorButton)

        mainH_box = QtWidgets.QHBoxLayout()
        mainH_box.addLayout(mainV_box)

        self.setLayout(mainH_box)

        self.savepass.clicked.connect(self.addPassword)
        self.allpassw.clicked.connect(self.allPasswords)
        self.generatorButton.clicked.connect(self.passwordGenerator)
        self.categories.clicked.connect(self.allCategories)

        self.setWindowTitle("Main Window")
        self.setMinimumHeight(260)
        self.setMaximumHeight(260)
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)
    
    def allCategories(self):
        self.thirdWindow = CategoriesWindow(self.user)
        self.thirdWindow.show()
        self.hide()

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
        category = self.combo_Box.currentText()


        if isim == "" or parola == "":
            self.answer.setText("Name and Password fields cannot be left blank!")
            return False

        self.start_connection(self.user)

        self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (isim,))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.cursor.execute(f"INSERT INTO {self.user} VALUES(?, ?, ?)", (isim, parola, category))
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
        self.CategoryMode = False
        self.category = "Uncategorized"
        self.user = user
        self.allpass_ui()
    
    def start_connection(self):
        if self.user == None:
            print("User yok")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (Name TEXT, Password TEXT, Category TEXT)")
            self.connection.commit()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user}C (Categories TEXT)")
            self.connection.commit()

    def allpass_ui(self):
        self.start_connection()
        if not self.CategoryMode:
            self.cursor.execute(f"SELECT Name FROM {self.user}")
            data = self.cursor.fetchall()
        else:
            self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Category = ?", (self.category,))
            data = self.cursor.fetchall()

        self.searchBar = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton("Search")
        self.showPass = QtWidgets.QPushButton("Show Password")
        self.editPass = QtWidgets.QPushButton("Edit Password")
        self.changeCategory = QtWidgets.QPushButton("Change Category")
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
        passH_box2.addWidget(self.changeCategory)
        passH_box2.addWidget(self.deletePass)

        passV_box = QtWidgets.QVBoxLayout()
        passV_box.addLayout(passH_box1)
        passV_box.addWidget(self.passList)
        passV_box.addLayout(passH_box2)

        self.passList.itemActivated.connect(self.showPassword_dc)
        self.showPass.clicked.connect(self.showPassword)
        self.editPass.clicked.connect(self.editPassword)
        self.changeCategory.clicked.connect(self.editCategory)
        self.deletePass.clicked.connect(self.deletePassword)
        self.searchButton.clicked.connect(self.searchPasswords)

        self.setLayout(passV_box)
        self.setWindowTitle("My Passwords")
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)
        self.setMinimumWidth(400)
        self.setMaximumWidth(700)
    
    def editCategory(self):
        if self.passList.currentItem() != None:
            item = self.passList.currentItem().text()
            self.cursor.execute(f"SELECT Category FROM {self.user} WHERE Name = ?", (item,))
            data = self.cursor.fetchone()
            category = data[0]
            print(category)
            self.chCategoryWindow = EditCategoryWindow(self.user, item, category)
            self.chCategoryWindow.show()
            self.hide()
        else:
            return False
    
    def searchPasswords(self):
        name = self.searchBar.text()
        self.passList.clear()
        if not self.CategoryMode:
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
        else:
            if name == "":
                self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Category = ?", (self.category,))
                data = self.cursor.fetchall()
                for i in range(len(data)):
                    self.passList.insertItem(i, data[i][0])
            else:
                self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Name LIKE '%{name}%' AND Category = ?", (self.category,))
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
            if not self.CategoryMode:
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
                item = self.passList.currentItem().text()
                self.cursor.execute(f"DELETE FROM {self.user} WHERE Name = ?", (item,))
                self.connection.commit()
                self.passList.clear()
                self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Category = ?", (self.category,))
                data = self.cursor.fetchall()
                for i in range(len(data)):
                    self.passList.insertItem(i, data[i][0])
                self.passList.repaint()
        else:
            return False

    def setCategoryMode(self, mode):
        self.CategoryMode = mode
        if mode:
            self.passList.clear()
            self.cursor.execute(f"SELECT Name FROM {self.user} WHERE Category = ?", (self.category,))
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.passList.insertItem(i, data[i][0])
            self.passList.repaint()

    def setCategory(self, category):
        self.category = category

    def closeEvent(self, event):
        self.mainWindow = MainWindow(self.user)
        self.mainWindow.show() 

class CategoriesWindow(QtWidgets.QWidget):

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.ctg_ui()
    
    def start_connection(self):
        if self.user == None:
            print("User yok")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (Name TEXT, Password TEXT, Category TEXT)")
            self.connection.commit()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user}C (Categories TEXT)")
            self.connection.commit()

    def ctg_ui(self):
        self.start_connection()
        self.cursor.execute(f"SELECT Categories FROM {self.user}C")
        data = self.cursor.fetchall()

        self.searchBar = QtWidgets.QLineEdit()
        self.searchButton = QtWidgets.QPushButton("Search")
        self.addBar = QtWidgets.QLineEdit()
        self.addCat = QtWidgets.QPushButton("Add Category")
        self.showCat = QtWidgets.QPushButton("Show Category")
        self.editBar = QtWidgets.QLineEdit()
        self.editCat = QtWidgets.QPushButton("Edit Category")
        self.deleteCat = QtWidgets.QPushButton("Delete Category")
        self.CatList = QtWidgets.QListWidget()

        for i in range(len(data)):
            self.CatList.insertItem(i, data[i][0])
            

        catH_box1 = QtWidgets.QHBoxLayout()
        catH_box1.addWidget(self.searchBar)
        catH_box1.addWidget(self.searchButton)

        catH_box2 = QtWidgets.QHBoxLayout()
        catH_box2.addWidget(self.showCat)
        catH_box2.addWidget(self.deleteCat)

        catH_box4 = QtWidgets.QHBoxLayout()
        catH_box4.addWidget(self.editBar)
        catH_box4.addWidget(self.editCat)

        catH_box3 = QtWidgets.QHBoxLayout()
        catH_box3.addWidget(self.addBar)
        catH_box3.addWidget(self.addCat)

        catV_box = QtWidgets.QVBoxLayout()
        catV_box.addLayout(catH_box1)
        catV_box.addWidget(self.CatList)
        catV_box.addLayout(catH_box3)
        catV_box.addLayout(catH_box4)
        catV_box.addLayout(catH_box2)

        self.CatList.itemActivated.connect(self.showCats_dc)
        self.addCat.clicked.connect(self.addCategory)
        self.showCat.clicked.connect(self.showCats)
        self.editCat.clicked.connect(self.editCategory)
        self.deleteCat.clicked.connect(self.deleteCategory)
        self.searchButton.clicked.connect(self.searchCats)

        self.setLayout(catV_box)
        self.setWindowTitle("Categories")
        self.setMinimumHeight(300)
        self.setMaximumHeight(500)
        self.setMinimumWidth(400)
        self.setMaximumWidth(700)
    
    def addCategory(self):
        categoryName = self.addBar.text()
        if categoryName == "":
            return False
        else:
            self.cursor.execute(f"SELECT * FROM {self.user}C WHERE Categories = ?", (categoryName,))
            data = self.cursor.fetchall()
            if len(data) == 0:
                self.cursor.execute(f"INSERT INTO {self.user}C VALUES(?)", (categoryName,))
                self.connection.commit()
                self.CatList.clear()
                self.cursor.execute(f"SELECT * FROM {self.user}C")
                data = self.cursor.fetchall()
                for i in range(len(data)):
                    self.CatList.insertItem(i, data[i][0])
                self.CatList.repaint()
                self.addBar.setText("")
            else:
                return False


    def showCats_dc(self, item):
        self.showWindow = AllPasswordsWindow(self.user)
        self.showWindow.setCategory(item.text())
        self.showWindow.setCategoryMode(True)
        self.showWindow.show()
        self.hide()

    def showCats(self):
        if self.CatList.currentItem() != None:
            item = self.CatList.currentItem()
            self.showWindow = AllPasswordsWindow(self.user)
            self.showWindow.setCategory(item.text())
            self.showWindow.setCategoryMode(True)
            self.showWindow.show()
            self.hide()
        else:
            return False

    def editCategory(self):
        if self.CatList.currentItem() != None:
            item = self.CatList.currentItem().text()
            if self.editBar.text() != "":
                name = self.editBar.text()
                self.cursor.execute(f"UPDATE {self.user}C SET Categories = ? WHERE Categories = ?", (name, item))
                self.connection.commit()
                self.cursor.execute(f"UPDATE {self.user} SET Category = ? WHERE Category = ?", (name, item))
                self.connection.commit()
                self.CatList.clear()
                self.cursor.execute(f"SELECT * FROM {self.user}C")
                data = self.cursor.fetchall()
                for i in range(len(data)):
                    self.CatList.insertItem(i, data[i][0])
                self.CatList.repaint()
                self.editBar.setText("")
            else:
                return False
        else:
            return False

    def deleteCategory(self):
        if self.CatList.currentItem() != None:
            item = self.CatList.currentItem().text()
            self.cursor.execute(f"UPDATE {self.user} SET Category = ? WHERE Category = ?", ("Uncategorized", item))
            self.connection.commit()
            self.cursor.execute(f"DELETE FROM {self.user}C WHERE Categories = ?", (item,))
            self.connection.commit()
            self.cursor.execute(f"SELECT * FROM {self.user}C WHERE Categories = ?", ("Uncategorized",))
            data = self.cursor.fetchall()
            if len(data) == 0:
                self.cursor.execute(f"INSERT INTO {self.user}C VALUES(?)", ("Uncategorized",))
                self.connection.commit()
            self.CatList.clear()
            self.cursor.execute(f"SELECT * FROM {self.user}C")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.CatList.insertItem(i, data[i][0])
            self.CatList.repaint()
        else:
            return False

    def searchCats(self):
        name = self.searchBar.text()
        self.CatList.clear()
        if name == "":
            self.cursor.execute(f"SELECT Categories FROM {self.user}C")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.CatList.insertItem(i, data[i][0])
        else:
            self.cursor.execute(f"SELECT Categories FROM {self.user}C WHERE Categories LIKE '%{name}%'")
            data = self.cursor.fetchall()
            for i in range(len(data)):
                self.CatList.insertItem(i, data[i][0])
        self.CatList.repaint()

    def closeEvent(self, event):
        self.mainMenu = MainWindow(self.user)
        self.mainMenu.show()

class EditCategoryWindow(QtWidgets.QWidget):

    def __init__(self, user, item_name, category = "Uncategorized"):
        super().__init__()
        self.category = category
        self.item_name = item_name
        self.user = user
        self.editCat_ui()

    def start_connection(self):
        if self.user == None:
            print("User yok")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user} (Name TEXT, Password TEXT, Category TEXT)")
            self.connection.commit()
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.user}C (Categories TEXT)")
            self.connection.commit()
    
    def editCat_ui(self):
        self.start_connection()
        self.comboBox = QtWidgets.QComboBox()
        self.editButton = QtWidgets.QPushButton("Edit")
        self.cancelButton = QtWidgets.QPushButton("Cancel")

        self.cursor.execute(f"SELECT * FROM {self.user}C")
        data = self.cursor.fetchall()
        for i in range(len(data)):
            self.comboBox.addItem(data[i][0])
        index = self.comboBox.findText(self.category)
        if index >= 0:
            self.comboBox.setCurrentIndex(index)
        
        editV_box2 = QtWidgets.QHBoxLayout()
        editV_box2.addWidget(self.editButton)
        editV_box2.addWidget(self.cancelButton)

        editH_Box = QtWidgets.QVBoxLayout()
        editH_Box.addStretch()
        editH_Box.addWidget(self.comboBox)
        editH_Box.addLayout(editV_box2)
        editH_Box.addStretch()

        editV_box = QtWidgets.QHBoxLayout()
        editV_box.addStretch()
        editV_box.addLayout(editH_Box)
        editV_box.addStretch()

        self.editButton.clicked.connect(self.editCatButton)
        self.cancelButton.clicked.connect(self.cancelTaskButton)

        self.setLayout(editV_box)
        self.setWindowTitle(f"{self.item_name}")
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)
    
    def editCatButton(self):
        item = self.comboBox.currentText()
        self.cursor.execute(f"UPDATE {self.user} SET Category = ? WHERE Name = ?", (item, self.item_name))
        self.connection.commit()
        self.close()

    def cancelTaskButton(self):
        self.close()
    
    def closeEvent(self, event):
        self.mainMenu = MainWindow(self.user)
        self.mainMenu.show()

    
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