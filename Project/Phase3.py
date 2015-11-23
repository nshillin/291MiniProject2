from bsddb3 import db
#from csv import reader
from pyparsing import commaSeparatedList
import datetime
import re

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","date","summary","text"]
#allReviews = {}

class QueryData:
	def __init__(self):
		#Terms to be checked
		self.terms = []
		self.termsP = []
		self.termsR = []
		#Value must be > value 0, < value 1
		self.ranges = {
		'rscore': [None, None],
		'pprice': [None, None],
		'rdate': [None, None]
		}
		# List of reviews
		self.reviews = []
		self.reviewsAdded = False

	def date_update(self, oper, dateStr):
		#Updates the rdate values.
		date = datetime.datetime.strptime(dateStr, "%Y/%m/%d")
		if oper == '>':
			original = self.ranges['rdate'][0]
			if original is None or compareTwoItems(date, oper, original):
				self.ranges['rdate'][0] = date;
		elif oper == '<':
			original = self.ranges['rdate'][1]
			if original is None or compareTwoItems(date, oper, original):
				self.ranges['rdate'][1] = date;
		return

	def value_update(self, fieldStr, oper, valueStr):
		#Updates the rscore or pprice values.
		value = float(valueStr)
		if oper == '>':
			original = self.ranges[fieldStr][0]
			if original is None or compareTwoItems(value, oper, original):
				self.ranges[fieldStr][0] = value;
		elif oper == '<':
			original = self.ranges[fieldStr][1]
			if original is None or compareTwoItems(value, oper, original):
				self.ranges[fieldStr][1] = value;
		return

	def term_update(self, fieldStr, termStr):
		#Adds terms.
		if fieldStr is None:
			self.terms.append(termStr)
		elif fieldStr == 'p:':
			self.termsP.append(termStr)
		elif fieldStr == 'r:':
			self.termsR.append(termStr)


def main():
	#setupReviewList()
	#setupReviews()
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
				search(queryData)

def parseQuery(text):
    regex_date = '^\s*rdate\s*([<>])\s*(\d{4}[/]\d{2}[/]\d{2})(\s+|\Z)'
    regex_value = '^\s*(rscore|pprice)\s*([<>])\s*([-]?\d+([.]\d+)?)(\s+|\Z)'
    regex_term = '^\s*([pr]:)?(\w+[%]?)(\s+|\Z)'

    data = QueryData()

    while len(text) > 0:
		matcher = re.search(regex_date, text)
		if matcher is not None:
			data.date_update(matcher.group(1), matcher.group(2))
			text = re.sub(regex_date, '', text)
			continue
		matcher = re.search(regex_value, text)
		if matcher is not None:
			data.value_update(matcher.group(1), matcher.group(2), matcher.group(3))
			text = re.sub(regex_value, '', text)
			continue
		matcher = re.search(regex_term, text)
		if matcher is not None:
			data.term_update(matcher.group(1),matcher.group(2))
			text = re.sub(regex_term, '', text)
			continue
		return None
    return data


def search(queryData):
	if queryData.terms != []:
		pass
	if queryData.termsP != []:
		pass
	if queryData.termsR != []:
		pass
	queryData = compare_rscore(queryData)
	reviewHandler(queryData)

## Start of query handlers
# Query handlers should accept a command and

def compare_rscore(queryData):
	database = db.DB()
	database.open("sc.idx")
	cur = database.cursor()
    #review = database.get(reviewNumber).decode("utf-8")
	rscoreList = []
	queryRange = queryData.ranges['rscore']
	if queryRange != [None, None]:
		if queryRange[0] == None:
			value = cur.first()
			end = queryRange[1]
		elif queryRange[1] == None:
			end = float(cur.last()[1])
			value = cur.set_range(str(queryRange[0]+0.1))
		else:
			value = cur.set_range(str(queryRange[0]+0.1))
			end = queryRange[1]
		while value:
			if float(value[0]) < end:
				rscoreList.append(int(value[1]))
				value = cur.next()
			else:
				break
		if queryData.reviewsAdded:
			queryData.reviews = list(set(queryData.reviews).intersection(rscoreList))
		else:
			queryData.reviews = sorted(rscoreList)
			queryData.reviewsAdded = True
	database.close()
	return queryData

def reviewHandler(queryData):
	for r in queryData.reviews:
		review = parseReview(r)
		dates = queryData.ranges['rdate']
		prices = queryData.ranges['pprice']
		if compareRange(dates, review['date']) and compareRange(prices, review['price']):
			printReview(r,review)

def compareRange(queryRange, reviewData):
	if queryRange != [None, None]:
		if queryRange[0] == None:
			if not(queryRange[1] > reviewData):
				return False
		elif queryRange[1] == None:
			if not(queryRange[0] < reviewData):
				return False
		elif not((queryRange[0] < reviewData) and (queryRange[1] > reviewData)):
			return False
	return True

# End of query handlers

# Turns Reviews into Dictionary

def parseReview(reviewNumber):
	database = db.DB()
	database.open("rw.idx")
	review = database.get(str(reviewNumber))
	database.close()
	reviewItems = commaSeparatedList.parseString(review).asList()
	#reviewItems = ["1","2","3","4","5","6","7","1182816100","9","10"]
	reviewDict = dict(zip(reviewsColumns, reviewItems))
	date = datetime.datetime.fromtimestamp(int(reviewDict['date']))
	reviewDict['date'] = date
	try:
		reviewDict['price'] = float(reviewDict['price'])
	except ValueError:
		pass
	reviewDict['score'] = float(reviewDict['score'])
	return reviewDict


# Prints individual Review for User
def printReview(number,review):
	#for testing
	#print number
	for i in reviewsColumns:
		print i + ":" + str(review[i])
	print '' """

def dbPrint():
	database = db.DB()
	database.open("rw.idx")
	print database.get('1')
	cur = database.cursor()
	a = cur.first()
	while a:
		print(a[0])
		a = cur.next()
	database.close()

main()
