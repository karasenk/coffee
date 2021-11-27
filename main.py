from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sys
import sqlite3


class CoffeeShop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.data = self.cur.execute("""SELECT * FROM coffee""").fetchall()
        self.loadTable()

    def loadTable(self):
        self.tbl.setColumnCount(7)
        self.tbl.setHorizontalHeaderLabels(['id', 'сорт', 'степень обжарки',
                                            'молотый/в зёрнах', 'описание вкуса',
                                            'цена', 'объём упаковки'])
        self.tbl.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                self.tbl.setItem(i, j, QTableWidgetItem(str(item)))
        self.tbl.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeShop()
    ex.show()
    sys.exit(app.exec_())
