from bsddb3 import db

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","time","summary","text"]

database = db.DB()
main()

def main():
    while True:
        text = raw_input(':').lower()
        if text == "exit":
            return
        else:
            queryParser(text)

def queryParser(text):
    validQuery = False
    if validQuery:
        berkeleyHandler(query)
    else:
        print('"'+text+'" is not a valid query')

def reviewParser(review):
    parsedReview = {}
    for c in reviewsColumns:
        parsedReview[c] = ""
