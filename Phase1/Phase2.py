import sys
import re 
from bsddb3 import db 

def main():
    try: 
        fileName1 = str(sys.argv[1])
        fileName2 = str(sys.argv[2])
        fileName3 = str(sys.argv[3])
        fileName4 = str(sys.argv[4])
    except Exception as e:
        print("Expected more files in input.")
    

def sortFile(fileName, database):
    btree = false
    if filename != 'reviews.txt':
        sort = subprocess.Popen(['sort', fileName, '| uniq -u'], stdout = subprocess.PIPE)
        btree = true
        sort.stdout = open(filename, "w")
        createDatabase(btree, filename)
    else:
        createDatabase(btree, filename)

def createDatabase(btree, filename):
    if btree:
        createbTreeDatabase(filename)
    else :
        createHashDatabase(filename)

def createBTreeDatabase(filename):
    try:
        database = db.DB()
        database = db.DB()
        database.open("myDatabase", None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Database wouldn't open.")
    with open(filename, "r") as contents:
        file = contents.read().replace('\n', '')
        for line in file:
            print(line + 'Adding to database\n')
            indexOfKey = line.find(",")
            key = line[:indexOfKey+1]
            value = line[indexOfKey+1:]
            database.put(key, value)
    iterateDatabaseForTesting(database)

def createHashDatabase(filename):
    try:
        database = db.DB()
        database.open("myDatabase", None, db.DB_HASH, db.DB_CREATE)
    except:
        print("Database wouldn't open.")
    with open(filename, "r") as contents:
        file = contents.read().replace('\n', '')
        for line in file:
            print(line + 'Adding to database\n')
            indexOfKey = line.find(",")
            indexOfDescription = line.find(","[indexOfKey + 1])
            key = line[indexOfKey + 1:indexOfDescription]
            value = line[indexOfDescription+1:]
            database.put(key, value)
    iterateDatabaseForTesting(database)

def iterateDatabaseForTesting(database):
    cur = database.cursor()
    iter = cur.first()
    while iter:
        print(iter)
        iter = cur.next()
    cur.close()

            
