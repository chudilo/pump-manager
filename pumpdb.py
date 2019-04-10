import os
import sqlite3

def createDataBase():
    os.remove("./pumpdb.sqlite")

    conn = sqlite3.connect('pumpdb.sqlite')
    curs = conn.cursor()

    curs.execute("""CREATE TABLE Player (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nickname VARCHAR)""")

    curs.execute("""CREATE TABLE Community (
                            idCommunity   INTEGER PRIMARY KEY,
                            nameCommunity VARCHAR
                            )""")

#    curs.execute

    curs.close()
    conn.close()

createDataBase()
