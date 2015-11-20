import sys,csv, re
from bsddb3 import db 

def main():
    filesList = []
    #print("I am totes working.")
    try: 
        fileName1 = "reviews.txt"
        fileName2 = "pterms.txt"
        fileName3 = "rterms.txt"
        fileName4 = "scores.txt"
        filesList.append(fileName1)
	#print(fileName1 + " first file\n")
        filesList.append(fileName2)
	#print(fileName2 + " second file\n")
        filesList.append(fileName3)
	#print(fileName3 + " third file\n")
        filesList.append(fileName4)
	#print(fileName4 + " fourth file\n")
        for filename in filesList:
            sortFile(filename)
    except Exception as e:
        print("Phase 1 has not been run for the necessary text files.")

def sortLines(filename):
    file = open(filename, "r").read()
    lines = file.split("\n")
    lines.sort()
   # for line in lines:
	#print("I am having difficulties reaching this point, durrr sort lines")
	#print(line)
    #file.close()
    return "\n".join(lines)

def sortFile(filename):
    #print("Thank goodness I made it!")
    btree = False
    #print(btree)
    #print(filename + " current file name\n")
    if filename != 'reviews.txt':
	#sortedFile = open(filename, "w")
        #sort = sortLines(filename)
        #print(sort)
	#sortedFile.write()
	#sort = subprocess.Popen(['sort', fileName, '| uniq -u'], stdout = subprocess.PIPE)
        #print("I am having difficulties reaching this point, durrr")
        btree = True
        #for item in sort:
	    #print(item)
        #sort.stdout = open(filename, "w")
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
    else :
	print("Invalid file name.")
    return
    
def createIndex2(filename):
    try:
	database = db.DB()
	database.set_flags(db.DB_DUP)
	database.open("pt.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
	print("Database wouldn't open for pt.idx.")
    with open(filename, "r") as contents:
	entries = []
	for line in contents.read():
	    if line != "\n" and line != ",":
		entries.append(line)
	    elif line == "\n":
		value = "".join(entries)
		#print("key :" + key + " value: " + value)
		database.put(key, value)
		entries = []
	    elif line == ",":
		key = "".join(entries)
		entries = []
    #iterateDatabaseForTesting(database, "pt.idx")    

def createIndex3(filename):
    try:
	database = db.DB()
	database.set_flags(db.DB_DUP)
	database.open("rt.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
	print("Database wouldn't open for rterms.txt.")
    with open(filename, "r") as contents:
	entries = []
	for line in contents.read():
	    #print(line + ": line" )
	    if line != "\n" and line != ",":
		entries.append(line)
	    elif line == "\n":
		value = "".join(entries)
		database.put(key, value)
		entries = []
	    elif line == ",":
		key = "".join(entries)
		entries = []
	#iterateDatabaseForTesting(database, "rt.idx")    

def createIndex4(filename):
    try:
	database = db.DB()
	database.set_flags(db.DB_DUP)
	database.open("sc.idx", None, db.DB_BTREE, db.DB_CREATE)
    except:
	print("Database wouldn't open for sc.idx.")
    with open(filename, "r") as contents:
	entries = []
	for line in contents.read():
	    #print(line + ": line" )
	    if line != "\n" and line != ",":
		entries.append(line)
	    elif line == "\n":
		value = "".join(entries)
		database.put(key, value)
		entries = []
	    elif line == ",":
		key = "".join(entries)
		entries = []
	#iterateDatabaseForTesting(database, "sc.idx")    

'''def createHashDatabase(filename):
    try:
        database = db.DB()
        database.open("rw.idx", None, db.DB_HASH, db.DB_CREATE)
    except:
        print("Database wouldn't open for rw.idx.")
    with open(filename, "r") as contents:
        file = contents.read()
	#file = contents
	recordID = 1
	kv = 1
	entries = []
        for line in file:
	    if line == "\n":
	       kv = 1
	       value = "".join(entries)
	       entries = []
	       newval = key + " " +  value
	       database.put(str(recordID),newval)
	       recordID = recordID + 1
	    if line == recordID and kv == 0:
	       	 kv = 1
	    elif line == "," and kv == 1:
	    	 kv = 2
	    elif line != "," and kv == 2:
	    	 entries.append(line)
	    elif line == "," and kv == 2:
	    	 key = "".join(entries)
		 kv = 1
		 #print(key + 'Adding to database\n')
		 entries = []
	    elif line == '"' and kv == 1:
	    	 kv = 3
	    elif line != '"' and kv == 3:
	    	 entries.append(line)
	    elif line == "\n" and kv == 3:
	    	 value = "".join(entries)
		 kv = 1
		 recordID = recordID + 1
		 entries = []
	       	 database.put(key, value)
	#iterateDatabaseForTesting(database, "rw.idx")
	database.close()'''
	
def createHashDatabase(filename):
    try:
        database = db.DB()
        database.open("rw.idx", None, db.DB_HASH, db.DB_CREATE)
    except:
        print("Database wouldn't open for rw.idx.")
    with open(filename, "r") as contents:
	file = contents.read()
	entries = []
	reviewID = 1
	inValue = False;
	for line in file:
	    if line == "\n":
	        #print("\n" + str(reviewID) + "\n")
		value = "".join(entries)
		#print("I AM YOUR REVIEW. " + str(reviewID) + value)
		database.put(str(reviewID),value)
		reviewID += 1
		entries = []
		inValue = False
	    elif line == "," and not inValue:
		inValue = True
	    elif inValue:
		entries.append(line)
		


def iterateDatabaseForTesting(database, databaseName):
    cur = database.cursor()
    iter = cur.first()
    while iter:
        print(iter)
        iter = cur.next()
    cur.close()
    #database.remove(databaseName)
    
main()

            
