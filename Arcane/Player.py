import pygame
from Core.GameObject import GameObjectBase

class Player(GameObjectBase):
    def __init__(self, gameWindow, startPosition):
        self.gameWindow = gameWindow

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isometricPos = self.cartesianToIsometric(self.cartesianPos)

        self.files = pygame.image.load("SPRITES/Human/Human_0_Idle0.png")
    
    def cartesianToIsometric(self, cartesian):
        return pygame.math.Vector2((cartesian.x - cartesian.y), (cartesian.x + cartesian.y) / 2)

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
        self.isometricPos = self.cartesianToIsometric(self.cartesianPos)
        self.playerSprite = self.gameWindow.blit(self.files, (self.isometricPos.x + cameraX, self.isometricPos.y + cameraY))