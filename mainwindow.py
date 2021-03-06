from PyQt5 import QtWidgets, QtGui, QtCore

import dbfunctions as db
import models
import uitools

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupWindow()
        self.setCurrentDate()
        self.setDateInterval()
        self.buildMenu()
        self.getCategories()
        self.buildCatDict()
        self.setHeaders(["ID","Name","Date","Amount","Category"])
        self.buildHeaderDict()
        self.getTransactions()
        self.buildStatList()
        self.buildFilter()
        model = models.MainTableModel(data=self.trans, headers=self.headers)
        self.setModel(model)
        self.setProxyModel(self.tableModel)
        self.mainTable = self.buildTable(model=self.tableModel, proxyModel=self.proxyModel)

        """Buttons"""
        self.addTransBttn = QtWidgets.QPushButton('Add Transaction', self)
        self.addTransBttn.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.addTransBttn.clicked.connect(self.openAddDialog)

        title = "Displaying: {} to {}".format(self.lowdate,self.highdate)
        self.titleLabel = QtWidgets.QLabel(self)
        self.setTitle(title)

        """Top Grid"""
        self.topGrid = QtWidgets.QGridLayout()
        self.topGrid.addWidget(self.spentLabel,0,0)
        self.topGrid.addWidget(self.earnedLabel,1,0)
        self.topGrid.addWidget(self.savedLabel,2,0)
        self.topGrid.addWidget(self.addTransBttn,0,2,3,1)
        self.topGrid.addWidget(self.spentEdit,0,1)
        self.topGrid.addWidget(self.earnedEdit,1,1)
        self.topGrid.addWidget(self.savedEdit,2,1)
        self.topGrid.addWidget(self.titleLabel,2,3)
        self.topGrid.addWidget(self.filterLabel,2,4)
        self.topGrid.addWidget(self.filterComboBox,2,5)
        self.topGrid.addWidget(self.filterEdit,2,6)
        self.topGrid.setColumnStretch(3,1)

        """Main Layout"""
        self._mainvbox = QtWidgets.QVBoxLayout()
        self._mainvbox.addLayout(self.topGrid)
        self._mainvbox.addWidget(self.mainTable)
        self._mainWidget = QtWidgets.QWidget()
        self._mainWidget.setLayout(self._mainvbox)
        self.setCentralWidget(self._mainWidget)

    def setupWindow(self):
        self.setWindowTitle("Full Test Application")
        self.resize(QtWidgets.QDesktopWidget().availableGeometry().size()*0.7)
        self.centerScreen(self)

    def centerScreen(self, widget):
        rectangle = widget.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(centerPoint)
        widget.move(rectangle.topLeft())

    def buildMenu(self):
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        self.editMenu = self.mainMenu.addMenu('Edit')
        self.reportMenu = self.mainMenu.addMenu('Report')

        self.createActions()

        self.fileMenu.addAction(self.addCatAct)
        self.editMenu.addAction(self.catWindow)
        self.editMenu.addAction(self.delAct)
        self.reportMenu.addAction('Week')
        self.reportMenu.addAction('Month')
        self.reportMenu.addAction('Year')

    def createActions(self):
        self.printAct = QtWidgets.QAction()
        self.printAct.setText("Print")
        
        self.addCatAct = QtWidgets.QAction()
        self.addCatAct.setText("Add Category")
        self.addCatAct.triggered.connect(self.addCatDialog)

        self.delAct = QtWidgets.QAction()
        self.delAct.setText("Delete")
        self.delAct.triggered.connect(self.deleteTrans)

        self.catWindow = QtWidgets.QAction()
        self.catWindow.setText("Categories")
        self.catWindow.triggered.connect(self.categoryDialog)

    def setTitle(self, title):
        self.titleLabel.setText(title)

    def setHeaders(self, headers):
        self.headers = headers

    def setModel(self, model):
        self.tableModel = model

    def setProxyModel(self, model):
        self.proxyModel = models.floatProxyModel()
        self.proxyModel.setSourceModel(model)


    def setDateInterval(self, thisMonth = True, lowdate = None, highdate = None): 
        if not thisMonth:
            self.lowdate = lowdate
            self.highdate = highdate
        else:
            self.lowdate = self.currentDate.toString("yyyy-MM-01")
            self.highdate = self.currentDate.toString("yyyy-MM-dd")

    def setCurrentDate(self):
        self.currentDate = QtCore.QDate.currentDate()

    def getTransactions(self):
        query = db.getTransByDate(lowdate=self.lowdate, highdate=self.highdate)
        self.trans = [list(i) for i in query]

    def getCategories(self):
        query = db.GetAllCategories()
        self.categories = [list(i) for i in query]

    def getSelectedRows(self, table):
        selectedRows = table.selectionModel().selectedRows()
        indices = []
        for i in selectedRows:
            indices.append(i.row())
        indices.sort()
        return indices
        
    def buildCatDict(self):
        self._categoriesDict = {}
        for row in self.categories:
            self._categoriesDict[row[1]] = row[0]

    def buildHeaderDict(self):
        self._headerDict = dict(zip(self.headers,range(len(self.headers))))    

    def buildTable(self, model, proxyModel):
        table = QtWidgets.QTableView()
        table.setModel(proxyModel)
        if not model.columnCount() == 0:
            self.stretchTableHeaders(table, model.columnCount())
        table.setSortingEnabled(True)
        proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        return table

    def buildStatList(self):
        if self.isEmpty():
            data = []
        else:
            self.calcStats()
            data = self.stats
        self.statList = QtWidgets.QTableView()
        self.listModel = models.StatModel(data=data)
        self.statList.setModel(self.listModel)
        self.spentLabel = QtWidgets.QLabel('Spent:')
        self.earnedLabel = QtWidgets.QLabel('Earned:')
        self.savedLabel = QtWidgets.QLabel('Saved:')
        self.spentEdit = QtWidgets.QLineEdit()
        self.earnedEdit = QtWidgets.QLineEdit()
        self.savedEdit = QtWidgets.QLineEdit()
        self._mapper = QtWidgets.QDataWidgetMapper()
        self._mapper.setModel(self.listModel)
        self._mapper.addMapping(self.spentEdit, 0)
        self._mapper.addMapping(self.earnedEdit, 1)
        self._mapper.addMapping(self.savedEdit, 2)
        self._mapper.toFirst()

    def calcStats(self):
        amountSpent = db.totalSpent(self.lowdate,self.highdate)[0]
        amountEarned = db.totalEarned(self.lowdate,self.highdate)[0]
        amountSaved = float(amountEarned) - float(amountSpent)
        self.stats = [[amountSpent,amountEarned,str(round(amountSaved,2))]]
        
    def isEmpty(self):
        if len(self.trans) == 0:
            return True
        return False

    def headerComboBox(self):
        comboBox = QtWidgets.QComboBox()
        for header in self.headers:
            comboBox.addItem(header)
        return comboBox

    def buildFilter(self):
        self.filterLabel = QtWidgets.QLabel('Filter')
        self.filterComboBox = self.headerComboBox()
        self.filterEdit = QtWidgets.QLineEdit()
        self.filterEdit.setPlaceholderText('Enter Text')

        def filterTable():
            self.proxyModel.setFilterKeyColumn(self._headerDict[self.filterComboBox.currentText()])
            self.proxyModel.setFilterRegExp(self.filterEdit.text())

        self.filterEdit.textChanged.connect(filterTable)

    def categoryDialog(self):
        catDialog = QtWidgets.QDialog()
        catDialog.setWindowTitle("Categories")
        catDialog.resize(QtWidgets.QDesktopWidget().availableGeometry().size()*0.5)
        self.centerScreen(catDialog)
        model = models.CatTableModel(data=self.categories, headers=["ID","Name","Income"])
        proxyModel = QtCore.QSortFilterProxyModel()
        proxyModel.setSourceModel(model)
        catTable = self.buildTable(model, proxyModel)
        addButton = QtWidgets.QPushButton("Add",catDialog)
        addButton.clicked.connect(self.addCatDialog)

        def deleteCategory():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Would you like to delete all items under this category?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            test = msgBox.exec_()
            if test == QtWidgets.QMessageBox.Yes:
                cascade = True
            else:
                cascade = False
            self.deleteRows(catTable,model,"cat",cascade)

        deleteButton = QtWidgets.QPushButton("Delete", catDialog)
        deleteButton.clicked.connect(deleteCategory)
        closeButton = QtWidgets.QPushButton("Close", catDialog)
        closeButton.clicked.connect(catDialog.close)
        toplayout = QtWidgets.QHBoxLayout()
        toplayout.addWidget(addButton)
        toplayout.addWidget(deleteButton)
        mainlayout = QtWidgets.QVBoxLayout() 
        mainlayout.addLayout(toplayout)
        mainlayout.addWidget(catTable)
        mainlayout.addWidget(closeButton)
        catDialog.setLayout(mainlayout)
        catDialog.exec_()

    def datePopup(self):
        dateEdit = QtWidgets.QDateEdit()
        dateEdit.setDate(self.currentDate)
        dateEdit.setCalendarPopup(True)
        dateEdit.setDisplayFormat('yyyy-MM-dd')
        return dateEdit
    
    def stretchTableHeaders(self, table, numColumns):
        header = table.horizontalHeader()
        for i in range(numColumns):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    def deleteTrans(self):
        self.deleteRows(self.mainTable, self.tableModel, "trans")
        self.calcStats()
        self.listModel.changeData(self.stats)
        

    def deleteRows(self, table, model, itemType, cascade=False):
        selectedRows = table.selectionModel().selectedRows()
        indices = []
        for i in selectedRows:
            indices.append(i.row())
        indices.sort()
        difference = 0
        for index in indices:
            row = index-difference
            model.removeRows(row=row,count=1, itemType=itemType, cascade=cascade)
            difference += 1

    def openAddDialog(self):
        addWindow = QtWidgets.QDialog()
        addWindow.setWindowTitle("Adding Transaction")
        self.centerScreen(addWindow)
        edit_name = QtWidgets.QLineEdit()
        edit_name.setPlaceholderText('Name')
        check_float = QtGui.QDoubleValidator()
        check_float.setDecimals(2)
        edit_amount = QtWidgets.QLineEdit()
        edit_amount.setValidator(check_float)
        edit_amount.setPlaceholderText('Price')
        comboBox_category = QtWidgets.QComboBox()
        for row in self.categories:
            comboBox_category.addItem(row[1])
        edit_date = self.datePopup()
        addButton = QtWidgets.QPushButton('Submit', addWindow)
        cancelButton = QtWidgets.QPushButton('Cancel', addWindow)

        def submit():
            name = edit_name.text()
            date = edit_date.text()
            amount = edit_amount.text()
            category = comboBox_category.currentText()
            transaction = [name,date,float(amount), self._categoriesDict[category]]
            position = self.tableModel.rowCount()
            self.tableModel.insertRows(position, 1, data=transaction)
            self.calcStats()
            self.listModel.changeData(self.stats)
            addWindow.close()

        addButton.clicked.connect(submit)
        cancelButton.clicked.connect(addWindow.close)
        mainlayout = QtWidgets.QVBoxLayout()
        buttonlayout = QtWidgets.QHBoxLayout()
        buttonlayout.addWidget(addButton)
        buttonlayout.addWidget(cancelButton)
        mainlayout.addWidget(edit_date)
        mainlayout.addWidget(edit_name)
        mainlayout.addWidget(edit_amount)
        mainlayout.addWidget(comboBox_category)
        mainlayout.addLayout(buttonlayout)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()
        
    def addCatDialog(self):
        addWindow = QtWidgets.QDialog()
        addWindow.setWindowTitle("Adding Category")
        self.centerScreen(addWindow)
        edit_category = QtWidgets.QLineEdit()
        edit_category.setPlaceholderText('Category')
        checkBox_income = QtWidgets.QCheckBox('Income')
        addButton = QtWidgets.QPushButton('Submit', addWindow)
        cancelButton = QtWidgets.QPushButton('Cancel', addWindow)

        def submit():
            category = edit_category.text()
            income = 0
            if checkBox_income.isChecked():
                income = 1
            db.AddCategory(name=category, income=income)
            addWindow.close()


        addButton.clicked.connect(submit)
        cancelButton.clicked.connect(addWindow.close)
        mainlayout = QtWidgets.QVBoxLayout()
        buttonlayout = QtWidgets.QVBoxLayout()
        buttonlayout.addWidget(addButton)
        buttonlayout.addWidget(cancelButton)
        mainlayout.addWidget(edit_category)
        mainlayout.addWidget(checkBox_income)
        mainlayout.addLayout(buttonlayout)
        addWindow.setLayout(mainlayout)
        addWindow.exec_()

