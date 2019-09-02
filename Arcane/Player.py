import pygame
from Core.GameObject import GameObjectBase

class Player(GameObjectBase):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #def Render(self, _gameWindow):
    #    pygame.draw.rect(_gameWindow, (0,0,255), (self.x,self.y, 64, 64))
