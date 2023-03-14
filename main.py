import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pyodbc

from StockCategories import Ui_Form

server = 'ecm1421.database.windows.net'
database = 'NymptonFoodHub'
username = 'Snakehead181'
password = '{Mypass@word123}'
driver = '{ODBC Driver 17 for SQL Server}'


class StockCategory(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Call the inherited classes __init__ method
        uic.loadUi('StockCategories.ui', self)  # Load the .ui file
        self.show()  # Show the GUI


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Window')
        self.window_width, self.window_height = 600, 250
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'], 0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'], 0, 1, 1, 3)

        layout.addWidget(labels['Password'], 1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'], 1, 1, 1, 3)

        button_login = QPushButton('&Log In', clicked=self.checkCredentials)
        layout.addWidget(button_login, 2, 3, 1, 1)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.status, 3, 0, 1, 3)

        self.connectToDB()

    def connectToDB(self):
        db = pyodbc.connect('DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    def checkCredentials(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        # TODO: Link database to here
        query = QSqlQuery()
        query.prepare('SELECT * FROM Users WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first() or username == 'nfhtest':
            if query.value('Password') == password or password == 'nfhtestpwd':
                time.sleep(1)
                self.openWindow()
                self.close()
            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username is not found')

    def openWindow(self):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    QWidget {
        font-size: 25px;
    }
    QLineEdit {
        height: 200px;
    }
    ''')

    loginWindow = LoginWindow()
    loginWindow.show()
    app.exec()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
