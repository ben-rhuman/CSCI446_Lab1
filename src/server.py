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

#Initialization Variables for server setup 
port_num = int(sys.argv[1])
local_board_file = sys.argv[2]

#Create custom HTTPRequestHandler class
class BattleshipHTTPRequestHandler(BaseHTTPRequestHandler):
  
  #handle GET command
  def do_GET(self):
    rootdir = 'C:/Users/Ben/Desktop/Fall 2017/CSCI466_Lab1/CSCI446_Lab1/src/' #file location
    print(self.path)
    try:
      if self.path.endswith('.html'):
        f = open(rootdir + self.path) #open requested file

        #send code 200 response
        self.send_response(200)

        #send header first
        self.send_header('Content-type','text-html')
        self.end_headers()

        #send file content to client
        self.wfile.write(f.read().encode("utf-8")) #In python 3.x you need to convert to utf-8
        f.close()
        return
      
    except IOError:
      self.send_error(404, 'file not found')
  
def run():
  print('http server is starting...')

  server_address = ('127.0.0.1', port_num)
  httpd = HTTPServer(server_address, BattleshipHTTPRequestHandler)

  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()