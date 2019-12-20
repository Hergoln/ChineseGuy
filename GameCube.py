import pygame
import random


class GameCube:
    def __init__(self, board, x, y, size):
        self.posX = x
        self.posY = y
        self.size = size
        self.board = board
        self.cubeImg = pygame.transform.scale(
            pygame.image.load('gfx/1.png').convert(), (size, size)
        )
        self.value = 1
        self.currentFrame = 0

    def render(self):
        self.board.screen.blit(self.cubeImg, (self.posX, self.posY))

    def roll(self):
        self.currentFrame = self.board.tickrate // 2
        self.value = random.randint(1, 6)
        self.cubeImg = pygame.transform.scale(
            pygame.image.load('gfx/' + str(self.value) + '.png').convert(), (self.size, self.size)
        )

    def isClicked(self, x, y):
        if abs(x - self.size // 2 - self.posX) < self.size // 2 and abs(
                y - self.size // 2 - self.posY) < self.size // 2:
            return True
        return False

    def rollAnimation(self):
        self.value = random.randint(1, 6)
        self.cubeImg = pygame.transform.scale(
            pygame.image.load('gfx/' + str(self.value) + '.png').convert(), (self.size, self.size)
        )
        self.currentFrame -= 1
