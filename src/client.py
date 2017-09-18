#######################################################
#													  #
#        CSCI 466 Lab 1 - Battleship over HTTP        #
#        Authors: Ben Rhuman & Taylor Sheffels        #
#        Date: 9/14/17                                #
#        File: client.py                              #
# 		 
#        
#                 
#                          
#                                                     #
#######################################################

#Example invocation: python client.py 127.0.0.1 5000 5 7
#Note: Make sure to start server first. 

#!/usr/bin/env python

import http.client
import sys
import os

oBoard = []


def main():
	#Retrieves server IP, port number, and x & y coordinates from system arguments 
	server_ip = sys.argv[1] 
	port_num = sys.argv[2]
	x_coordinate = sys.argv[3] 
	y_coordinate = sys.argv[4]

	message = build_message(x_coordinate, y_coordinate)
	response = connect_to_server(server_ip, port_num, message)
	client_logic(response, x_coordinate, y_coordinate)

#Local host server
localhost = "127.0.0.1"

def build_message(x, y):
	return "x=" + str(x) + "&y=" + str(y)

def connect_to_server(server_ip, port_num, message):
	#creates a connection to local server
	print("Connecting to server...")
	conn = http.client.HTTPConnection(localhost, port_num)
	#request(method, url, body=None, headers={}, *, encode_chunked=False)
	conn.request("POST", '', message, headers={"Content-Length": len(message)})
	print("Message sent...")

	#get response from server
	rsp = conn.getresponse()
	response = rsp.getheader("Response")
	conn.close() 	
	return response
	

def client_logic(response, x, y):
	print(response)
	hit = int(response[4])
	sink = response[11]
	print(hit)
	print(sink)


	rootdir = os.path.dirname(os.path.abspath(__file__))[:-3]  #file location
	f = open(rootdir + 'oBoard.txt', 'r')
	while True:
		ch=f.read(1)
		if not ch: break
		if not ch == "\n":
			oBoard.extend(ch)
	f.close()
	
	guess = ((int(y)*10)+ int(x))

	if(hit == 1):
		oBoard[guess] = "X"
	else:
		oBoard[guess] = "O"

	write_to_file(oBoard, rootdir, sink)

def write_to_file(oBoard, rootdir,s):
	newBoard = []
	for x in range(0,100):
		newBoard.extend(oBoard[x])
		if x%10 == 9:
			newBoard.extend("\n")
	g = open(rootdir + 'oBoard.txt', 'w')

	if s == 'G':
		newBoard = []
		newBoard.extend("\n\n\n\n  YOU WIN!")
	for x in newBoard:
		g.write(x)
	g.close()

main()
