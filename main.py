import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.coffee_db = sqlite3.connect('coffee.db')
        self.cur = self.coffee_db.cursor()
        self.pushButton.clicked.connect(self.second_form)
        self.table()

    def table(self):
        self.load_table = load_table(self.cur, self.tableWidget)

    def second_form(self):
        self.edit_table = EditTable(self.coffee_db)
        self.hide()
        self.edit_table.show()


class EditTable(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.cur = self.db.cursor()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.close)
        self.table()

    def table(self):
        self.load_table = load_table(self.cur, self.tableWidget)

    def add(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)


    def close(self):
        for i in range(self.tableWidget.rowCount()):
            if i < self.load_table:
                self.cur.execute('''UPDATE coffee SET SortName =?, Roasting =?, MilledGrains =?,
                                 Taste =?, Price =?, Mass =? WHERE id =?''',
                                     (self.tableWidget.item(i, 1).text(),
                                      self.tableWidget.item(i, 2).text(),
                                      self.tableWidget.item(i, 3).text(),
                                      self.tableWidget.item(i, 4).text(),
                                      self.tableWidget.item(i, 5).text(),
                                      self.tableWidget.item(i, 6).text(), i + 1,))
            else:
                self.cur.execute('''INSERT INTO coffee(id,SortName,Roasting,MilledGrains,
                                    Taste,Price,Mass) VALUES(?,?,?,?,?,?,?)''',
                                 (i + 1, self.tableWidget.item(i, 1).text(),
                                 self.tableWidget.item(i, 2).text(),
                                 self.tableWidget.item(i, 3).text(),
                                 self.tableWidget.item(i, 4).text(),
                                 self.tableWidget.item(i, 5).text(),
                                 self.tableWidget.item(i, 6).text(),))
                self.db.commit()
        self.hide()
        coffee.table()
        coffee.show()


def load_table(cur, table):
    data = cur.execute('SELECT * FROM coffee').fetchall()
    if table.rowCount() != len(data):
        table.setRowCount(len(data))
    for i, elem in enumerate(data):
        elems = list(elem)
        for j, item in enumerate(elems):
            table.setItem(i, j, QTableWidgetItem(str(item)))
    return len(data)


app = QApplication(sys.argv)
coffee = Coffee()
coffee.show()
sys.exit(app.exec_())
