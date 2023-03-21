import sys
import os
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import pyodbc

from login2 import Ui_Login
#from stock_categories import Ui_Stock_Categories


server = 'tcp:ecm1421.database.windows.net'
database = 'NymptonFoodHub'
username = 'Snakehead181'
password = '{Mypass@word123}'
driver = '{ODBC Driver 17 for SQL Server}'

def connect(server, db, uid, pwd):

    #connection = pyodbc.connect(
    #    f"""DRIVER={{ODBC Driver 17 for SQL Server}};
    #    SERVER={{{server}}};
    #    DATABASE={{{db}}};
    #    UID={{{uid}}};
    #    PWD={{{pwd}}};
    #    Encrypt=yes;
    #    TrustServerCertificate=no;
    #    Connection Timeout=30;"""
    #)
    connection = pyodbc.connect(
        f"""DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER=tcp:ecm1421.database.windows.net;
        PORT=1433;
        DATABASE=NymptonFoodHub;
        UID=Snakehead181;
        PWD={{Mypass@word123}};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;"""
    )

    return connection, connection.cursor()


class LoginWindow(QtWidgets.QMainWindow):
    def build_ui(self):
        uic.loadUi('login.ui', self)
        self.invalid_login.setText("")
        self.submit.clicked.connect(self.login)
        self.show()


    def login(self):
        '''Logs in to the system'''

        username = self.username.text()
        password = self.password.text()

        cursor.execute("SELECT * FROM dbo.Users")

        if any(row[1] == username and row[2] == password for row in cursor.fetchall()):
            time.sleep(0.5)
            #self.mainApp = StockCategoryWindow()
            #self.mainApp.show()
            #self.close()
            stock_cat_ui = StockCategoryWindow()
            stock_cat_ui.build_ui()
        else:
            self.resize(302, 265)
            self.invalid_login.setText("Invalid login")



class StockCategoryWindow(QtWidgets.QMainWindow):
    
    def build_ui(self):
        uic.loadUi('stock_categories.ui', self)

        self.edit_mode = False

        self.edit.clicked.connect(self.toggle_edit)
        self.add.clicked.connect(self.func_add(self.stock_category.text(),self.display_order.text()))
        self.update.clicked.connect(self.func_update(self.id.text(),self.stock_category.text(),self.display_order.text()))
        self.delete_2.clicked.connect(self.func_delete())

        self.add.setEnabled(False)
        self.update.setEnabled(False)
        self.delete_2.setEnabled(False)
        self.id.setEnabled(False)
        self.stock_category.setEnabled(False)
        self.display_order.setEnabled(False)

        self.stock_categories_table.setColumnCount(3)
        self.refresh_table()
        # Loop through the data in the database and add the items to the table

        self.show()


    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        self.add.setEnabled(self.edit_mode)
        self.update.setEnabled(self.edit_mode)
        self.delete_2.setEnabled(self.edit_mode)
        self.stock_category.setEnabled(self.edit_mode)
        self.display_order.setEnabled(self.edit_mode)


    def refresh_table(self):
        cursor.execute("SELECT * FROM StockCategory")
        self.table = cursor.fetchall()
        self.populate_table
        self.stock_categories_table.setRowCount(0)
        for row_number, row_data in enumerate(self.table):
            self.stock_categories_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.stock_categories_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        

    def update_record(self, id, stock_category, old_do, new_do):
        old_do = None
        for row in self.table:
            if row[0] == id:
                old_do = row[2]
        if old_do is None:
            self.func_update(id, stock_category, new_do)
            return

        if old_do < new_do:
            rows_to_update = [row for row in self.table if new_do <= row[2] <= old_do]
            for row in rows_to_update:
                row[2] -= 1
                self.func_update(row[0], row[1], row[2])
            
        elif new_do < old_do:
            rows_to_update = [row for row in self.table if old_do <= row[2] <= new_do]
            for row in rows_to_update:
                row[2] += 1
                self.func_update(row[0], row[1], row[2])
        
        self.func_update(id, stock_category, new_do)


    def update_record_sql(self,id,stock_category,display_order):
        """Updates the values of the item with the given id in the StockCategory table."""

        cursor.execute(
            "UPDATE StockCategory SET stockcategory='%(stock_category)s', displayorder='%(display_order)d' WHERE id=%(id)d;",
            {
                "stock_category": stock_category,
                "display_order": display_order,
                "id": id,
            },
        )
        
        connection.commit()


    def func_add(self, stock_category, display_order):
        """Adds an item to the StockCategory table, where stock_category and display_order are given in the PyQt page. Autogenerates a unique ID for the item."""
        cursor.execute(
            "INSERT INTO StockCategory (stockcategory, displayorder) VALUES ('%(stock_category)s','%(display_order)d');",
            {"stock_category": stock_category, 
             "display_order": display_order},
        )
        
        connection.commit()
        
        for row in self.table:
            if row[2] >= display_order:
                self.update_record_sql(row[0],row[1],row[2]+1)

        self.refresh_table()

        self.message.setText("Record added successfully")
        time.sleep(3)
        self.message.setText("")


    def func_update(self,id,stock_category,display_order):
        '''Updates the attributes of a specifc record in the stock categories'''

        self.update_record(id, stock_category, int(display_order))

        self.message.setText("Record updated successfully")
        time.sleep(3)
        self.message.setText("")


    def func_delete(self):
        """Deletes the item with the given id in the StockCategory table."""

        # N.B. BEFORE THIS IS RUN, ADD CONFIRMATION IN THE GUI

        cursor.execute("DELETE FROM StockCategory WHERE id=%(id)d;", {"id": id})

        connection.commit()

        display_order = None
        for row in self.table:
            if row[0] == id:
                display_order = row[2]

        #for row in self.table:
        #    if row[2] >= :
        #        self.update_record_sql(row[0],row[1],row[2]+1)
#
        self.refresh_table()

        self.message.setText("Record deleted successfully")
        time.sleep(3)
        self.message.setText("")

def validate(table):
    for row in table:
        if row[1] == username and row[2] == password:
            return True


if __name__ == "__main__":

    # connect to db
    connection, cursor = connect(
        server,
        database,
        username,
        password,
    )

    app = QtWidgets.QApplication(sys.argv)
    #Login = QtWidgets.QMainWindow()
    ui = StockCategoryWindow()
    ui.build_ui()
    #Login.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
