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
        self.edit_btn.clicked.connect(self.editing)
        self.loadTable()

    def loadTable(self):
        data = self.cur.execute("""SELECT * FROM coffee""").fetchall()
        self.tbl.setColumnCount(7)
        self.tbl.setHorizontalHeaderLabels(['id', 'сорт', 'степень обжарки',
                                            'молотый/в зёрнах', 'описание вкуса',
                                            'цена', 'объём упаковки'])
        self.tbl.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.tbl.setItem(i, j, QTableWidgetItem(str(item)))
        self.tbl.resizeColumnsToContents()
    
    def editing(self):
        self.ed = Editing(self.con)
        self.ed.show()
    
    
class Editing(QMainWindow):
    def __init__(self, con):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = con
        self.cur = self.con.cursor()
        self.edit_btn.clicked.connect(self.edit)
        self.add_btn.clicked.connect(self.add)
        self.id_ed.textChanged.connect(self.find)
        self.request = """SELECT * FROM coffee
                        WHERE id = ?"""
        
    def find(self):
        info = self.cur.execute(self.request, (self.id_ed.text(),)).fetchone()
        if info:
            self.sort_ed.setText(info[1])
            self.roasting_ed.setText(info[2])
            self.grinding_ed.setText(info[3])
            self.taste_ed.setText(info[4])
            self.price_ed.setText(str(info[5]))
            self.volume_ed.setText(str(info[6]))
        else:
            self.sort_ed.setText('')
            self.roasting_ed.setText('')
            self.grinding_ed.setText('')
            self.taste_ed.setText('')
            self.price_ed.setText('')
            self.volume_ed.setText('')
            
    def edit(self):
        if self.sort_ed.text() and self.roasting_ed.text() and self.grinding_ed.text() and \
            self.taste_ed.text() and self.price_ed.text() and self.volume_ed.text():
            self.cur.execute("""UPDATE coffee SET sort = ?,
                                            roasting = ?,
                                            grinding = ?,
                                            taste = ?,
                                            price = ?,
                                            volume = ?
                                            WHERE id = ?""", (self.sort_ed.text(), self.roasting_ed.text(),
                                                              self.grinding_ed.text(), self.taste_ed.text(),
                                                              self.price_ed.text(), self.volume_ed.text(),
                                                              self.id_ed.text()))
            self.con.commit()
            ex.loadTable()
            
    def add(self):
        if self.sort_ed.text() and self.roasting_ed.text() and self.grinding_ed.text() and \
           self.taste_ed.text() and self.price_ed.text() and self.volume_ed.text():
            self.cur.execute("""INSERT INTO coffee(sort, roasting, grinding, taste, price, volume)
                                VALUES(?, ?, ?, ?, ?, ?)""", (self.sort_ed.text(), self.roasting_ed.text(),
                                                              self.grinding_ed.text(), self.taste_ed.text(),
                                                              self.price_ed.text(), self.volume_ed.text()))
            self.con.commit()
            ex.loadTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeShop()
    ex.show()
    sys.exit(app.exec_())
