import sys,csv, re
from bsddb3 import db 

def main():
    filesList = []
    #print("I am totes working.")
    try: 
	fileName1 = str(sys.argv[1])
	fileName2 = str(sys.argv[2])
	fileName3 = str(sys.argv[3])
	fileName4 = str(sys.argv[4])
	filesList.append(fileName1)
	print(fileName1 + " first file\n")
	filesList.append(fileName2)
	print(fileName2 + " second file\n")
	filesList.append(fileName3)
	print(fileName3 + " third file\n")
	filesList.append(fileName4)
	print(fileName4 + " fourth file\n")
	for filename in filesList:
	    print(filename)
	    sortFile(filename)
    except Exception as e:
	print("Expected more files in input.")
    

def sortFile(filename):
    #print("Thank goodness I made it!")
    btree = False
    #print(btree)
    #print(filename + " current file name\n")
    if filename != 'reviews.txt':
        sort = subprocess.Popen(['sort', fileName, '| uniq -u'], stdout = subprocess.PIPE)
        btree = True
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
        database.open("test", None, db.DB_BTREE, db.DB_CREATE)
    except:
        print("Database wouldn't open.")
    with open(filename, "r") as contents:
#        file = contents.readline().replace('\n', '')
        for line in contents:
            print(line + 'Adding to database\n')
            indexOfKey = line.find(",")
            key = line[:indexOfKey+1]
            value = line[indexOfKey+1:]
            database.put(key, value)
    iterateDatabaseForTesting(database)

def createHashDatabase(filename):
    try:
        database = db.DB()
        database.open("rw.idx", None, db.DB_HASH, db.DB_CREATE)
    except:
        print("Database wouldn't open.")
    with open(filename, "r") as contents:
        file = contents.read()
	#file = contents
	recordID = 1
	kv = 1
	entries = []
        for line in file:
	    if line == "\n":
	       #print("Blank Line.")
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
		 #print(value +  " value.")
		 entries = []
	       	 database.put(key, value)
	#database.put(recordID,key + ", "+ value)
	#iterateDatabaseForTesting(database)
	database.close()
            #indexOfKey = line.find(",")
            #indexOfDescription = line.find(","[indexOfKey + 1])
	   # if line == """ and kv == 0:
	    #     kv = kv + 1
	    #elif kv == 1 and line != """:
	     #    entries.append(line)
	    #elif kv == 1 and line == ":
             #  	 value = "".join(entries)
	#	 entries = []
	#	 kv = 0
	 #   elif line == "," and kv == 0:
	  #  	 kv = kv + 2
           # elif kv == 2 and line != ","
	    #	 entries.append(line)
	    #elif kv == 2 and line == ","
	    #	 key =


def iterateDatabaseForTesting(database):
    cur = database.cursor()
    iter = cur.first()
    while iter:
        print(iter)
        iter = cur.next()
    cur.close()

main()

            
