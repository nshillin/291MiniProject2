import sys,csv, re
from bsddb3 import db

def main():
    #print("I am totes working.")
    try: 
        filesList = ["reviews.txt","pterms.txt","rterms.txt","scores.txt"]
        for filename in filesList:
            sortFile(filename)
    except Exception as e:
        print("Phase 1 has not been run for the necessary text files.")

def sortFile(filename):
    btree = False
    if filename != 'reviews.txt':
        btree = True
        createDatabase(btree, filename)
    else:
        createDatabase(btree, filename)

def createDatabase(btree, filename):
    if btree:
        createBTreeDatabase(filename)
    else :
        createHashDatabase(filename)


def createBTreeDatabase(filename):
    if filename == "pterms.txt":
        createIndex2(filename)
    elif filename == "rterms.txt":
        createIndex3(filename)
    elif filename == "scores.txt":
        createIndex4(filename)
    return

#creates a bTree style database to store pterms.txt    
def createIndex2(filename):
    try:
        database = db.DB()
        database.set_flags(db.DB_DUP)
        database.open("pt.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Database wouldn't open for pt.idx.")
    with open(filename, "r") as contents:
        for line in contents:
            splitPoint = line.find(",")
            #print(line[:splitPoint] + "    value    "+ line[splitPoint + 1:-1])
            database.put(line[:splitPoint], line[splitPoint + 1:-1])
    #iterateDatabaseForTesting(database, "pt.idx")    

#creates a bTree style database for rterms.txt
def createIndex3(filename):
    try:
        database = db.DB()
        database.set_flags(db.DB_DUP)
        database.open("rt.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Database wouldn't open for rterms.txt.")
    with open(filename, "r") as contents:
        for line in contents:
            splitPoint = line.find(",")
            database.put(line[:splitPoint], line[splitPoint + 1:-1])  

#creates a bTree style database for scores.txt
def createIndex4(filename):
    try:
        database = db.DB()
        database.set_flags(db.DB_DUP)
        database.open("sc.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Database wouldn't open for sc.idx.")
    with open(filename, "r") as contents:
        for line in contents:
            splitPoint = line.find(",")
            database.put(line[:splitPoint], line[splitPoint + 1:-1])

#creates a hash style database for review.txt   
def createHashDatabase(filename):
    try:
        database = db.DB()
        database.open("rw.idx", None, db.DB_HASH, db.DB_CREATE)
    except:
        print("Database wouldn't open for rw.idx.")
    with open(filename, "r") as contents:
        for line in contents:
            splitPoint = line.find(",")
            #print(line[:splitPoint] + "    value    "+ line[splitPoint + 1:-1])
            database.put(line[:splitPoint], line[splitPoint + 1:-1])
 
def iterateDatabaseForTesting(database, databaseName):
    cur = database.cursor()
    iter = cur.first()
    while iter:
        print(iter)
        iter = cur.next()
    cur.close()
    #database.remove(databaseName)
    
main()

            
