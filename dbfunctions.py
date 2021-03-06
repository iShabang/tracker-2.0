import sqlite3

def DbConnectQuery(func):
    def wrapper(*args,**kwargs):
        connection = sqlite3.connect('tracker.db')
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") 
        data = func(cursor,*args,**kwargs)
        connection.close()
        return data
    return wrapper

def DbConnectAction(func):
    def wrapper(*args,**kwargs):
        connection = sqlite3.connect('tracker.db')
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") 
        func(cursor,*args,**kwargs)
        connection.commit()
        connection.close()
    return wrapper


################################################################
#ADD and DELETE
################################################################
@DbConnectAction
def AddTrans(cursor, values):
    cursor.execute("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", values)

@DbConnectAction
def AddManyTrans(cursor, values):
    cursor.executemany("INSERT INTO trans(name, date, amount, cat_id) VALUES (?,?,?,?);", values)

@DbConnectAction
def delTransByID(cursor, id_num):
    cursor.execute("DELETE FROM trans WHERE trans_id=?;", (id_num,))

@DbConnectAction
def delTransByCat(cursor, cat_id):
    cursor.execute("DELETE FROM trans WHERE cat_id=?;", (cat_id,))

@DbConnectAction
def AddCategory(cursor, name, income):
    cursor.execute("INSERT INTO category(name, income) VALUES (?,?);", (name,income))

@DbConnectAction
def delCategoryByID(cursor, cat_id):
    cursor.execute("DELETE FROM category WHERE cat_id=?;", (cat_id,))

@DbConnectAction
def AddBill(cursor, values):
    cursor.execute("INSERT INTO bills(due_date,amount_due,cat_id,last_payment) VALUES (?,?,?,?)", (values,))

@DbConnectAction
def DelBill(cursor, bill_id):
    cursor.execute("DELETE FROM bills WHERE bill_id=?", (bill_id,))


################################################################
#Queries
################################################################
@DbConnectQuery
def findTransCategory(cursor, trans_id):
    cursor.execute('''
    SELECT trans.cat_id
    FROM trans
    WHERE trans.trans_id = ?''',(trans_id,))
    return cursor.fetchone()

@DbConnectQuery
def getCatID(cursor, name):
    cursor.execute('''
    SELECT category.cat_id
    FROM category
    WHERE category.name = ?;''',(name,))
    return cursor.fetchone()

@DbConnectQuery
def totalEarned(cursor, lowdate, highdate):
    cursor.execute('''
    SELECT printf("%.2f",SUM(trans.amount))
    FROM trans LEFT JOIN category ON trans.cat_id = category.cat_id
    WHERE category.income = 1 AND date >= ? AND date <= ?''',(lowdate,highdate))
    return cursor.fetchone()

@DbConnectQuery
def totalSpent(cursor, lowdate, highdate):
    cursor.execute('''
    SELECT printf("%.2f",SUM(trans.amount))
    FROM trans LEFT JOIN category ON trans.cat_id = category.cat_id
    WHERE category.income = 0 AND date >= ? AND date <= ?''',(lowdate,highdate))
    return cursor.fetchone()

@DbConnectQuery
def getLastTrans(cursor):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, printf("%.2f",trans.amount), category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE trans.trans_id = (SELECT MAX(trans.trans_id) FROM trans)''')
    return cursor.fetchone()

@DbConnectQuery
def getTransByDate(cursor, lowdate, highdate):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, printf("%.2f", trans.amount), category.name
    FROM trans LEFT JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?''',(lowdate,highdate))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByName(cursor, name):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE name LIKE ?''', (name,))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByNameDate(cursor, name, lowdate, highdate):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?
    AND name LIKE ?''', (lowdate,highdate, name))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByCategory(cursor, cat_id):
    cursor.execute('''
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE cat_id=?''', (cat_id,))
    return cursor.fetchall()

@DbConnectQuery
def GetTransByCategoryDate(cursor, cat_id, lowdate, highdate):
    cursor.execute("""
    SELECT trans.trans_id, trans.name, trans.date, trans.amount, category.name
    FROM trans INNER JOIN category ON trans.cat_id = category.cat_id
    WHERE date >= ? AND date <= ?
    AND cat_id=?""", (lowdate, highdate, cat_id))
    return cursor.fetchall()

@DbConnectQuery
def GetAllCategories(cursor):
    cursor.execute("""
    SELECT cat_id, name, income
    FROM category""")
    return cursor.fetchall()

@DbConnectQuery
def getCatNamesType(cursor):
    cursor.execute("""
    SELECT category.name, category.income
    FROM category""")
    return cursor.fetchall()

################################################################
#UPDATE Statements
################################################################
@DbConnectAction
def updateTrans(cursor, transId, name, date, amount, catId):
    cursor.execute('''
    UPDATE trans
    SET name=?, date=?, amount=?, cat_id=?
    WHERE trans_id = ?;''', (name,date,amount,catId,transId))

@DbConnectAction
def updateCat(cursor, cat_id, name, income):
    cursor.execute('''
    UPDATE category
    SET name=?, income=?
    WHERE cat_id = ?;''', (name,income,cat_id))

