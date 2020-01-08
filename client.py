import sys
import socket
import threading
from struct import *
from enum import IntEnum
from server import PacketType


class Connection:	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost', 10000)
		self.sock.connect(self.server_address)

	def sendMovement(self, cube_value, x, y):
		self.send(pack('hhii', int(PacketType.MOVEMENT), cube_value, x, y))

	def requestCubeValue(self):
		self.send(pack('hhii', int(PacketType.CUBE_REQUEST), 0, 0, 0))

	def send(self, data):
		self.sock.sendall(data)

	def receive(self):
		return self.sock.recv(1024)

	def close(self):
		self.sock.close()
