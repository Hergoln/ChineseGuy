import pygame
from Board import Board
from Pawn import Pawn

(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chinese cool guy')
clock = pygame.time.Clock()

tickrate = 60
board = Board("gfx/board.png", screen, tickrate)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            board.shutDown()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = event.pos
            board.handleMouseClick(x, y)
            # print(str(x) + ', ' + str(y) + ', 0')

    board.render()
    pygame.display.flip()
    clock.tick(tickrate)
