import pygame
from Core.GameObject import GameObjectBase

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Player(GameObjectBase):
    def __init__(self, gameWindow, startPosition):
        self.gameWindow = gameWindow

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isometricPos = self.cartesianToIsometric(self.cartesianPos)

        self.files = pygame.image.load("SPRITES/Human/Human_0_Idle0.png")

        self.position = startPosition
    
    def cartesianToIsometric(self, cartesian):
        return pygame.math.Vector2((cartesian.x - cartesian.y), (cartesian.x + cartesian.y) / 2)

    def ProcessInputs(self):
        events = pygame.event.get()
            
    def Render(self, cameraX, cameraY):
        self.isometricPos = self.cartesianToIsometric(self.cartesianPos)
        self.playerSprite = self.gameWindow.blit(self.files, (self.isometricPos.x + cameraX, self.isometricPos.y + cameraY))