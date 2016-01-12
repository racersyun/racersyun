from socket import *
from select import *
import sys
from time import ctime

HOST=''
PORT=56789
BUFSIZE=1024
ADDR=(HOST,PORT)

serverSocket=socket(AF_INET,SOCK_STREAM)

serverSocket.bind(ADDR)

serverSocket.listen(10)
connection_list=[serverSocket]

print "Starting char server with port %s"%str(PORT)

while connection_list:
	try:
		print "[INFO] Wating request..."

		read_socket,write_socket,error_socket=select(connection_list,[],[],10)

		for sock in read_socket:
			if sock==serverSocket:
				clientSocket,addr_info=serverSocket.accept()
				connection_list.append(clientSocket)
				print "[INFO] %s connected"%addr_info[0]

				for socket_in_list in connection_list:
					if socket_in_list in connection_list:
						try:
							socket_in_list.send("[INFO] Welcome")
						except Exception as e:
							socket_in_list.close()
							connection_list.remove(socket_in_list)
			else:
				data=sock.recv(BUFSIZE)
				if data:
					print "[INFO] Message Received"
					for socket_in_list in connection_list:
						if socket_in_list!=serverSocket and socket_in_list!=sock:
							try:
								socket_in_list.send("[%s] %s"%(ctime,data))
								print "Message Sent"
							except Exception as e:
								print e.message
								socket_in_list.close()
								connection_list.remove(socket_in_list)
								continue
				else:
					connection_list.remove(sock)
					sock.close()
					print "Connection lost"
	except KeyboardInterrupt:
			serverSocket.close()
			sys.exit()

