import pygame


class Pawn:
    fieldPosArr = [
        349, 35, 0,
        348, 81, 0,
        350, 131, 0,
        348, 180, 0,
        348, 239, 0,
        395, 241, 0,
        449, 239, 0,
        500, 242, 0,
        551, 242, 0,
        551, 296, 0,
        552, 347, 0,
        502, 347, 0,
        451, 348, 0,
        395, 347, 0,
        349, 349, 0,
        348, 399, 0,
        347, 448, 0,
        349, 497, 0,
        349, 554, 0,
        297, 554, 0,
        242, 552, 0,
        243, 503, 0,
        242, 451, 0,
        243, 397, 0,
        242, 348, 0,
        179, 345, 0,
        132, 344, 0,
        81, 344, 0,
        35, 345, 0,
        38, 296, 0,
        35, 244, 0,
        80, 243, 0,
        130, 243, 0,
        179, 241, 0,
        242, 239, 0,
        242, 188, 0,
        241, 134, 0,
        241, 81, 0,
        242, 36, 0,
        296, 36, 0
    ]

    homePosArr = [
        497, 34, 0,  # blue
        559, 35, 0,
        493, 80, 0,
        557, 85, 0,
        499, 506, 0,  # green
        551, 505, 0,
        503, 558, 0,
        555, 566, 0,
        38, 503, 0,  # yellow
        87, 504, 0,
        36, 562, 0,
        88, 557, 0,
        31, 37, 0,  # red
        87, 35, 0,
        32, 86, 0,
        89, 85, 0
    ]

    endingPosArr = [
        292, 235, 0,  # blue
        297, 195, 0,
        294, 142, 0,
        295, 87, 0,
        349, 298, 0,  # green
        398, 298, 0,
        453, 299, 0,
        504, 296, 0,
        296, 353, 0,  # yellow
        295, 400, 0,
        295, 452, 0,
        294, 505, 0,
        240, 296, 0,  # red
        192, 296, 0,
        139, 295, 0,
        87, 294, 0
    ]

    def __init__(self, board, size, color):
        self.board = board
        self.size = size
        self.color = color
        self.image = pygame.image.load("gfx/pawn" + str(color) + ".png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.inGame = False
        self.ended = False
        self.posIndex = -1
        self.posX = 0
        self.posY = 0
        self.xStep = 0
        self.yStep = 0
        self.destinationX = 0
        self.destinationY = 0
        self.currentFrame = 0
        self.homePosInd = 0
        self.endPosInd = 0
        self.setHomePos()

    def render(self):
        if self.currentFrame < self.board.tickrate:
            self.posX += self.xStep
            self.posY += self.yStep
            self.currentFrame += 1
        else:
            self.xStep = 0
            self.yStep = 0
            self.currentFrame = 0
        self.board.screen.blit(
            self.image,
            (
                self.posX,
                self.posY
            )
        )

    def getColor(self):
        return self.color

    def throwIntoGame(self):
        if self.fieldPosArr[(3 * 10 * (self.color - 1) + 2) % len(self.fieldPosArr)] != 0:
            self.board.beatPawn((10 * (self.color - 1)) % (len(self.fieldPosArr) // 3))

        self.moveParams(self.fieldPosArr[3 * 10 * (self.color - 1)] - (self.size / 2),
                        self.fieldPosArr[3 * 10 * (self.color - 1) + 1] - (self.size / 2))
        self.fieldPosArr[3 * 10 * (self.color - 1) + 2] = self.color
        self.inGame = True
        self.posIndex = 10 * (self.color - 1)
        self.homePosArr[3 * (4 * (self.color - 1) + self.homePosInd) + 2] = 0

    def move(self, step):
        if (self.posIndex < (10 * (self.color - 1)) <= (self.posIndex + step) or
                (self.posIndex < len(self.fieldPosArr) // 3 <= self.posIndex + step and (10 * (self.color - 1)) == 0)):
            self.setCastlePos()
            self.board.addPoint(self.color)
        else:
            if self.fieldPosArr[(3 * (self.posIndex + step) + 2) % len(self.fieldPosArr)] != 0:
                self.board.beatPawn((self.posIndex + step) % (len(self.fieldPosArr) / 3))
            self.fieldPosArr[3 * self.posIndex + 2] = 0
            self.posIndex += step
            self.posIndex %= len(Pawn.fieldPosArr) // 3

            self.moveParams(self.fieldPosArr[3 * self.posIndex] - self.size / 2,
                            self.fieldPosArr[3 * self.posIndex + 1] - self.size / 2)

            self.fieldPosArr[3 * self.posIndex + 2] = self.color

    def isInGame(self, x, y):
        if not self.ended and abs(x - self.size // 2 - self.posX) < self.size // 2 and abs(
                y - self.size // 2 - self.posY) < self.size // 2 and self.inGame:
            return True
        return False

    def isInHome(self, x, y):
        if not self.ended and abs(x - self.size // 2 - self.posX) < self.size // 2 and abs(
                y - self.size // 2 - self.posY) < self.size // 2 and not self.inGame:
            return True
        return False

    def reset(self):
        self.inGame = False
        self.fieldPosArr[3 * self.posIndex + 2] = 0
        self.posIndex = -1
        self.setHomePos()

    def setHomePos(self):
        self.homePosInd = 0
        while self.homePosArr[3 * (4 * (self.color - 1) + self.homePosInd) + 2] != 0:
            self.homePosInd += 1
        self.moveParams(self.homePosArr[3 * (4 * (self.color - 1) + self.homePosInd)] - self.size / 2,
                        self.homePosArr[3 * (4 * (self.color - 1) + self.homePosInd) + 1] - self.size / 2)
        self.homePosArr[3 * (4 * (self.color - 1) + self.homePosInd) + 2] = 1

    def setCastlePos(self):
        self.posIndex = -1
        self.inGame = False
        self.endPosInd = 0
        while self.endingPosArr[3 * (4 * (self.color - 1) + self.endPosInd) + 2] != 0:
            self.endPosInd += 1
        self.moveParams(self.endingPosArr[3 * (4 * (self.color - 1) + self.endPosInd)] - self.size / 2,
                        self.endingPosArr[3 * (4 * (self.color - 1) + self.endPosInd) + 1] - self.size / 2)
        self.endingPosArr[3 * (4 * (self.color - 1) + self.endPosInd) + 2] = 1
        self.ended = True

    def moveParams(self, x, y):
        self.destinationX = x
        self.destinationY = y

        self.xStep = - (self.posX - self.destinationX) / self.board.tickrate
        self.yStep = - (self.posY - self.destinationY) / self.board.tickrate

        self.currentFrame = 0
