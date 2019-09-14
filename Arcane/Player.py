import pygame, math
from Core.GameObject import GameObjectBase

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Player(GameObjectBase):
    def __init__(self, gameWindow, startPosition, mapData):
        self.gameWindow = gameWindow

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoMov = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoReal = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.destination = pygame.math.Vector2(startPosition.x, startPosition.y)

        self.files = pygame.image.load("SPRITES/Human/Human_0_Idle0.png")

        self.mapData = mapData
        self.grid = Grid(matrix=mapData)

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path = 0
        self.actualPath = 0
        self.moving = False
        
        self.dX = 0
        self.dY = 0

    def cartesianToIsometric(self, cartesian):
        self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y), (cartesian.x + cartesian.y) / 2)
        self.isoReal = pygame.math.Vector2(cartesian.x / 128, math.floor(-cartesian.y / 128))

    def checkPosition(self):
        if(self.moving == True):
            if(self.isoReal.x == self.destination.x):
                self.dX = 0
                print("Aligned X")
                self.moving = False

    def goToPosition(self):
        self.destination = pygame.math.Vector2(self.path[1][0], self.path[1][1])
        
        if(self.moving == False):
            if(self.isoReal.x > self.destination.x):
                self.dX = -1
            elif(self.isoReal.x < self.destination.x):
                self.dX = 1
            else:
                self.dX = 0

            self.moving = True


    def ProcessInputs(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.cartesianPos.x -= 128
                if event.key == pygame.K_RIGHT:
                    self.cartesianPos.x += 128
                if event.key == pygame.K_UP:
                    self.cartesianPos.y -= 128
                if event.key == pygame.K_DOWN:
                    self.cartesianPos.y += 128

    def Render(self, cameraX, cameraY):
        self.checkPosition()

        self.cartesianPos.x += self.dX

        self.cartesianToIsometric(self.cartesianPos) 

        self.playerSprite = self.gameWindow.blit(self.files, (self.isoMov.x + cameraX, self.isoMov.y + cameraY))