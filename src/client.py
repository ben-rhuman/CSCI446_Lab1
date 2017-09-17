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

#Retrieves server IP, port number, and x & y coordinates from system arguments 
http_server_ip = sys.argv[1] 
port_num = sys.argv[2]
x_coordinate = sys.argv[3] 
y_coodinate = sys.argv[4]


#Local host server
localhost = "127.0.0.1"

#creates a connection to local server
conn = http.client.HTTPConnection(localhost, port_num)

while 1:
  cmd = input('input command (ex. GET index.html): ')
  cmd = cmd.split()

  if cmd[0] == 'exit': #type exit to end it
    break
  
  #request command to server
  conn.request(cmd[0], cmd[1])

  #get response from server
  rsp = conn.getresponse()
  
  #print server response and data
  print(rsp.status, rsp.reason)
  data_received = rsp.read()
  print(data_received)
  
conn.close()