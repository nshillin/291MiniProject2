#from bsddb3 import db
from csv import reader
import datetime
import re

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","date","summary","text"]

class QueryData:
	def __init__(self):
		#Terms to be checked
		self.termsP = []
		self.termsR = []
		#Value must be > value 0, < value 1
		self.ranges = {
		'rscore': [None, None],
		'pprice': [None, None],
		'rdate': [None, None]
		}

	def date_update(oper, dateStr):
		#Updates the rdate values.
		if oper == '>':
			original = self.ranges['rdate'][0]
			if original is None or compareTwoItems(datetime.datetime.strptime(dateStr, "%Y/%m/%d"), oper, datetime.datetime.strptime(original, "%Y/%m/%d")):
				self.ranges['rdate'][0] = dateStr;
		elif oper == '<':
			original = self.ranges['rdate'][1]
			if original is None or compareTwoItems(datetime.datetime.strptime(dateStr, "%Y/%m/%d"), oper, datetime.datetime.strptime(original, "%Y/%m/%d")):
				self.ranges['rdate'][1] = dateStr;
		return

	def value_update(fieldStr, oper, valueStr):
		#Updates the rscore or pprice values.
		if oper == '>':
			original = self.ranges[fieldStr][0]
			if original is None or compareTwoItems(float(valueStr), oper, float(original)):
				self.ranges[fieldStr][0] = valueStr;
		elif oper == '<':
			original = self.ranges[fieldStr][1]
			if original is None or compareTwoItems(float(valueStr), oper, float(original)):
				self.ranges[fieldStr][1] = valueStr;
		return

	def term_update(fieldStr, termStr):
		#Adds terms.
		if fieldStr is None:
			#TODO: figure this out
			return
		elif fieldStr == 'p:':
			termsP.append(termStr)
		elif fieldStr == 'r:':
			termsR.append(termStr)

	def date_update(oper, dateStr):
		#TODO: write this
		pass
		return

	def value_update(fieldStr, oper, valueStr):
		#TODO: write this
		pass
		return

	def term_update(fieldStr, termStr):
		if fieldStr is None:
			#TODO: figure this out
			pass
			return
		elif fieldStr == 'p:':
			termsP.append(termStr)
		elif fieldStr == 'r:':
			termsR.append(termStr)

def main():
	while True:
		text = raw_input(':').lower()
		if text.strip(' ') == "":
			pass
		elif text == "exit":
			return
		else:
			queryData = parseQuery(text)
			if queryData is None:
				print('Invalid query.')
			else:
				#TODO: Put search stuff here
				pass


'''
def parseQuery(text):
    queryList = text.split()
    organizedQueryList = organizeQueries(queryList)
    if len(organizedQueryList) == 0:
        return
    reviewList = [1]
    for query in organizedQueryList:
        if ('<' in query) or ('>' in query):
            reviewList = compareQuery(query, reviewList)
        print reviewList
        # Some other query type

    printReviews(reviewList)
'''

def parseQuery(text):
    regex_date = '^\s*rdate\s*([<>])\s*(\d{4}[/]\d{2}[/]\d{2})(\s+|\Z)'
    regex_value = '^\s*(rscore|pprice)\s*([<>])\s*([-]?\d+([.]\d+)?)(\s+|\Z)'
    regex_term = '^\s*([pr]:)?(\w+[%]?)(\s+|\Z)'

    data = QueryData()

    while len(text) > 0:
		matcher = re.search(regex_date, text)
		if matcher is not None:
			QueryData.date_update(matcher.group(1), matcher.group(2))
			re.sub(regex_date, '', text)
			continue
		matcher = re.search(regex_value, text)
		if matcher is not None:
			QueryData.value_update(matcher.group(1), matcher.group(2), matcher.group(3))
			re.sub(regex_value, '', text)
			continue
		matcher = re.search(regex_term, text)
		if matcher is not None:
			QueryData.term_update(matcher.group(1), matcher.group(2))
			re.sub(regex_term, '', text)
			continue
		else:
			return None
    return data


#### Fixes < and > queries, as well as adds them to the end of the organizedQueryList
# ,this is used to increase efficiency, as < and > require going through all of
# the reviews, whereas other commands can just find the key and immediately find
# the result
def organizeQueries(queryList):
    organizedQueryList = []
    i = 0
    while i < len(queryList):
        query = queryList[i]
        if (i+2 < len(queryList) and (queryList[i+1] == '<' or queryList[i+1] == '>')):
            query = queryList[i] + queryList[i+1] + queryList[i+2]
            i+=2
        elif (i+1 < len(queryList) and ('<' in queryList[i+1] or '>' in queryList[i+1] or '<' in queryList[i] or '>' in queryList[i])):
            query = queryList[i] + queryList[i+1]
            i+=1

        # Something should be here to stop invalid queries
        if False:
            print('"'+text+'" is not a valid query')
            return []

        if ('<' in query) or ('>' in query):
            organizedQueryList.append(query)
        else:
            organizedQueryList.insert(0,query)
        i+=1
    return organizedQueryList


## Start of query handlers
# Query handlers should accept a command and

# Return a list of review keys
def compareQuery(query, reviewList):
    if '<' in query:
        comparator = '<'
        query = query.replace('<', '')
    elif '>' in query:
        comparator = '>'
        query = query.replace('>', '')

    if "rscore" in query:
        query = query.replace('rscore','')
        reviewList = compare_rscore(query, comparator)
    elif "rdate" in query:
        query = query.replace('rdate','')
        reviewList = compare_rdate(query, comparator, reviewList)
    elif "pprice" in query:
        query = query.replace('pprice','')
        reviewList = compare_pprice(query, comparator, reviewList)

    return reviewList

def compare_rscore(item2String, comparator):
    item2 = float(item2String)
    # grab all rscores from bd as item1
    compareTwoItems(item1, comparator, item2)
    return reviewList

def compare_rdate(item2String, comparator, reviewList):
    updatedReviewList = []
    item2 = datetime.datetime.strptime(item2String, "%Y/%m/%d")
    for i in reviewList:
        review = parseReview(i)
        item1 = datetime.datetime.strptime(review['date'], "%Y/%m/%d")
        if compareTwoItems(item1, comparator,item2):
            updatedReviewList.append(i)
    return updatedReviewList

def compare_pprice(item2String, comparator, reviewList):
    updatedReviewList = []
    item2 = float(item2String)
    for i in reviewList:
        review = parseReview(i)
        item1 = float(review['price'])
        if compareTwoItems(item1, comparator,item2):
            updatedReviewList.append(i)
    return updatedReviewList

def compareTwoItems(item1,comparator,item2):
    if comparator == '<':
        return item1 < item2
    elif comparator == '>':
        return item1 > item2

# End of query handlers

# Turns Reviews into Dictionary
def parseReview(reviewNumber):
    #####database = db.DB()
    #database.open("rw.idx")
    #review = database.get(reviewNumber).decode("utf-8")
    #database.close()
    #reviewItems = reader(review).next()
    reviewItems = ["1","2","3","4","5","6","7","1182816000","9","10"]
    reviewDict = dict(zip(reviewsColumns, reviewItems))
    date = datetime.datetime.fromtimestamp(int(reviewDict['date']))
    reviewDict['date'] = date.strftime('%Y/%m/%d')
    return reviewDict

# Prints Reviews for User
def printReviews(reviews):
    for review in reviews:
        reviewDict = parseReview(review)
        for i in reviewDict:
            print i + ":" + reviewDict[i]
        print ''

main()
