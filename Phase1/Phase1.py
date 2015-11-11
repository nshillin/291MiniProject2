import sys

def main():
	try:
		fileName = str(sys.argv[1])
	except Exception, e:
		print "No file specified."
		return
	fileArray = readFile(fileName)
	reviews(fileArray)

def readFile(fileName):
	with open(fileName, "r") as f:
		for line in f:
			line = line.rstrip('\n')
			line = line.replace('"','&quot;')
			line = line.replace('\\','\\\\')
			print line

def reviews(fileArray):
	pass

main()
