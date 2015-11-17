from bsddb3 import db

database = db.DB()
main()

def main():
    while True:
        text = raw_input(':').lower()
        if text == "exit":
            return
        else:
            queryParse(text)

def queryParse(text):
    query = ""
    validQuery = False
    if validQuery:
        berkeleyHandler(query)
    else:
        print('"'+text+'" is not a valid query')

def berkeleyHandler(query):
    database.open("")
    cur = database.cursor()
    database.close()
