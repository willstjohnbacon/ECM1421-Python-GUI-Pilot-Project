import sys
import time
from PyQt5 import QtWidgets, uic
import pyodbc

server = "tcp:ecm1421.database.windows.net"
database = "NymptonFoodHub"
username = "Snakehead181"
password = "{Mypass@word123}"
driver = "{SQL Server}"


def connect(server, db, uid, pwd):

    # connection =pyodbc.connect(
    #     f"""DRIVER={{SQL Server}};
    #     SERVER={server};
    #     DATABASE={db};
    #     Encrypt=yes;
    #     UID={{{uid}}};
    #     PWD={{{pwd}}};
    #     TrustServerCertificate=no;
    #     Connection Timeout=30;"""
    #  )
    server = "DESKTOP-Q1O1S18\SQLEXPRESS"
    connection = pyodbc.connect(
        f"DRIVER={{SQL Server}};SERVER={server};DATABASE=nfhcw2"
    )
    return connection, connection.cursor()


def execute_command(self, query, parameters):
    cursor.execute(query, parameters)

    connection.commit()
    self.refresh_table()
    self.message.setText("Record added successfully")
    self.message.show()
    time.sleep(3)
    self.message.setText("")


class LoginWindow(QtWidgets.QMainWindow):
    def build_ui(self):
        uic.loadUi("login.ui", self)
        self.invalid_login.setText("")
        self.submit.clicked.connect(self.login)
        self.show()

    def login(self):
        """Logs in to the system"""

        username = self.username.text()
        password = self.password.text()

        cursor.execute("SELECT * FROM dbo.Users")

        if any(row[1] == username and row[2] == password for row in cursor.fetchall()):
            stock_cat_ui = StockCategoryWindow()
            stock_cat_ui.build_ui()
            stock_item_ui = StockItemsWindow()
            stock_item_ui.build_ui()
            self.close()
        else:
            self.resize(302, 265)
            self.invalid_login.setText("Invalid login")


class StockCategoryWindow(QtWidgets.QMainWindow):
    def build_ui(self):
        uic.loadUi("stock_categories.ui", self)

        self.edit_mode = False

        self.stock_categories_table.setColumnCount(3)
        self.refresh_table()

        self.edit.clicked.connect(self.toggle_edit)
        self.add.clicked.connect(
            lambda: self.func_add(self.stock_category.text(), self.display_order.text())
        )
        self.update.clicked.connect(
            lambda: self.func_update(
                self.id.text(), self.stock_category.text(), self.display_order.text()
            )
        )
        self.delete_2.clicked.connect(self.func_delete)

        self.add.setEnabled(False)
        self.update.setEnabled(False)
        self.delete_2.setEnabled(False)
        self.id.setEnabled(False)
        self.stock_category.setEnabled(False)
        self.display_order.setEnabled(False)

        self.stock_categories_table.setColumnCount(3)
        self.refresh_table()

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
        self.stock_categories_table.setRowCount(0)
        for row_number, row_data in enumerate(self.table):
            self.stock_categories_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.stock_categories_table.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data))
                )
        self.stock_categories_table.cellDoubleClicked.connect(self.load_record)
        self.display_order.setRange(0, len(self.table))

    def load_record(self):
        current_row = self.stock_categories_table.currentRow()

        self.id.setText(str(self.table[current_row][0]))
        self.stock_category.setText(str(self.table[current_row][1]))
        self.display_order.setValue(self.table[current_row][2])

    def update_record(self, id, stock_category, new_do):
        old_do = None
        for row in self.table:
            if row[0] == id:
                old_do = row[2]
        if old_do is None or old_do == "":
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

    def update_record_sql(self, id, stock_category, display_order):
        """Updates the values of the item with the given id in the StockCategory table."""
        query = "UPDATE StockCategory SET stockcategory=?, displayorder=? WHERE id=?;"
        parameters = (stock_category, display_order, id)
        cursor.execute(query, parameters)

        connection.commit()

    def func_add(self, stock_category, display_order):
        """Adds an item to the StockCategory table, where stock_category and display_order are given in the PyQt page. Autogenerates a unique ID for the item."""
        query = "INSERT INTO StockCategory (stockcategory, displayorder) VALUES (?,?);"
        parameters = (stock_category, display_order)

        for row in self.table:
            if row[2] >= int(display_order):
                self.update_record_sql(row[0], row[1], row[2] + 1)

        execute_command(self, query, parameters)

    def func_update(self, id, stock_category, display_order):
        """Updates the attributes of a specifc record in the stock categories"""

        self.update_record(id, stock_category, int(display_order))

        self.message.setText("Record updated successfully")
        time.sleep(3)
        self.message.setText("")

    def func_delete(self, id):
        """Deletes the item with the given id in the StockCategory table."""

        button = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure that you want to delete the selected category?",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )

        if button == QtWidgets.QMessageBox.StandardButton.Yes:
            query = "DELETE FROM StockCategory WHERE id=?;"
            parameters = id
            cursor.execute(query, parameters)

            connection.commit()

            display_order = None
            for row in self.table:
                if row[0] == id:
                    display_order = row[2]

            if display_order is not None:
                for row in self.table:
                    if row[2] >= display_order:
                        self.update_record_sql(row[0], row[1], row[2] + 1)

            self.refresh_table()

            self.message.setText("Record deleted successfully")
            time.sleep(3)
            self.message.setText("")


class StockItemsWindow(QtWidgets.QMainWindow):
    def build_ui(self):
        uic.loadUi("stock_items.ui", self)

        self.edit_mode = True
        self.toggle_edit()

        self.edit.clicked.connect(self.toggle_edit)

        self.add.clicked.connect(
            lambda: self.func_add(
                self.item_name.text(),
                self.item_unit.text(),
                self.price.text(),
                self.availability.currentText(),
                self.categories.currentText(),
                self.additional_information.toPlainText(),
            )
        )
        self.update.clicked.connect(
            lambda: self.func_update(
                self.id.text(),
                self.item_name.text(),
                self.item_unit.text(),
                self.price.text(),
                self.availability.currentText(),
                self.categories.currentText(),
                self.additional_information.toPlainText(),
            )
        )
        self.delete_2.clicked.connect(lambda: self.func_delete(self.id.text()))

        self.add.setEnabled(False)
        self.update.setEnabled(False)
        self.delete_2.setEnabled(False)
        self.id.setEnabled(False)
        self.item_name.setEnabled(False)
        self.price.setEnabled(False)
        self.availability.setEnabled(False)
        self.availability.addItem("Y")
        self.availability.addItem("N")
        self.additional_information.setEnabled(False)
        self.categories.setEnabled(False)

        cursor.execute("SELECT * FROM StockCategory")
        temp = cursor.fetchall()
        self.categories2 = {row[1]: row[0] for row in temp}
        self.categories1 = {row[0]: row[1] for row in temp}
        for row in temp:
            self.categories.addItem(row[1])

        self.stock_items_table.setColumnCount(5)
        self.refresh_table()

        self.show()

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        self.add.setEnabled(self.edit_mode)
        self.update.setEnabled(self.edit_mode)
        self.delete_2.setEnabled(self.edit_mode)
        self.item_name.setEnabled(self.edit_mode)
        self.price.setEnabled(self.edit_mode)
        self.item_unit.setEnabled(self.edit_mode)
        self.availability.setEnabled(self.edit_mode)
        self.additional_information.setEnabled(self.edit_mode)
        self.categories.setEnabled(self.edit_mode)

    def refresh_table(self):
        cursor.execute("SELECT * FROM StockItem")
        self.table = cursor.fetchall()
        self.stock_items_table.setRowCount(0)
        for row_number, row_data in enumerate(self.table):
            self.stock_items_table.insertRow(row_number)
            for column_number, data in enumerate(
                row_data[:4] + (self.categories1[row_data[5]],)
            ):
                self.stock_items_table.setItem(
                    row_number, column_number, QtWidgets.QTableWidgetItem(str(data))
                )
        self.stock_items_table.cellDoubleClicked.connect(self.load_record)

    def load_record(self):
        current_row = self.stock_items_table.currentRow()
        self.id.setText(str(self.table[current_row][0]))
        self.item_name.setText(self.table[current_row][1])
        self.item_unit.setText(self.table[current_row][2])
        self.price.setValue(self.table[current_row][3])
        self.availability.setCurrentText(self.table[current_row][4])
        self.categories.setCurrentText(self.categories1[self.table[current_row][5]])
        self.additional_information.setText(self.table[current_row][6])

    def func_add(
        self,
        item_name,
        item_unit,
        item_price,
        availability,
        category,
        additional_information,
    ):
        """Adds an item to the StockCategory table, where stock_category and display_order are given in the PyQt page. Autogenerates a unique ID for the item."""

        query = "INSERT INTO StockItem (itemname, itemunit, itemprice, available, categoryid, itemaddlinfo) VALUES (?,?,?,?,?,?);"
        parameters = (
            item_name,
            item_unit,
            float(item_price),
            availability,
            self.categories2[category],
            additional_information,
        )

        execute_command(self, query, parameters)

    def func_update(
        self,
        id,
        item_name,
        item_unit,
        item_price,
        availability,
        category,
        additional_information,
    ):
        """Updates the attributes of a specifc record in the stock categories"""

        query = "UPDATE StockItem SET itemname=?, itemunit=?, itemprice=?, available=?, categoryid=?, itemaddlinfo=? WHERE id=?;"
        parameters = (
            item_name,
            item_unit,
            float(item_price),
            availability,
            self.categories2[category],
            additional_information,
            id,
        )
        execute_command(self, query, parameters)

    def func_delete(self, id):
        """Deletes the item with the given id in the StockItem table."""

        button = QtWidgets.QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure that you want to delete the selected item?",
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No,
        )

        if button == QtWidgets.QMessageBox.StandardButton.Yes:
            query = "DELETE FROM StockItem WHERE id=?;"
            parameters = id

            execute_command(self, query, parameters)


if __name__ == "__main__":

    connection, cursor = connect(
        server,
        database,
        username,
        password,
    )
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWindow()
    ui.build_ui()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing Window...")
