import sqlite3
import dbfunctions

values = [("chipotle", "2018-11-06", 8, 1),
          ("mcdonolds", "2018-11-04", 5.01, 1),
          ("canes", "2018-10-05", 10.25, 1),
          ("innout", "2018-09-03", 14.30, 1),
          ("chewy", "2018-08-02", 6.45, 1),
          ("phone case", "2018-11-09", 45.43, 2),
          ("headphones", "2018-11-08", 56.99, 2),
          ("Check","2018-12-27", 500.00, 3),
          ("Armor All", "2019-01-12", 4.97, 2),
          ("Ramen", "2019-01-12", 0.25, 1),
          ("Teryaki Rice", "2019-01-12", 1.50, 1),
          ("Dozen Eggs", "2019-01-12", 1.48, 1),
          ("Milk", "2019-01-12", 1.55, 1),
          ("Chicken", "2019-01-12", 5.30, 1),
          ("Water", "2019-01-12", 3.98, 1),
          ("Haircut", "2017-09-02", 76.36, 2),
          ("Parking", "2017-09-02", 4.00, 2),
          ("Circle K", "2017-09-02", 2.29, 1),
          ("Chewy Boba", "2017-09-05", 9.28, 1),
          ("Chewy Boba", "2017-09-07", 4.15, 1),
          ("Walgreens", "2017-09-08", 6.28, 1),
          ("Steak & Shake", "2017-09-11", 5.40, 1),
          ("UPS", "2017-09-11", 5.96, 2),
          ("Chewy Boba", "2017-09-13", 6.91, 1),
          ("Smashburger", "2017-09-14", 4.64, 1),
          ("Vons", "2017-09-14", 8.48, 1),
          ("Chipotle", "2017-09-15", 7.52, 1),
          ("Hotel", "2017-09-15", 102.13, 2),
          ("Disney Ticket", "2017-09-16", 110.00, 2),
          ("In-N-Out", "2017-09-15", 7.97, 1),
          ("Soho", "2017-09-14", 8.12, 1),
          ("Disney Parking", "2017-09-16", 20.00, 2),
          ("Locker", "2017-09-16", 3.50, 2),
          ("Disney Charm", "2017-09-16", 75.43, 2),
          ("Rancho Del Zocalo", "2017-09-17", 19.37, 1),
          ("Mint Julep", "2017-09-16", 2.42, 1),
          ("Bengal BBQ", "2017-09-16", 9.00, 1),
          ("Ice Cream", "2017-09-16", 7.00, 1),
          ("Plaza Inn", "2017-09-16", 20.50, 1),
          ("Candy Palace", "2017-09-16", 21.53, 1),
          ("Mix It Up", "2017-09-17", 11.85, 1),
          ("Canes", "2017-09-19", 7.78, 1),
          ("Setebello", "2017-09-19", 29.23, 1),
          ("Sonic", "2017-09-19", 5.28, 1),
          ("Chewy Boba", "2017-09-20", 4.60, 1),
          ("Chewy Boba", "2017-09-27", 4.60, 1),
          ("Walmart", "2017-09-27", 1.48, 1),
          ("Overwatch", "2017-09-29", 30.00, 2),
          ("Check", "2017-09-29", 500.00, 3),
          ("Chipotle", "2017-09-29", 7.52, 1)]

dbfunctions.AddCategory(name="Food", income=0)
dbfunctions.AddCategory(name="Things", income=0)
dbfunctions.AddCategory(name="Income", income=1)
dbfunctions.AddManyTrans(values=values)
