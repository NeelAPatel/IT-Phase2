import socket as mysoc


def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


# FIRST Socket
try:
	rs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for RS created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))
	
# SECOND SOCKET
try:
	ts = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[C]: Socket for TS created")
except mysoc.error as err:
	print('{} \n'.format("TS socket open error ", err))

RsPort = 50020
clientHost = mysoc.gethostname()
print("[C]: Client name is: " , clientHost)

clientIP = mysoc.gethostbyname(mysoc.gethostname())
print("[C]: Client IP is: " , clientIP)


# connect to RS_SERVER first
server_bindingRS = (clientIP, RsPort)
rs.connect(server_bindingRS)
print ("[C]:  Connected to RS Server")

# Import from file
inPath = 'PROJI-HNS.txt'
numLinesInFile = fileLineCount(inPath)
inFile = open(inPath, 'r')
print("Num Of Lines in HNS: " + str(numLinesInFile))

rs.send(str(numLinesInFile).encode('utf-8'))
data_from_server = rs.recv(100)
msg = data_from_server.decode('utf-8')
print("[C < RS]: Response: " + msg)
# send num of lookups

#create a file to output the data
fileOut = open("Resolved.txt", "w")
tsConnected = False
while True:
	# Each iteration = one lookup in TS/RS
	inLine = inFile.readline()
	if not inLine:
		break
	
	# Send line to RS
	inLine = inLine.strip('\n')
	rs.send(inLine.encode('utf-8'))
	print("[C > RS] Line Sent: " + inLine)
	
	
	data_from_server = rs.recv(1024)
	msg = data_from_server.decode('utf-8')
	print("[C < RS]: Response : " + msg)
	
	#split it in 3 and check 3rd portion.
	
	splitList = msg.split()
	if splitList[2] == 'NS':
		if tsConnected == False:
			tsConnected= True
			print("[C]: MUST CONNECT TO TS NOW.")
			TsPort = 60000
			tsHostName = splitList[0]
			ts_ip = mysoc.gethostbyname(tsHostName)
			print("GREP IP IS: ", ts_ip)
			server_bindingTS = (ts_ip, TsPort)
			ts.connect(server_bindingTS)
			print("[C]: Connected to TS Server")
	
		#send the hostname to ts
		print("[C > TS] sending: "  + inLine)
		ts.send(inLine.encode('utf-8'))
		data_from_ts = ts.recv(1024)
		print("[C < TS] received:  ", data_from_ts.decode('utf-8'))
		msgTS= data_from_ts.decode('utf-8')
		splitListTS = msgTS.split()
		
		#write to file
		strToFileTS = msgTS + "\n"
		fileOut.write(strToFileTS)
	else:
		# output the string to result file
		strToFile = msg + "\n"
		fileOut.write(strToFile)
		print("[C]: Line is VALID: ", msg)
	
	print("")



ts.send("Kill TS".encode('utf-8'))

rs.close()
ts.close()




#print("Stuff ended")
#data_from_server = rs.recv(1024)
#print("[C]: Data received from RS server: [", data_from_server.decode('utf-8'), "]")
#data_from_server_decoded= data_from_server.decode('utf-8')







