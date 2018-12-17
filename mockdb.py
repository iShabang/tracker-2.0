import sqlite3
import dbfunctions

conn = sqlite3.connect('tracker.db')
c = conn.cursor()

values = [("chipotle", "2018-11-06", 8, 1),
          ("mcdonolds", "2018-11-04", 5.01, 1),
          ("canes", "2018-10-05", 10.25, 1),
          ("innout", "2018-09-03", 14.30, 1),
          ("chewy", "2018-08-02", 6.45, 1),
          ("phone case", "2018-11-09", 45.43, 2),
          ("headphones", "2018-11-08", 56.99, 2)]

dbfunctions.AddCategory(c, "Food")
dbfunctions.AddCategory(c, "Things")
dbfunctions.AddManyTrans(c,values)

c.execute("SELECT * FROM trans")
print(c.fetchall())

conn.commit()

conn.close()