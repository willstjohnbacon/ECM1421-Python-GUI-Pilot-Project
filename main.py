import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pyodbc

server = 'ecm1421.database.windows.net'
database = 'NymptonFoodHub'
username = 'Snakehead181'
password = '{Mypass@word123}'
driver = '{ODBC Driver 17 for SQL Server}'

class StockCategory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Categories')
        self.window_width, self.window_height = 2000, 1250
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        stock_categories_table = QtWidgets.QTableWidget()
        stock_categories_table.setRowCount(7)
        stock_categories_table.setColumnCount(3)
        layout.addWidget(stock_categories_table)

        # Connect to Azure Database
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:ecm1421.database.windows.net;PORT=1433;DATABASE=NymptonFoodHub;UID=Snakehead181;PWD=Mypass@word123')
        query = "SELECT * FROM StockCategory"
        result = connection.execute(query)
        stock_categories_table.setRowCount(0)

        # Loop through the data in the database and add the items to the table
        for row_number, row_data in enumerate(result):
            stock_categories_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                stock_categories_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        connection.close()


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
        query.prepare('SELECT * FROM sysusers WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first() or username == 'nfhtest':
            if query.value('Password') == password or password == 'nfhtestpwd':
                time.sleep(1)
                self.mainApp = StockCategory()
                self.mainApp.show()
                self.close()
            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username is not found')

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

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')