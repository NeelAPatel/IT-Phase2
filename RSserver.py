import socket as mysoc


def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


try:
	ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Server socket created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))
server_binding = ('', 50020)
ss.bind(server_binding)
ss.listen(1)
host = mysoc.gethostname()
print("[RS]: Server host name is: ", host)
localhost_ip = (mysoc.gethostbyname(host))
print("[RS]: Server IP address is  ", localhost_ip)
csockid, addr = ss.accept()
print("[RS]: Got a connection request from a client to RSSERVER", addr)

# RS TABLE SET UP

# IMPORT FROM TS FILE HERE
inPath = 'PROJI-DNSRS.txt'
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')
print("Num Of Lines: " + str(numLinesInFile))

# Create Table
RSarr = [[] for _ in range(numLinesInFile)]

# fill in table
rowIndex = 0
while True:
	inLine = inFile.readline()
	if not inLine:  # if Line does not exist (EOF)
		break
	# print("Current Line: " + str(rowIndex) + " >>" + inLine + "<<")
	# Separate by spaces (there are different # of spaces
	splitList = inLine.split()
	RSarr[rowIndex].append(splitList[0])
	RSarr[rowIndex].append(splitList[1])
	RSarr[rowIndex].append(splitList[2])
	# print(RSarr)
	rowIndex += 1
	# print("============")

print(len(RSarr))




data_from_client = csockid.recv(100)
msg = data_from_client.decode('utf-8')
print("[RS] Received Num of lookups: " + msg)
csockid.send("NumLookups received".encode('utf-8'))

while 1:
	print("=========== LOOKUP ==============")
	data_from_client = csockid.recv(100)
	if not data_from_client:
		break
	msg = data_from_client.decode('utf-8')
	print("[RS] DNS received from Client: " + msg)
	
	
	#send confirmation
	
	# Look up DNS in RS_Table
	x = len(RSarr)
	str =""
	strNS=""
	dnsMatch = False
	for i in range(x):
		if (RSarr[i][0] == msg):
			print("MATCH FOUND >> " + RSarr[i][0] + " ||| " + msg)
			dnsMatch = True
			# send entire row
			str = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
			break
		else:
			if (RSarr[i][2] == "NS"):
				strNS = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
		
	
				
	if dnsMatch == False:
		# send TS server information
		print("Match not found. sending TS info")
		csockid.send(strNS.encode('utf-8'))
	else:
		csockid.send(str.encode('utf-8'))
	
	print("")
	

# Close the server socket
ss.close()
print("#### CLOSE RS SERVER")
exit()
