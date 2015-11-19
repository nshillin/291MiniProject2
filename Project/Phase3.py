#from bsddb3 import db
from csv import reader

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","time","summary","text"]

def main():
    while True:
        text = raw_input(':').lower()
        if text == "":
            pass
        elif text == "exit":
            return
        else:
            parseQuery(text)


def parseQuery(text):
    queryList = text.split()
    i = 0
    while i < len(queryList):
        query = queryList[i]
        if (i+2 < len(queryList) and (queryList[i+1] == '<' or queryList[i+1] == '>')):
            query = queryList[i] + queryList[i+1] + queryList[i+2]
            i+=2
        elif (i+1 < len(queryList) and ('<' in queryList[i+1] or '>' in queryList[i+1] or '<' in queryList[i] or '>' in queryList[i])):
            query = queryList[i] + queryList[i+1]
            i+=1
        if ('<' in query) or ('>' in query):
            compareQuery(query)
        print query
        i+=1

    validQuery = False

    if validQuery:
        printReviews()
    else:
        print('"'+text+'" is not a valid query')

## Start of query handlers
# Query handlers should accept a command and
# Return a list of review keys

def compareQuery(query):
    reviewList = []
    return reviewList


## End of query handlers

# Turns Reviews into Dictionary
def parseReview(reviewNumber):
    #####database = db.DB()
    #database.open("rw.idx")
    #review = database.get(reviewNumber).decode("utf-8")
    #database.close()
    #reviewItems = reader(review).next()
    reviewItems = ["1","2","3","4","5","6","7","8","9","10"]
    reviewDict = dict(zip(reviewsColumns, reviewItems))
    return reviewDict

# Prints Reviews for User
def printReviews(reviews):
    for review in reviews:
        reviewDict = parseReview(review)
        for i in reviewDict:
            print i + ":" + reviewDict[i]
        print ''

main()
