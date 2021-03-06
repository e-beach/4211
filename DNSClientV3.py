# Fall 2017 CSci4211: Introduction to Computer Networks
# This program serves as the client of DNS query.
# Written in Python v3.

import sys
import os
from socket import *

def main():
	while 1:
		
		print("Type in a domain name to query, or 'q' to quit:")
		while 1:
			st = input() # Get input from users.
			if st == "":
				continue
			else:
				break
		if st == "q" or  st == "Q":
			cSock.close()
			sys.exit(1) # If input is "q" or "Q", quit the program.
		else:
			host = "localhost" # Remote hostname. It can be changed to anything you desire.
			port = os.environ.get("4211_port", 5000)

			try:
				cSock = socket(AF_INET, SOCK_STREAM)
			except error as msg:
				cSock = None

			try:
				cSock.connect((host, port))
			except error as msg:
				cSock = None

			if cSock is None:
				print("Error: cannot open socket")
				sys.exit(1) # If the socket cannot be opened, quit the program.

			cSock.send(st.encode()) # Otherwise, send the input to server.
			data = cSock.recv(1024).decode() # Receive from server.
			print("Received:", data) # Print out the result.
			cSock.close()
main()
