import pygame
from Core.GameObject import GameObjectBase

class Player(GameObjectBase):
    def __init__(self, gameWindow, x, y):
        self.gameWindow = gameWindow

        self.x = x
        self.y = y

        self.files = pygame.image.load("SPRITES/Human/Human_0_Idle0.png")
    
    def Render(self, cameraX, cameraY):
        self.playerSprite = self.gameWindow.blit(self.files, (self.x + cameraX, self.y + cameraY))