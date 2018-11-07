import socket as mysoc
import sys

def fileLineCount(path):
	with open(path) as fileIn:
		for index, element in enumerate(fileIn):
			pass
	
	val = index + 1
	return val


print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

# Socket with Client
try:
	ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Server socket created")
except mysoc.error as err:
	print('{} \n'.format("socket open error ", err))

#Socket bound to pre-determined value for client
server_binding = ('', 50020)
ss.bind(server_binding)
ss.listen(1)
rsHost = mysoc.gethostname()
print("[RS]: RSServer host name is: ", rsHost)
localhost_ip = (mysoc.gethostbyname(rsHost))
print("[RS]: RSServer IP address is  ", localhost_ip)
csockid, addr = ss.accept()
print("[RS]: Got a connection request from a client to RSSERVER", addr)


# com Socket
try:
	com = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Socket for TS_COM created")
except mysoc.error as err:
	print('{} \n'.format("socket open error (TS_COM)", err))

# edu SOCKET
try:
	edu = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
	print("[RS]: Socket for TS_EDU created")
except mysoc.error as err:
	print('{} \n'.format("TS socket open error ", err))



#important info
#FIXME will need to change when testing on different machine


if (len(sys.argv) == 4):
	TS_COM_Host = sys.argv[1]
	TS_EDU_Host = sys.argv[2]
	DNS_RS_TXT = sys.argv[3]
else:
	TS_COM_Host = mysoc.gethostname()
	TS_EDU_Host = mysoc.gethostname()
	DNS_RS_TXT = 'PROJ2-DNSRS.txt'


COMHostName = TS_COM_Host #65500
EDUHostName = TS_EDU_Host #55000
COMHostConnected = False
EDUHostConnected = False


# RS TABLE SET UP
# IMPORT FROM TS FILE HERE
inPath = DNS_RS_TXT
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
	dnsMatch = False
	for i in range(x):
		if (RSarr[i][0] == msg):
			print("MATCH FOUND >> " + RSarr[i][0] + " ||| " + msg)
			dnsMatch = True
			# send entire row
			str = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
			break
		#else:
			#if (RSarr[i][2] == "NS"):
			#	strNS = RSarr[i][0] + " " + RSarr[i][1] + " " + RSarr[i][2]
		
				
	if dnsMatch:
		csockid.send(str.encode('utf-8'))
	else:
		print("Match not found")
		if "com" in msg:
			print("must connect to COM: ", msg)
			if not COMHostConnected:
				COMHostConnected = True
				COMPort = 65500
				com_ip = mysoc.gethostbyname(COMHostName)
				#FIXME will change here for the ports on diff machines
				server_bindingCOM = (com_ip, COMPort)
				com.connect(server_bindingCOM)
				print("[C]: Connected to COM Server")
				
			# send the hostname to com
			print("[RS > COM] sending: " + msg)
			com.send(msg.encode('utf-8'))
			data_from_com = com.recv(1024)
			print("[RS < COM] received:  ", data_from_com.decode('utf-8'))
			msgCOM = data_from_com.decode('utf-8')
			csockid.send(msgCOM.encode('utf-8'))
		elif "edu" in msg:
			print("must connect to EDU:  ", msg)
			if not EDUHostConnected:
				EDUHostConnected = True
				EDUPort = 55000
				edu_ip = mysoc.gethostbyname(EDUHostName)
				# FIXME will change here for the ports on diff machines
				server_bindingEDU = (edu_ip, EDUPort)
				edu.connect(server_bindingEDU)
				print("[C]: Connected to EDU Server")
			
			# send the hostname to com
			print("[RS > EDU] sending: " + msg)
			edu.send(msg.encode('utf-8'))
			data_from_edu = edu.recv(1024)
			print("[RS < EDU] received:  ", data_from_edu.decode('utf-8'))
			msgEDU = data_from_edu.decode('utf-8')
			csockid.send(msgEDU.encode('utf-8'))
		else:
			print("error:  ", msg)
			strSendBack = "Error"
			csockid.send(strSendBack.encode('utf-8'))
			
	# send back the original message or something saying not found
	# csockid.send(strNS.encode('utf-8'))
	
	print("")
	
com.send("Kill COM".encode('utf-8'))
edu.send("Kill EDU".encode('utf-8'))

# Close the server socket
ss.close()
com.close()
edu.close()
print("#### CLOSE RS SERVER")
exit()
