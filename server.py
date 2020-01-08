import sys
import socket
import threading
import random
from struct import *
from enum import IntEnum
import time

class PacketType(IntEnum):
		MOVEMENT = 1
		CUBE_REQUEST = 2
		COLOR_INFO = 3
		RESET = 4

class Client:
	def __init__(self, parrent):
		self.name = 'Anon'
		self.parrent = parrent
		self.is_listening = False

	def setAddress(self, addr):
		self.address = addr

	def setConnection(self, addr):
		self.connection = addr

	def send(self, data):
		self.connection.sendall(data)

	def startListening(self):
		self.listeningThread = threading.Thread(target=self.listenFunction, args=())
		self.is_listening = True
		self.listeningThread.start()

	def disconnect(self):
		self.is_listening = False
		self.connection.shutdown(socket.SHUT_RDWR)

	def listenFunction(self):
		while self.is_listening:			
			data = self.connection.recv(1024)		
			try:
				packet_type, cube_value, x, y = unpack('hhii', data)
			except:
				self.is_listening = False
				print("Client disconnected")
				self.connection.close()
				self.parrent.removeClient(self)
				break
			if(packet_type == PacketType.MOVEMENT):
				self.parrent.sendMovement(self, data)
			elif(PacketType.CUBE_REQUEST):
				self.parrent.sendCubeValue(self, data)

class Server:	
	def __init__(self):
		self.clients_list = []
		self.currentPlayer = 0;
		self.inGame = False
		self.currentCubeValue = 0
		self.is_listening_for_new_players = False;
		print("Setting up server socket")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost', 10000)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(self.server_address)
		print("Socket created and binded")
		self.sock.listen(1)
		print("Start listening")

	def connectPlayers(self):
		self.is_listening_for_new_players = True
		while self.is_listening_for_new_players:
			if(len(self.clients_list) < 4 and self.inGame == False):
				try:
					connection, client_address = self.sock.accept()
				except:
					self.is_listening_for_new_players = False
					print("Server socket closed")
					break		
				new_client = Client(self)
				new_client.setAddress(client_address)
				new_client.setConnection(connection)
				new_client.startListening()
				self.clients_list.append(new_client)
				self.sendColor(new_client)
				print("New client connected")
			else:
				time.sleep(1)

	def giveControllToNextPlayer(self):
		if(self.currentPlayer + 1 >= len(self.clients_list)):
			self.currentPlayer = 0
		else:
			self.currentPlayer = self.currentPlayer + 1

	def sendMovement(self, sender, data):
		if(self.clients_list[self.currentPlayer] == sender and self.inGame == True):
			for client in self.clients_list:
				client.send(data)
			self.giveControllToNextPlayer()

	def sendColor(self, client):
		client.send(pack('hhii', int(PacketType.COLOR_INFO), len(self.clients_list), 0, 0))

	def sendCubeValue(self, sender, data):
		self.inGame = True
		if(self.clients_list[self.currentPlayer] == sender):
			self.currentCubeValue = random.randint(1, 6)
			for client in self.clients_list:				
				client.send(pack('hhii', int(PacketType.CUBE_REQUEST), self.currentCubeValue, 0, 0))

	def removeClient(self, client):
		self.clients_list.remove(client)

	def close_server(self):
		self.is_listening_for_new_players = False
		for client in self.clients_list:
			client.disconnect()
		self.sock.shutdown(socket.SHUT_RDWR)

	def reset(self):
		for client in self.clients_list:
			client.send(pack('hhii', PacketType.RESET, 0, 0, 0))

	def run(self):
		new_clients_listening_thread = threading.Thread(target=self.connectPlayers, args=())
		new_clients_listening_thread.start()
		while True:
			command = raw_input()
			if (command == "q"):
				self.close_server()			
				break
			elif(command == "reset"):
				self.reset()

if __name__ == '__main__':
   server = Server()
   server.run()
