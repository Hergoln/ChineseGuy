import pygame
from Pawn import Pawn
from GameCube import GameCube
from struct import *
from client import Connection
from client import PacketType
import threading

class Board():
    winnerColorText = ['BLUE', 'GREEN', 'YELLOW', 'RED']
    colors = [(0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]

    def __init__(self, boardImgPath, screen, tickrate):
        self.connection = Connection()
        self.communication_listening_thread = threading.Thread(target=self.communicationListeningFunction, args=())
        self.communication_listening_thread.start()
        self.screen = screen
        self.tickrate = tickrate
        self.myColor = 0
        self.boardImg = pygame.transform.scale(
            pygame.image.load(boardImgPath).convert(), (screen.get_width(), screen.get_height())
        )
        # indicates who is now playing
        self.player = 1
        self.pawns = []
        for i in range(4):
            for j in range(4):
                self.pawns.append(Pawn(self, 48, i + 1))
        self.cube = GameCube(self, self.screen.get_width() * 0.7, self.screen.get_height() * 0.2, 70)
        self.points = [
            0,  # blue
            0,  # green
            0,  # yellow
            0  # red
        ]
        self.winner = 0
        self.ended = False

    def render(self):
        self.screen.blit(self.boardImg, (0, 0))
        self.cube.render()
        [pawn.render() for pawn in self.pawns]
        if self.cube.currentFrame > 0:
            self.cube.rollAnimation()
        if self.ended:
            self.renderWiner(self.winner)
        else:
            self.renderCurrentPlayer()

    def beatPawn(self, index):
        for pawn in self.pawns:
            if pawn.posIndex == index:
                pawn.reset()

    def setPawn(self, index, color):
        Pawn.fieldPosArr[3 * index + 2] = color

    def addPoint(self, color):
        self.points[color - 1] += 1
        for index in range(len(self.points)):
            if self.points[index] >= 4:
                self.winner = index + 1
                self.ended = True

    def renderWiner(self, color):
        pygame.font.init()
        font = pygame.font.SysFont(None, 50)
        winnerImg = pygame.image.load('gfx/winner' + str(color) + '.png').convert()
        self.screen.blit(winnerImg,
                         ((self.screen.get_width() / 2) - winnerImg.get_width() / 2,
                          (self.screen.get_height() / 2) - winnerImg.get_height() / 2))
        self.screen.blit(font.render(self.winnerColorText[color - 1] + ' wins', True, self.colors[color - 1]),
                         ((self.screen.get_width() / 2) - winnerImg.get_width() / 4,
                          (self.screen.get_height() / 2) + winnerImg.get_height() / 4))

    def renderCurrentPlayer(self):
        pygame.font.init()
        font = pygame.font.SysFont(None, 50)
        self.screen.blit(
            font.render(self.winnerColorText[self.player - 1], True, self.colors[self.player - 1]),
            (self.screen.get_width() * 0.1,
             self.screen.get_height() * 0.7))

    def handleMouseClick(self, x, y):
        if self.ended:
            return
        if self.cube.isClicked(x, y):
            if self.cube.currentFrame <= 0:
                self.connection.requestCubeValue()
        else:
            for pawn in self.pawns:
                if (pawn.getColor() == self.color):
                    if pawn.isInGame(x, y) or pawn.isInHome(x, y):
                        self.connection.sendMovement(self.cube.value, x, y)
  
    def handleMovementFunction(self, cube_value, x, y):
        for pawn in self.pawns:
            if pawn.isInGame(x, y):
                    pawn.move(cube_value)
            elif pawn.isInHome(x, y):
                pawn.throwIntoGame()

    def handleCubeValueResponse(self, value):
        self.cube.roll(value)

    def communicationListeningFunction(self):
        while True:
            data = self.connection.receive()
            try:
                packet_type, value, x, y = unpack('hhii', data)
            except:
                print("Disconnected")
                self.shutDown()
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                break
            if(packet_type == PacketType.MOVEMENT):
                self.handleMovementFunction(value, x, y)
            elif(packet_type == PacketType.CUBE_REQUEST):
                if self.cube.currentFrame <= 0:
                    self.handleCubeValueResponse(value)
            elif(packet_type == PacketType.COLOR_INFO):
                self.color = value
                print(self.color)
            elif(packet_type == PacketType.RESET):
                self.reset()

    def reset(self):
        for pawn in self.pawns:
            pawn.reset()


    def shutDown(self):
        self.connection.close()
