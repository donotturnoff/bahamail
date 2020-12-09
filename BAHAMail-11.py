#Import modules
from socket import *
import csv
from tkinter import *
from time import sleep
import os

version = 11 #Version

for i in os.listdir(): #For every file in the current directory
	nameParts = i.split('-') #Split the filename at every -
	if nameParts[0] == 'BAHAMail': #If the first part is BAHAMail
		nameParts = nameParts[1].split('.') #Split the second part of the filename at every .
		if int(nameParts[0]) < version: #If the second part of the name (the version) is less than the current version
			os.remove(i) #Delete the file

while True: #Forever
	try: #Try
		connected = False #Boolean: True if connected, False if not
		loggedIn = False #Boolean variable: True when user is logged in, False when user is logged out
		username = '' #Variable to store username locally
		password = '' #Variable to store password locally

		def clear(): #Create clear function
			if os.name == 'posix': #If system is of type *nix
				os.system('clear') #Clear screen
			elif os.name == 'nt': #If system is of type Windows
				os.system('cls') #Clear screen

		def update(): #Create update function
			global version
			s = socket() #Create a socket object
			s.connect((host, 6000)) #Connect to specified host
			s.send(b'update;' + username.encode() + b';' + str(version).encode()) #Send request
			data = s.recv(10000000).decode() #Receive data
			version = data.split("$$$")[0]
			code = "$$$".join(data.split("$$$")[1:])
			if data == 'no': #If there are no updates
				print('No updates') #Print message
			else: #If there are
				if input('Updates available. Install? (y/n)').lower() == 'y': #If the user wants updates
					f = open('BAHAMail-' + version + '.py', 'w') #Open a new file
					f.write(code) #Write the new code
					f.close() #Close the file
					print('Updates installed.\nClose this window\nDelete the current program\nGo to BAHAMail-' + version + '.py\nRun it\n\nWindow will auto-close in 20 seconds') #Print instructions
					sleep(20) #Wait 20 seconds
					exit() #Exit
				else: #Otherwise
					print('Ok then') #Say ok

		def directory(): #Create directory function
			s = socket() #Create a socket object
			s.connect((host, 6000)) #Connect to specified host
			s.send(b'dir;' + username.encode()) #Send request containing username
			data = s.recv(10000000) #Receive response
			print(data.decode()) #Print data
		
		def commands(): #Create commands function
			print('Commands:\nlogin\nregister\nlogout\nsend\nrecv\ndir\ncommands\nintro\nclear\nupdate\nexit') #Print commands

		def baha(): #Baha function
			print('     _________ ')
			print('    /         \\')
			print('   /        _  |')
			print('   |       (_) |')
			print('   |  O        |')
			print('   |     |   | |____')
			print(' __|  |  |   | |    \\')
			print('/  \   \____/  /     \\')
			print('|   \_________/   .  |')

		def intro(): #Intro function
			print('BAHAMail v' + str(version) + '\nType \'commands\' for commands') #Print introduction
			
		intro() #Run intro at start

		while True:
			host = input('Enter host address (hit enter to auto-connect): ') #Get host address

			if host == 'exit': #If exit command entered
				exit() #Exit

			elif not host == 'dev': #If developer mode isn't enabled
				if host == '': #If enter is hit
					host = 'localhost' #Revert to localhost

				for i in range(5): #Loop five times
					try: #Try to...
						s = socket() #Create socket object
						s.connect((host, 6000)) #Connect to specified host
						s.send(b'connect') #Send connect request
						data = s.recv(16).decode() #Receive response
						if data == 'connected': #If response is affirmative
							print('Connected') #Print message
							connected = True #Set connected to True
							update() #Check for updates
							break #Leave loop
						else: #If response is negative
							raise Exception #Raise an error
					except Exception as msg: #If there is an error
						print(msg)
						print('Could not connect. Retrying ' + str(5-i) + ' more times, next retry in 5 seconds') #Print error message
						sleep(5) #Wait five seconds

				if connected: #If connected
					break #Leave loop

			else: #If developer mode is enabled
				break #Leave loop

		while True: #Forever
			command = input('>>> ').lower() #Ask for input
			if command == 'login': #If input is login
				while True: #Forever
					if loggedIn == True: #If user is logged in
						print('Already logged in') #Print error
						break #Leave loop
					else: #If user is not logged in
						username = input('Username: ') #Ask for username
						password = input('Password: ') #Ask for password
						s = socket() #Make a socket object
						s.connect((host, 6000)) #Connect to specified host
						s.send(b'login;' + username.encode() + b';' + password.encode()) #Send a request containing username and password
						data = s.recv(16).decode() #Receive response
						s.close() #Close socket
						if data == 'welcome': #If response is affirmative
							loggedIn = True #Set loggedIn to True
							print('Welcome', username) #Print a welcome message
							break #Leave loop
						else: #If response is negative
							loggedIn = False #Set loggedIn to False
							print('Incorrect username or password') #Print error

		####################################################################   

			elif command == 'send': #If input is send
				if loggedIn == False: #If user isn't logged in
					accountYN = input('Do you have an account? (y/n) ').lower() #Ask user if they have an account
					if accountYN == 'y': #If they do have an account
						while True: #Forever
							username = input('Username: ') #Ask for username
							password = input('Password: ') #Ask for password
							s = socket() #Create socket object
							s.connect((host, 6000)) #Connect to specified host
							s.send(b'login;' + username.encode() + b';' + password.encode()) #Send request containing username and password
							data = s.recv(16).decode() #Receive response
							s.close() #Close socket
							if data == 'welcome': #If response is affirmative
								loggedIn = True #Set loggedIn to True
								print('Welcome', username) #Print welcome message
								break #Leave loop
							else: #If response is negative
								loggedIn = False #Set loggedIn to False
								print('Incorrect username or password') #Print error
					else: #If they don't have an account
						while True: #Forever
								username = input('Username: ') #Ask for username
								password = input('Password: ') #Ask for password
								password2 = input('Confirm password: ') #Ask for password confirmation
								if not password == password2: #If passwords don't match
										print('Passwords do not match') #Print error message
								else: #If they do
										break #Leave the loop
						s = socket() #Make a socket object
						s.connect((host, 6000)) #Connect to specified host
						s.send(b'register;' + username.encode() + b';' + password.encode()) #Send request containing username and password
						data = s.recv(16).decode() #Receive response
						s.close() #Close socket
						if data == 'welcome': #If response is affirmative
							loggedIn = True #Set loggedIn to True
							print('Welcome', username) #Print welcome message
						elif data == 'exists': #If data indicates that the user already exists
							loggedIn = False #Set loggedIn to False
							print('User already exists') #Print error message
						else: #If data is otherwise negative
							loggedIn = False #Set loggedIn to false
							print('Incorrect username or password') #Print error 

				recipient = input('Enter recipient: ').encode() #Ask for recipient		
				message = input('Enter message: ').encode() #Ask for message
				s = socket() #Create socket object
				s.connect((host, 6000)) #Connect to specified host
				s.send(b'send;' + recipient + b';' + username.encode() + b';' + message) #Send request containing recipient, sender and message
				s.close() #Close socket
				print('Sent') #Print affirmative message
			
		####################################################################   
				
			elif command == 'recv' or command == 'receive': #If input is recv or receive
				if not loggedIn: #If user isn't logged in
					accountYN = input('Do you have an account? (y/n) ').lower() #Ask if they have an account
					if accountYN == 'y': #If they do have an account
						while True: #Forever
							username = input('Username: ') #Ask for username
							password = input('Password: ') #Ask for password
							s = socket() #Create socket object
							s.connect((host, 6000)) #Connect to specified host
							s.send(b'login;' + username.encode() + b';' + password.encode()) #Send request containing username and password
							data = s.recv(16).decode() #Receive response
							s.close() #Close socket
							if data == 'welcome': #If response is negative
								loggedIn = True #Set loggedIn to True
								print('Welcome', username) #Print welcome message
								break #Leave loop
							else: #If response is negative
								loggedIn = False #Set loggedIn to False
								print('Incorrect username or password') #Print error message
					else: #If they don't have an account
						while True: #Forever
							username = input('Username: ') #Ask for username
							password = input('Password: ') #Ask for password
							password2 = input('Confirm password: ') #Ask for password confirmation
							if not password == password2: #If passwords don't match
								print('Passwords do not match') #Print error message
							else: #If they do
								break #Leave the loop
						s = socket() #Make a socket object
						s.connect((host, 6000)) #Connect to specified host
						s.send(b'register;' + username.encode() + b';' + password.encode()) #Send request containing username and password
						data = s.recv(16).decode() #Receive response
						s.close() #Close socket
						if data == 'welcome': #If response is affirmative
								loggedIn = True #Set loggedIn to True
								print('Welcome', username) #Print welcome message
						elif data == 'exists': #If data indicates that the user already exists
								loggedIn = False #Set loggedIn to False
								print('User already exists') #Print error message
						else: #If data is otherwise negative
								loggedIn = False #Set loggedIn to false
								print('Incorrect username or password') #Print error 

				s = socket() #Create socket object
				s.connect((host, 6000)) #Connect to specified host 
				s.send(b'recv;' + username.encode()) #Send request containing username
				data = int(s.recv(16).decode()) #Receive response (amount of messages)
				messagesAmount = data #Make a variable containing the amount of messages
				print('From\tMessage') #Print table heading
				for i in range(0, messagesAmount): #For every message
					data = s.recv(10000).decode() #Receive the message
					if not data == '':
						print(data) #Print the message		

		####################################################################
				
			elif command == 'register': #If input is register
				if loggedIn: #If user is already logged in
					print('Already logged in') #Print error message
				else: #If user isn't logged in
					while True: #Forever
						username = input('Username: ') #Ask for username
						password = input('Password: ') #Ask for password
						password2 = input('Confirm password: ') #Ask for password confirmation
						if not password == password2: #If passwords don't match
							print('Passwords do not match') #Print error message
						else: #If they do
							break #Leave the loop
					s = socket() #Make a socket object
					s.connect((host, 6000)) #Connect to specified host
					s.send(b'register;' + username.encode() + b';' + password.encode()) #Send request containing username and password
					data = s.recv(16).decode() #Receive response
					s.close() #Close socket
					if data == 'welcome': #If response is affirmative
						loggedIn = True #Set loggedIn to True
						print('Welcome', username) #Print welcome message
					elif data == 'exists': #If data indicates that the user already exists
						loggedIn = False #Set loggedIn to False
						print('User already exists') #Print error message
					else: #If data is otherwise negative
						loggedIn = False #Set loggedIn to false
						print('Incorrect username or password') #Print error 

		####################################################################
					
			elif command == 'logout': #If input is logout
				if loggedIn == True: #If user is logged in
					s = socket() #Make a socket object
					s.connect((host, 6000)) #Connect to specified host
					s.send(b'logout;' + username.encode()) #Send request containing username
					loggedIn = False #Set loggedIn to False
					print('You are logged out') #Print confirmation of logout
					username = '' #Clear username
					password = '' #Clear password
				else: #If user isn't logged in
					print('You are not logged in') #Print error

		####################################################################

			elif command == 'clear' or command == 'cls': #If command is cls or clear
				clear() #Run clear function

			elif command == 'anonymous': #If command is Anonymous
				anonymous() #Run Anonymous function

			elif command == 'update': #If command is update
				update() #Run update function

			elif command == 'dir' or command == 'directory': #If command is dir or directory
				directory() #Run directory function

			elif command == 'intro': #If command is intro
				intro() #Run intro function

			elif command == 'commands': #If input is commands
				commands() #Run commands function

			elif command == 'exit': #If command is exit
				exit() #Guess what? ... Exit!

			elif command == 'baha': #If command is baha
				baha() #Run baha function

			elif command == 'error': #If command is error
				raise Exception('Human error (404 - Brain not found)')

			else: #If command isn't recognised
				print('Invalid command. Type \'commands\' for a list') #Print error
				
	except Exception as msg: #If there is an error
		clear() #Clear screen
		print(str(msg) + '\nRestarting in 5 seconds...\n') #Print error and restart message
		sleep(5)
