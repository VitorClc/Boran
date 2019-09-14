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

        self.files = pygame.image.load("SPRITES/Human/Human_0_Idle0.png")

        self.position = startPosition
        self.mapData = mapData
        self.grid = Grid(matrix=mapData)

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    def cartesianToIsometric(self, cartesian):
        self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y), (cartesian.x + cartesian.y) / 2)
        self.isoReal = pygame.math.Vector2(cartesian.x / 128, math.floor(-cartesian.y / 128))

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
        self.cartesianToIsometric(self.cartesianPos) 

        self.playerSprite = self.gameWindow.blit(self.files, (self.isoMov.x + cameraX, self.isoMov.y + cameraY))