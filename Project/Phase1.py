import sys
import re
import multiprocessing

def main():
	print "Phase 1 Started"
	try:
		fileName = str(sys.argv[1])
	except Exception, e:
		print "No file specified."
		return
	fileArray = readFile(fileName)
	getReviews(fileArray)
	print "Phase 1 Finished"


def readFile(fileName):
	with open(fileName, "r") as f:
		fileString = f.read()
		fileArray = fileString.replace('"','&quot;').replace('\\','\\\\').splitlines()
	return fileArray

def getReviews(fileArray):
	k_requiresQuotes = ['product/title','review/profileName','review/summary','review/text']
	reviewsArray = []
	pTermsArray = []
	rTermsArray = []
	scoresArray = []
	review = ""
	reviewNumber = 1
	for line in fileArray:
		if ": " in line:
			splitLine = line.split(": ",1)

			if splitLine[0] == 'product/title':
				pTermsArray = newTerms(splitLine[1],reviewNumber,pTermsArray)
			elif splitLine[0] == 'review/summary' or splitLine[0] == 'review/text':
				rTermsArray = newTerms(splitLine[1],reviewNumber,rTermsArray)
			elif splitLine[0] == 'review/score':
				scoresArray = newScore(splitLine[1],reviewNumber,scoresArray)

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

	p1 = multiprocessing.Process(target=writeFile, args=('reviews.txt',reviewsArray))
	p1.start()
	#writeFile('reviews.txt',reviewsArray)
	p2 = multiprocessing.Process(target=writeFile, args=('pterms.txt',pTermsArray))
	p2.start()
	#writeFile('pterms.txt',pTermsArray)
	p3 = multiprocessing.Process(target=writeFile, args=('rterms.txt',rTermsArray))
	p3.start()
	#writeFile('rterms.txt',rTermsArray)
	p4 = multiprocessing.Process(target=writeFile, args=('scores.txt',scoresArray))
	p4.start()
	p1.join()
	p2.join()
	p3.join()
	p4.join()
	#writeFile('scores.txt',scoresArray)


def writeFile(filename, objects):
	print "writing ",filename
	with open(filename, 'w') as f:
		for i in objects:
			f.write(i + '\n')
	print "Finished writing ",filename


def newTerms(review,reviewNumber,array):
	wordList = re.split('\W+',review)
	for word in wordList:
		if word != '' and len(word) >= 3:
			array.append(word.lower() + ',' + str(reviewNumber))
	return array

def newScore(score,reviewNumber,array):
	array.append(score + ',' + str(reviewNumber))
	return array

main()
