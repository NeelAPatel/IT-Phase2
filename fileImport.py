def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass

	val = index + 1
	return val


# ============== CODE ==================

# IMPORT FROM TS FILE HERE
inPath = 'PROJI-DNSTS.txt'
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')

print("Num Of Lines: " + str(numLinesInFile))


#Create Table
TSarr = [[] for _ in range(numLinesInFile)]
print(TSarr)

# Take file contents, add to table
rowIndex= 0
while True:
	inLine = inFile.readline()
	# if Line does not exist (EOF)
	if not inLine:
		break
	print("Current Line: " + str(rowIndex) + " >>" + inLine + "<<")
	# 1. Separate by spaces (there are different # of spaces

	splitList = inLine.split()
	#print(*splitList, sep= "][")
	TSarr[rowIndex].append(splitList[0])
	TSarr[rowIndex].append(splitList[1])
	TSarr[rowIndex].append(splitList[2])
	print(TSarr)
	rowIndex+=1
	print("============")