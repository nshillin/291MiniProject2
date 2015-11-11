import sys

def main():
	try:
		fileName = str(sys.argv[1])
	except Exception, e:
		print "No file specified."
		return
	reviews(fileName)


def reviews(fileName):
	with open(fileName, "r") as f:
		for line in f:
			line = line.rstrip('\n')
			print line

main()