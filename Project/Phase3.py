#from bsddb3 import db
from csv import reader

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","time","summary","text"]
#infile = ['A,B,C,"D12121",E,F,G,H,"I9,I8",J,K']

#print reader(infile).next()
#database = db.DB()

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

def parseReview(reviewNumber):
    ####database = db.DB()
    #database.open("rw.idx")
    #review = database.get(reviewNumber).decode("utf-8")
    #reviewItems = reader(review).next()
    reviewItems = ["1","2","3","4","5","6","7","8","9","10"]
    parsedReview = dict(zip(reviewsColumns, reviewItems))
    print parsedReview

main()
