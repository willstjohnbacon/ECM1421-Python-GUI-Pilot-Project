import pyodbc
import sys
from PyQt5 import QtWidgets, uic

def load_metadata():
    with open("metadata.json", "r") as f:
        pass


    def login(self, cursor, username, password):

        # TEMPORARY VARIABLES, TO BE CHANGED WHEN GUI MADE
        username = "nfhtest"
        password = "nfhtestpwd"

        # Returns true or false values depending on whether or not the username and password are in the system.
        cursor.execute("SELECT * FROM Users")
        return any(
            row[1] == username and row[2] == password for row in cursor.fetchall()
        )


class StockCategories(object):
    def __init__(self):

        cursor.execute("SELECT * FROM StockCategory")

        stock_categories = (
            cursor.fetchall()
        )  # Returns StockCategory as a list of tuples.

        # CREATE GUI HERE

        # N.B. Display by display order, not ID

    def toggle_edit_mode(self):
        pass

    def cancel(self):
        sys.exit(self.exec_())

    def add(self, stock_category, display_order):
        """Adds an item to the StockCategory table, where stock_category and display_order are given in the PyQt page. Autogenerates a unique ID for the item."""

        cursor.execute("INSERT INTO StockCategory (stockcategory, displayorder) VALUES ('%(stock_category)s','%(display_order)d');",
                       {'stock_category': stock_category,
                       'display_order': display_order})

    def update(self, id, stock_category, display_order):
        """Updates the values of the item with the given id in the StockCategory table."""

        cursor.execute("UPDATE StockCategory SET stockcategory='%(stock_category)s', displayorder='%(display_order)d' WHERE id=%(id)d;",
                       {'stock_category': stock_category,
                        'display_order': display_order,
                        'id': id})
        

    def delete(self, id):
        """Deletes the item with the given id in the StockCategory table."""

        # N.B. BEFORE THIS IS RUN, ADD CONFIRMATION IN THE GUI

        cursor.execute("DELETE FROM StockCategory WHERE id=%(id)d;",
                       {'id': id})


class StockItems(object):
    def __init__(self):

        cursor.execute("SELECT id, stockcategory FROM StockCategory")
        stock_categories = cursor.fetchall()

        cursor.execute(
            """SELECT stock.id,
                            stock.itemname,
                            stock.itemunit,
                            stock.itemprice,
                            category.stockcategory
	                    FROM StockItem stock
	                    INNER JOIN StockCategory category
	                    ON stock.categoryid = category.id"""
        )

        stock_items = cursor.fetchall()  # Returns Stockitems as a list of tuples.

        # CREATE GUI HERE

        # Requirements:
        # ID box (not editable), Item Name box (editable), Item unit box (editable), Item Price box (editable, only accepts floats), Category dropdown box.

    def toggle_edit_mode(self):
        pass

    def cancel(self):
        sys.exit(self.exec_())

    def add(self, item_name, item_unit, item_price, category, stock_categories):

        for c in stock_categories:
            if category == c[1]:
                category = c[0]
                break

        cursor.execute("INSERT INTO StockItem (itemname, itemunit, itemprice, categoryid) VALUES ('%(item_name)s', '%(item_unit)s', %(item_price)f, %(category)d);",
                       {'item_name': item_name,
                        'item_unit': item_unit,
                        'item_price': item_price,
                        'category': category})

        connection.commit()

    def update(self, id, item_name, item_unit, item_price, category, stock_categories):

        for c in stock_categories:
            if category == c[1]:
                category = c[0]

        cursor.execute("UPDATE StockItem SET itemname='%(item_name)s', itemunit='%(item_unit)s', itemprice=%(item_price)f,categoryid=%(category)d WHERE id=%(id)d;",
                       {'item_name': item_name,
                        'item_unit': item_unit,
                        'item_price': item_price,
                        'category': category,
                        'id': id})
        connection.commit()

    def delete(self,  id):

        cursor.execute("DELETE FROM StockItem WHERE id=%(id)d;",
                       {"id": id})
        connection.commit()


server = "DESKTOP-Q1O1S18\SQLEXPRESS"
connection = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={server};DATABASE=nfhcw2"
)  # TEMP, MUST BE REPLACED
cursor = connection.cursor()

login = Login()

stock_items = StockItems()

stock_categories_list= StockCategories()
#login.login(cursor)
