from PyQt5 import QtCore, QtWidgets, QtGui
import dbfunctions


class tableModel(QtCore.QAbstractTableModel):
    def __init__(self, data = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.__data = data
        self.__headers = headers

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        return len(self.__data[0])

    def data(self, index, role):
        
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__data[row][column]
            return value

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        #insert stuff

        self.endInsertRows()

        return True

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
            if orientation == QtCore.Qt.Vertical:
                return "  "


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    data = dbfunctions.GetTransByDateInterval(lowdate='2017-00-00', highdate='2019-00-00')
    headers = ["Transaction ID", "Name", "Date", "Amount", "Category"]

    tableView = QtWidgets.QTableView()
    tableView.show()
    tableModel = tableModel(data=data, headers=headers)
    tableModel.insertRows(0,1)
    tableView.setModel(tableModel)

    app.exec_()
