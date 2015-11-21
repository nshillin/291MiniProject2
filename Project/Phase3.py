#from bsddb3 import db
from csv import reader
import datetime
import re

reviewsColumns = ["productId","title","price","userId","profileName","helpfulness","score","date","summary","text"]

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
		self.reviews = [1]

	def date_update(self, oper, dateStr):
		#Updates the rdate values.
		if oper == '>':
			original = self.ranges['rdate'][0]
			if original is None or compareTwoItems(datetime.datetime.strptime(dateStr, "%Y/%m/%d"), oper, original):
				self.ranges['rdate'][0] = datetime.datetime.strptime(dateStr, "%Y/%m/%d");
		elif oper == '<':
			original = self.ranges['rdate'][1]
			if original is None or compareTwoItems(datetime.datetime.strptime(dateStr, "%Y/%m/%d"), oper, original):
				self.ranges['rdate'][1] = datetime.datetime.strptime(dateStr, "%Y/%m/%d");
		return

	def value_update(self, fieldStr, oper, valueStr):
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

	def term_update(self, fieldStr, termStr):
		#Adds terms.
		if fieldStr is None:
			self.terms.append(termStr)
		elif fieldStr == 'p:':
			self.termsP.append(termStr)
		elif fieldStr == 'r:':
			self.termsR.append(termStr)

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
	if queryData.ranges['rscore'] != [None, None]:
		# grab all rscores from bd as item1
		pass
	return queryData

def reviewHandler(queryData):
	for r in queryData.reviews:
		review = parseReview(r)
		dates = queryData.ranges['rdate']
		prices = queryData.ranges['pprice']
		if compare_rdate(dates, review['date']): #and compare_pprice(prices, review['price']):
			printReview(review)

def compare_rdate(dates, reviewDate):
	if dates != [None, None]:
		if dates[0] == None:
			if not(dates[1] > reviewDate):
				return False
		elif dates[1] == None:
			if not(dates[0] < reviewDate):
				return False
		elif not((dates[0] < reviewDate) and (dates[1] > reviewDate)):
			return False
	return True

def compare_pprice(queryData):
	if queryData.ranges['pprice'] != [None, None]:
		pass
		for r in queryData.reviews:
			review = parseReview(r)
			# float(review['price'])
			# updatedReviewList.append(r)
	return queryData

# End of query handlers

# Turns Reviews into Dictionary
def parseReview(reviewNumber):
    #####database = db.DB()
    #database.open("rw.idx")
    #review = database.get(reviewNumber).decode("utf-8")
    #database.close()
    #reviewItems = reader(review).next()
    reviewItems = ["1","2","3","4","5","6","7","1182816100","9","10"]
    reviewDict = dict(zip(reviewsColumns, reviewItems))
    date = datetime.datetime.fromtimestamp(int(reviewDict['date']))
    reviewDict['date'] = date
    return reviewDict

# Prints individual Review for User
def printReview(review):
	reviewDict = parseReview(review)
	for i in reviewDict:
		print i + ":" + str(reviewDict[i])
	print ''

main()
