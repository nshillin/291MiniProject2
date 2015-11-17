#from bsddb3 import db
from csv import reader

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","time","summary","text"]

def main():
    while True:
        text = raw_input(':').lower()
        if text == "exit":
            return
        else:
            parseReview(0)
        #    parseQuery(text)


def parseQuery(text):
    queryList = text.split()

    validQuery = False

    if validQuery:
        pass
    else:
        print('"'+text+'" is not a valid query')


def executeQuery():
    pass
    #Return a list of reviews

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

def printReviews(reviews):
    for review in reviews:
        reviewDict = parseReview(review)
        for i in reviewDict:
            print i + ":" + reviewDict[i]
        print ''

main()
