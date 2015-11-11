import sys
import re

def main():
	try:
		fileName = str(sys.argv[1])
	except Exception, e:
		print "No file specified."
		return
	fileArray = readFile(fileName)
	# Creates Empty Files
	f = open('pterms.txt', 'w')
	f.close()
	f = open('rterms.txt', 'w')
	f.close()
	f = open('scores.txt', 'w')
	f.close()
	reviews = getReviews(fileArray)


def readFile(fileName):
	with open(fileName, "r") as f:
		fileArray = []
		for line in f:
			line = line.rstrip('\n')
			line = line.replace('"','&quot;')
			line = line.replace('\\','\\\\')
			fileArray.append(line)
	return fileArray

def getReviews(fileArray):
	k_requiresQuotes = ['product/title','review/profileName','review/summary','review/text']
	reviewsArray = []
	review = ""
	reviewNumber = 1
	for line in fileArray:
		if ": " in line:
			splitLine = line.split(": ",1)

			if splitLine[0] == 'product/title':
				newPTerms(splitLine[1],reviewNumber)
			elif splitLine[0] == 'review/summary' or splitLine[0] == 'review/text':
				newRTerms(splitLine[1],reviewNumber)
			elif splitLine[0] == 'review/score':
				newScore(splitLine[1],reviewNumber)

			if splitLine[0] in k_requiresQuotes:
				splitLine[1] = '"%s"' % splitLine[1]

			if splitLine[0] == 'review/text':
				review += ',' + splitLine[1]
				review = str(reviewNumber) + review
				reviewsArray.append(review)
				reviewNumber += 1
				review = ""
			else:
				review += ',' + splitLine[1]
		else:
			continue
	writeReviews(reviewsArray)

def writeReviews(reviews):
	with open('reviews.txt', 'w') as f:
		for review in reviews:
			f.write(review + '\n')

def newPTerms(title,reviewNumber):
	with open('pterms.txt', 'a') as f:
		wordList = re.split('\W+',title)
		for word in wordList:
			if word != '' and len(word) >= 3:
				f.write(word.lower() + ',' + str(reviewNumber) + '\n')

def newRTerms(review,reviewNumber):
	with open('rterms.txt', 'a') as f:
		wordList = re.split('\W+',review)
		for word in wordList:
			if word != '' and len(word) >= 3:
				f.write(word.lower() + ',' + str(reviewNumber) + '\n')

def newScore(score,reviewNumber):
	with open('scores.txt', 'a') as f:
		f.write(score + ',' + str(reviewNumber) + '\n')

main()
