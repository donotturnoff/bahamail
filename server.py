while True:
	try:
		#Import
		from socket import *
		from datetime import *
		import csv
		import os.path

		#Log data
		def log(time, logType, msg):
			log = open('log.txt', 'a')
			log.write(str(time) + '\t' + logType + '\t' + msg + '\n')
			log.close()
			print(str(time) + '\t' + logType + '\t' + msg)

		#Set up server
		s = socket()
		s.bind(('', 6000))
		s.listen(10)
		log(datetime.now(), 'start', 'Server started at ' + str(gethostbyname(gethostname())) + ' on port 6000')

		#List of online users
		users = []

		while True:
			#Accept a connection
			c, addr = s.accept()
			log(datetime.now(), 'conn', 'Connection received from ' + str(addr))

			#Receive data
			data = c.recv(8192).decode()
			dataParts = data.split(';')
			log(datetime.now(), 'data', 'Data received from ' + str(addr) + ': ' + str(data))

			#If it is 'login'
			if dataParts[0] == 'login':
				
				#Open user database
				with open('users.csv', 'r') as csvfile:
					reader = csv.reader(csvfile)
					for row in reader:
						if row == []:
							pass

						#Check for user details
						elif row[0] == dataParts[1] and row[1] == dataParts[2]: 
							loggedIn = True
							c.send(b'welcome')
							users.append(dataParts[1])
							log(datetime.now(), 'login', str(addr) + ' logged in as ' + str(dataParts[1]))

			#If it is 'register'		  
			elif dataParts[0] == 'register':
				#Open user database for writing
				with open('users.csv', 'a') as csvfile:
					#Open user database for reading
					with open('users.csv', 'r') as csvfileR:
						exists = False
						reader = csv.reader(csvfileR)
						for row in reader:
							if row == []:
								pass
							#If the username exists, raise an error
							elif row[0] == dataParts[1] and row[1] == dataParts[2]: 
								exists = True
								break
						csvfileR.close()
					if exists:
						c.send(b'exists')
					else:
						#Add user
						writer = csv.writer(csvfile)
						writer.writerow([dataParts[1], dataParts[2]])
						c.send(b'welcome')
						users.append(dataParts[1])
						csvfile.close()
						log(datetime.now(), 'reg', str(addr) + ' registered as ' + str(dataParts[1]))
						
			elif dataParts[0] == 'logout':
				#Delete user from list
				if dataParts[1] in users:
					del users[users.index(dataParts[1])]
					log(datetime.now(), 'logout', str(addr) + ' logged out of account with username ' + str(dataParts[1]))

			elif dataParts[0] == 'send':
				with open('messages.csv', 'a') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([dataParts[1], dataParts[2], dataParts[3]])
					c.send(b'sent')
					csvfile.close()
					log(datetime.now(), 'send', str(dataParts[2]) + ' sent \'' + str(dataParts[3]) + '\' to ' + str(dataParts[1]))

			elif dataParts[0] == 'recv':
				messagesAmount = 0		
				with open('messages.csv', 'r') as csvfile:
					reader = csv.reader(csvfile)
					for row in reader:
						if row == []:
							pass
						elif row[0] == dataParts[1]:
							messagesAmount += 1
					c.send(str(messagesAmount).encode())
					csvfile.close()
				with open('messages.csv', 'r') as csvfile:
					msgReader = csv.reader(csvfile)
					for msgRow in msgReader:
						if msgRow == []:
							pass
						elif msgRow[0] == dataParts[1]:
							c.send(msgRow[1].encode() + b'\t' + msgRow[2].encode() + b'\n')
				log(datetime.now(), 'recv', str(dataParts[1]) + ' received ' + str(messagesAmount) + ' messages')

			elif dataParts[0] == 'dir':
				with open('users.csv', 'r') as csvfile:
					userList = ''
					reader = csv.reader(csvfile)
					for row in reader:
						if row == []:
							pass
						else:
							userList += row[0] + '\n'

					c.send(userList.encode())

				log(datetime.now(), 'dir', str(dataParts[1]) + ' accessed dir')

			elif dataParts[0] == 'connect':
				c.send(b'connected')

			elif dataParts[0] == 'update':

				log(datetime.now(), 'upd', str(dataParts[1]) + ' updated' )

				update = False
				filename = ''
				version = 0

				for i in os.listdir(): #For every file in the current directory
					nameParts = i.split('-') #Split the filename at every -
					if nameParts[0] == 'BAHAMail' and int(dataParts[2]) < int(nameParts[1].split('.')[0]): #If the first part is BAHAMail
						update = True
						filename = i
						version = nameParts[1]
						break
					else:
						update = False

				if update == True:
					f = open(filename, 'rb')
					lines = f.read()
					f.close()
					c.send(version.encode() + b'$$$' + lines)
				else:
					c.send(b'no')
				
			c.close()
			
	except Exception as msg:
		log(datetime.now(), 'error', str(msg) + ' attempting to restart')
		
	
