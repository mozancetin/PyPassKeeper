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
        self.mainWindow = MainWindow()

        self.warning = QtWidgets.QLabel("")
        self.username = QtWidgets.QLineEdit()
        self.usernameString = QtWidgets.QLabel("Kullanıcı Adı")
        self.passwordString = QtWidgets.QLabel("Şifre")
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton = QtWidgets.QPushButton("Giriş Yap")
        self.regButton = QtWidgets.QPushButton("Kayıt Ol")

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
        self.setMaximumHeight(170)
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)

        self.show()
    
    def Login(self):
        isim = self.username.text()
        parola = self.password.text()

        self.cursor.execute("SELECT * FROM Users WHERE UserName = ? AND Password = ?",(isim,parola))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.warning.setText("Böyle bir kullanıcı yok.")
        else:
            self.mainWindow.user = isim
            self.warning.setText("Giriş yapıldı.")
            self.mainWindow.resetSpaces()
            self.mainWindow.show()
            self.close()
    
    def Register(self):
        isim = self.username.text()
        parola = self.password.text()

        if isim == "" or parola == "":
            self.warning.setText("İsim ve Şifre alanı boş bırakılamaz!")
            return False

        self.cursor.execute("SELECT * FROM Users WHERE UserName = ? AND Password = ?",(isim,parola))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.cursor.execute("INSERT INTO Users VALUES(?, ?)", (isim, parola))
            self.connection.commit()
            self.warning.setText("Kayıt başarılı")
        else:
            self.warning.setText("Böyle bir kullanıcı var.")



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.user = None

        self.init_ui()
    
    def start_connection(self,user):
        if user == None:
            print("User yok")
        else:
            self.connection = sqlite3.connect("passwordDatabase.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {user} (Name TEXT, Password TEXT)")
            self.connection.commit()

    def init_ui(self):
        self.name = QtWidgets.QLineEdit()
        self.nameString = QtWidgets.QLabel("Program Adı")

        self.passw = QtWidgets.QLineEdit()
        self.passwString = QtWidgets.QLabel("Şifre (Program kaydetmek için)")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)

        self.answer = QtWidgets.QLabel("")
        self.search = QtWidgets.QPushButton("Ara")
        self.savepass = QtWidgets.QPushButton("Kaydet")
        self.copyBtn = QtWidgets.QPushButton("Şifreyi Kopyala")
        self.copyBtn.setEnabled(False)

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
        mainV_box.addWidget(self.search)
        mainV_box.addWidget(self.savepass)
        mainV_box.addWidget(self.copyBtn)

        mainH_box = QtWidgets.QHBoxLayout()
        mainH_box.addStretch()
        mainH_box.addLayout(mainV_box)
        mainH_box.addStretch()

        self.setLayout(mainH_box)

        self.search.clicked.connect(self.searchPassword)
        self.savepass.clicked.connect(self.addPassword)
        self.copyBtn.clicked.connect(self.CopyPassword)

        self.setWindowTitle("Main Window")
        self.setMinimumHeight(230)
        self.setMaximumHeight(230)
        self.setMinimumWidth(250)
        self.setMaximumWidth(250)

    def searchPassword(self):
        isim = self.name.text()
        self.start_connection(self.user)

        self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (isim,))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.answer.setText("Böyle bir şifre kaydetmemişsiniz.")
        else:
            self.answer.setText(f"Şifre: {data[0][1]}")
            self.copyBtn.setEnabled(True)
        
        

    def addPassword(self):
        isim = self.name.text()
        parola = self.passw.text()

        if isim == "" or parola == "":
            self.answer.setText("İsim ve Şifre alanı boş bırakılamaz!")
            return False

        self.start_connection(self.user)

        self.cursor.execute(f"SELECT * FROM {self.user} WHERE Name = ?", (isim,))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.cursor.execute(f"INSERT INTO {self.user} VALUES(?, ?)", (isim, parola))
            self.connection.commit()
            self.answer.setText("Kayıt başarılı!")
        else:
            self.answer.setText("Daha önceden kaydedilmiş şifre!")
    
    def CopyPassword(self):
        pyperclip.copy(self.answer.text()[7:])
        self.answer.setText("Şifre panoya kopyalandı!")
    
    def resetSpaces(self):
        self.name.setText("")
        self.passw.setText("")
        self.answer.setText("")

app = QtWidgets.QApplication(sys.argv)
pencere = UserControlWindow()
sys.exit(app.exec_())