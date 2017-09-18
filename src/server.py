#######################################################
#													  #
#        CSCI 466 Lab 1 - Battleship over HTTP        #
#        Authors: Ben Rhuman & Taylor Sheffels        #
#        Date: 9/14/17                                #
#        File: server.py                              #
# 		 This server handles HTTP requests form       #
#        clients and servers to play a game of        #
#        battleship over a network using the          #
#        command line                                 #
#                                                     #
#######################################################

#Example invocation: python server.py 5000 board.txt
#Note: Make sure to start server first. 

#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import re

#ship_C, ship_B, ship_R, ship_S, ship_D
ship_C, ship_B, ship_R, ship_S, ship_D = 5, 4, 3, 3, 2

def main():

	#ship_C#, ship_B, ship_R, ship_S, ship_D
	
	#Initialization Variables for server setup 
	port_num = int(sys.argv[1])
	local_board_file = sys.argv[2]
	run(port_num)

#Create custom HTTPRequestHandler class
class BattleshipHTTPRequestHandler(BaseHTTPRequestHandler):
  
  #handle GET commands
	def do_GET(self):
		print(self.path)
		rootdir = os.path.dirname(os.path.abspath(__file__))+ "\\"
		#Make sure path will open the HTML file
		page = open(rootdir + self.path[1:], "r")
		contents = page.read()

		#GET should be used to get the HTML format of the game boards
		self.protocol_version = 'HTTP/1.1'
		self.send_response(200)
		self.send_header("User-Agent", "application/x-www-form-urlencoded")
		self.send_header("Content-type", "text/html")
		self.end_headers()
		elf.wfile.write(str.encode(contents))
		return

		#except IOError:
		#	self.send_error(404, 'file not found')

	def do_POST(self):
		length = int(self.headers.get('Content-Length'))
		body = self.rfile.read(length)
		print(body)

		response, code = game_logic(body)

		#HTTP OK (200) response 
		self.protocol_version = 'HTTP/1.1'
		self.send_response(code)
		self.send_header("User-Agent", "application/x-www-form-urlencoded")
		self.send_header("Content-type", "text/html")
		self.send_header("Response", response)
		self.end_headers()
 
def game_logic(message):
	board = []
	message = str(message)

	#Parses the url and provides the x,y coordinates
	x = message[4:6]
	x = int(re.search(r'\d+', x).group())

	y = message[-3:-1]
	y = int(re.search(r'\d+', y).group())
	print(x)
	print(y)

	#Converts x,y coordinates into an list index
	if x<10 and y<10:
		guess = ((y*10)+ x)
		print ("guess = " , guess)
	else:
		h, s, code = 0, str(0), 404
		return "hit="+ str(h) + "&sink=" + str(s) , code

	#Recovers board data from given text file
	rootdir = os.path.dirname(os.path.abspath(__file__))[:-3]  #file location
	f = open(rootdir + 'board.txt', 'r')
	while True:
		ch=f.read(1)
		if not ch: break
		if not ch == "\n":
			board.extend(ch)
	f.close()

	#Initial response variables
	h, s, code = 1, str(0), 200
	print(board[guess])
	if board[guess] == "X" or board[guess] == "O":
		h, code = 0, 410
		print ("this is the already shot at case")
	elif board[guess] == "_":
		h = 0
		print ("this is the miss case")
	elif board[guess] == "C":
		global ship_C
		ship_C-=1
		if ship_C == 0:
			s = 'C'
		print ("this is the C case")
	elif board[guess] == "B":
		global ship_B
		ship_B-=1
		if ship_B == 0:
			s = 'B'
		print ("this is the B case")
	elif board[guess] == "R":
		global ship_R
		ship_R-=1
		if ship_R == 0:
			s = 'R'
		print ("this is the R case")
	elif board[guess] == "S":
		global ship_S
		ship_S-=1
		if ship_S == 0:
			s = 'S'
		print ("this is the S case")
	elif board[guess] == "D":
		global ship_D
		ship_D-=1
		if ship_D == 0:
			s = 'D'
		print ("this is the D case")
	else:
		h, code = 0, 400
		print ("you broke the game, are you happy now?")

	if h == 1:
		board[guess] = "X"
	elif board[guess] == "X":
		board[guess] = "X"
	else:
		board[guess] = "O"

	if s != '0':
		if(ship_D+ship_S+ship_R+ship_B+ship_C == 0):
			s = 'G'

	write_to_file(board, rootdir,s)

	return "hit="+ str(h) + "&sink=" + str(s) , code

def write_to_file(board, rootdir, s):
	newBoard = []
	for x in range(0,100):
		newBoard.extend(board[x])
		if x%10 == 9:
			newBoard.extend("\n")
	g = open(rootdir + 'board.txt', 'w')

	if s == 'G':
		newBoard = []
		newBoard.extend("\n\n\n\n  YOU LOSE!")

	for x in newBoard:
		g.write(x)
	g.close()

def run(port_num):
  print('http server is starting...')

  server_address = ('127.0.0.1', port_num) #('127.0.0.1', port_num)
  httpd = HTTPServer(server_address, BattleshipHTTPRequestHandler)

  print('http server is running...')
  httpd.serve_forever()
  
main()