# -*- coding: utf-8 -*-

from socket import *
from select import select
import sys

HOST='127.0.0.1'
PORT=56789
BUFSIZE=1024
ADDR=(HOST,PORT)

clientSocket=socket(AF_INET,SOCK_STREAM)

try:
	clientSocket.connect(ADDR)
except Exception as e:
	print "Cannot connect chat server"
	sys.exit()
print "Connect succeed chat server"

def prompt():
	sys.stdout.write('<Me> ')
	sys.stdout.flush()

while True:
	try:
		connection_list=[sys.stdin,clientSocket]
		read_socket,write_socket,error_socket=select(connection_list,[],[],10)
		for sock in read_socket:
			if sock==clientSocket:
				data=sock.recv(BUFSIZE)
				if not data:
					print "Connection lost with chat server"
					clientSocket.close()
					sys.exit()
				else:
					print "%s"%data
					prompt()
			else:
				message=sys.stdin.readline()
				clientSocket.send(message)
				prompt()
	except KeyboardInterrupt:
		clientSocket.close()
		sys.exit()

