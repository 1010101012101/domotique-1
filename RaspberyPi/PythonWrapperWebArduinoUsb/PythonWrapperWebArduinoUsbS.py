#!/usr/bin/python

import serial, time
import sys
import socket
import datetime
import sqlite3
# Echo client program
import socket

HOST = ''    # The remote host
PORT = 50007          # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
s.send('J')

data = s.recv(1024)

s.close()

print 'Received', repr(data)